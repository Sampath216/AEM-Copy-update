import requests
from requests.auth import HTTPBasicAuth
from app.services.component_ca_mapping import COMPONENT_CA_MAPPING

AEM_HOST = "http://localhost:8080"
AEM_USER = "admin"
AEM_PASSWORD = "admin"


def find_component_path(page_path, resource_type, instance=1):
    """
    Finds the Nth component under the page that matches the resourceType.
    instance = 1 means first match, 2 means second match, etc.
    """
    url = f"{AEM_HOST}{page_path}.infinity.json"

    try:
        response = requests.get(
            url,
            auth=HTTPBasicAuth(AEM_USER, AEM_PASSWORD),
            timeout=20
        )

        if response.status_code != 200:
            return None

        data = response.json()
        matches = []

        def search(node, current_path):
            if isinstance(node, dict):
                if node.get("sling:resourceType") == resource_type:
                    matches.append(current_path)

                for key, value in node.items():
                    if key.startswith("jcr:") or key.startswith("sling:") or key.startswith("cq:"):
                        continue
                    search(value, f"{current_path}/{key}")

        jcr_content = data.get("jcr:content", data)
        search(jcr_content, f"{page_path}/jcr:content")

        # instance is 1-based
        index = instance - 1
        if 0 <= index < len(matches):
            return matches[index]

        return None

    except Exception:
        return None


def update_component_ca(row):
    """
    CA-Friendly component update with Instance support
    """

    page_path = row.get("Page Path")
    component_name = row.get("Component Name")
    field_name = row.get("Field Name")
    new_value = row.get("New Value")

    # Instance is optional (default = 1)
    instance = row.get("Instance", 1)
    try:
        instance = int(instance)
        if instance < 1:
            instance = 1
    except:
        instance = 1

    if not all([page_path, component_name, field_name, new_value]):
        return {
            "status": "failed",
            "message": "Missing required columns (Page Path, Component Name, Field Name, New Value)"
        }

    mapping = COMPONENT_CA_MAPPING.get(component_name)

    if not mapping:
        return {
            "status": "failed",
            "message": f"Unknown Component Name: {component_name}"
        }

    resource_type = mapping["resourceType"]
    real_property = mapping["fields"].get(field_name)

    if not real_property:
        # Try case-insensitive match for better CA experience
        real_property = None
        for key, value in mapping["fields"].items():
            if key.lower() == str(field_name).lower():
                real_property = value
                break

    if not real_property:
        return {
            "status": "failed",
            "message": f"Unknown Field Name '{field_name}' for component '{component_name}'"
        }

    # Find the correct component instance
    component_path = find_component_path(page_path, resource_type, instance)

    if not component_path:
        return {
            "status": "failed",
            "message": f"Could not find instance #{instance} of component '{component_name}' under {page_path}"
        }

    # Update the property
    url = f"{AEM_HOST}{component_path}"

    try:
        response = requests.post(
            url,
            data={real_property: new_value},
            auth=HTTPBasicAuth(AEM_USER, AEM_PASSWORD),
            timeout=15
        )

        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "message": f"Updated instance #{instance} of {component_name} ({field_name})",
                "component_path": component_path,
                "property": real_property,
                "value": new_value,
                "instance": instance
            }
        else:
            return {
                "status": "failed",
                "message": f"AEM Error {response.status_code}: {response.text[:200]}"
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": f"Connection error: {str(e)}"
        }