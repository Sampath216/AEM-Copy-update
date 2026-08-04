def generate_json(df):

    payload = []

    for _, row in df.iterrows():

        payload.append({
            "page_path": row["Page Path"],
            "component_name": row["Component Name"],
            "property_name": row["Property"],
            "property_value": row["New Value"]
        })

    return payload