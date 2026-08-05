import requests
from requests.auth import HTTPBasicAuth

AEM_HOST = "http://localhost:8080"
AEM_USER = "admin"
AEM_PASSWORD = "admin"


def update_seo_properties(row):
    """
    Updates SEO / Page properties on jcr:content node
    """

    page_path = row.get("Page Properties Path")

    if not page_path:
        return {
            "status": "failed",
            "message": "Missing Page Properties Path",
            "row": row
        }

    # Properties we want to update
    properties = {}

    if row.get("jcr:title"):
        properties["jcr:title"] = row["jcr:title"]

    if row.get("jcr:description"):
        properties["jcr:description"] = row["jcr:description"]

    if row.get("pageTitle"):
        properties["pageTitle"] = row["pageTitle"]

    if row.get("cq:canonicalUrl"):
        properties["cq:canonicalUrl"] = row["cq:canonicalUrl"]

    if not properties:
        return {
            "status": "failed",
            "message": "No properties to update",
            "row": row
        }

    url = f"{AEM_HOST}{page_path}"

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
                "message": f"Updated SEO properties on {page_path}",
                "updated_properties": list(properties.keys()),
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