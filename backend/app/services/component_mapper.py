# Component Mapping Dictionary

COMPONENT_MAPPING = {

    "hero-banner": {
        "resourceType":
        "fca/components/content/hero-banner"
    },

    "promo-banner": {
        "resourceType":
        "fca/components/content/promo-banner"
    },

    "cta-component": {
        "resourceType":
        "fca/components/content/cta"
    },

    "title": {
    "resourceType": "weretail/components/content/title"
     },

}


# Function to fetch mapping

def get_component_mapping(component_name):

    return COMPONENT_MAPPING.get(
        component_name,
        None
    )