def create_preview_record(payload):

    if payload.get("status") == "failed":

        return {
            "page_path": "",
            "component": "",
            "property": "",
            "new_value": "",
            "status": "FAILED",
            "message": payload["message"]
        }

    return {
        "page_path": payload["pagePath"],
        "component": payload["resourceType"],
        "property": payload["property"],
        "new_value": payload["value"],
        "status": "READY"
    }