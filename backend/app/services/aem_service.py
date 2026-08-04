import requests
from requests.auth import HTTPBasicAuth

# ======================
# LOCAL AEM SETTINGS
# ======================
AEM_HOST = "http://localhost:8080"
AEM_USER = "admin"
AEM_PASSWORD = "admin"


def update_component(payload):

    # If earlier step already failed
    if payload.get("status") == "failed":
        return payload

    # In your Excel, "pagePath" actually contains the full component path
    component_path = payload.get("pagePath")
    property_name = payload.get("property")
    property_value = payload.get("value")

    if not component_path or not property_name:
        return {
            "status": "failed",
            "message": "Missing component path or property name",
            "payload": payload
        }

    # Full URL to the component
    url = f"{AEM_HOST}{component_path}"

    try:
        response = requests.post(
            url,
            data={
                property_name: property_value
            },
            auth=HTTPBasicAuth(AEM_USER, AEM_PASSWORD),
            timeout=15
        )

        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "message": f"Successfully updated {property_name} = {property_value}",
                "component_path": component_path,
                "aem_status_code": response.status_code,
                "payload": payload
            }
        else:
            return {
                "status": "failed",
                "message": f"AEM Error {response.status_code}: {response.text[:250]}",
                "component_path": component_path,
                "aem_status_code": response.status_code,
                "payload": payload
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": f"Connection Error: {str(e)}",
            "payload": payload
        }