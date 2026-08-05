# CA Friendly Mapping for Components
# Format: Component Name → { resourceType, fields: { Field Name → real property } }

COMPONENT_CA_MAPPING = {

    "Title": {
        "resourceType": "weretail/components/content/title",
        "fields": {
            "Title": "jcr:title",
            "Type": "type"
        }
    },

    "Promo Banner": {
        "resourceType": "fca/components/content/promo-banner",
        "fields": {
            "Heading": "heading",
            "Description": "description"
        }
    },

    "Hero Banner": {
        "resourceType": "fca/components/content/hero-banner",
        "fields": {
            "Title": "title",
            "Subtitle": "subtitle"
        }
    },

    "CTA": {
        "resourceType": "fca/components/content/cta",
        "fields": {
            "Button Text": "ctaText",
            "Link": "link"
        }
    }

}