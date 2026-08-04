from app.services.component_mapper import (
    get_component_mapping
)

def build_payload(record):

    component = get_component_mapping(
        record["component_name"]
    )

    # Handle Unknown Component
    if component is None:
        return {
            "status": "failed",
            "message": f"Unknown component: {record['component_name']}"
        }

    return {
        "status": "success",
        "pagePath": record["page_path"],
        "resourceType": component["resourceType"],
        "property": record["property_name"],
        "value": record["property_value"]
    }