import requests
from requests.auth import HTTPBasicAuth

AEM_HOST = "http://localhost:8080"
AEM_USER = "admin"
AEM_PASSWORD = "admin"

# Mapping: What CA sees → Real AEM property
SEO_FIELD_MAPPING = {
    "Meta Title": "jcr:title",
    "Meta Description": "jcr:description",
    "Page Title": "pageTitle",
    "Canonical URL": "cq:canonicalUrl"
}


def update_seo_properties(row):
    """
    CA-Friendly SEO property update
    """

    page_path = row.get("Page Path")

    if not page_path:
        return {
            "status": "failed",
            "message": "Missing Page Path",
            "row": row
        }

    # Automatically add /jcr:content
    target_path = f"{page_path.rstrip('/')}/jcr:content"

    # Build properties using mapping
    properties = {}

    for ca_field, aem_property in SEO_FIELD_MAPPING.items():
        value = row.get(ca_field)
        if value and str(value).strip() != "":
            properties[aem_property] = str(value).strip()

    if not properties:
        return {
            "status": "failed",
            "message": "No valid SEO fields found to update",
            "row": row
        }

    url = f"{AEM_HOST}{target_path}"

    try:
        response = requests.post(
            url,
            data=properties,
            auth=HTTPBasicAuth(AEM_USER, AEM_PASSWORD),
            timeout=15
        )

        if response.status_code in [200, 201]:
            return {
                "status": "success",
                "message": f"Updated SEO properties on {target_path}",
                "updated_fields": list(properties.keys()),
                "aem_status_code": response.status_code
            }
        else:
            return {
                "status": "failed",
                "message": f"AEM Error {response.status_code}: {response.text[:250]}",
                "aem_status_code": response.status_code
            }

    except Exception as e:
        return {
            "status": "failed",
            "message": f"Connection error: {str(e)}"
        }