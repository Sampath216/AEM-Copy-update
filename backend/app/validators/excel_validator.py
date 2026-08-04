import pandas as pd


def validate_excel(df):
    errors = []

    required_columns = [
        "Page Path",
        "Component Name",
        "Property",
        "New Value"
    ]

    # Check Required Columns
    for column in required_columns:
        if column not in df.columns:
            errors.append({
                "row": 0,
                "error": f"Missing column: {column}"
            })

    # Stop further validation if columns missing
    if errors:
        return errors

    # Validate Rows
    for index, row in df.iterrows():

        # Empty Page Path
        if pd.isna(row["Page Path"]) or str(row["Page Path"]).strip() == "":
            errors.append({
                "row": index + 2,
                "error": "Page Path is empty"
            })

        # Empty Component Name
        if pd.isna(row["Component Name"]) or str(row["Component Name"]).strip() == "":
            errors.append({
                "row": index + 2,
                "error": "Component Name is empty"
            })

        # Empty Property
        if pd.isna(row["Property"]) or str(row["Property"]).strip() == "":
            errors.append({
                "row": index + 2,
                "error": "Property is empty"
            })

        # Empty New Value
        if pd.isna(row["New Value"]) or str(row["New Value"]).strip() == "":
            errors.append({
                "row": index + 2,
                "error": "New Value is empty"
            })

        # Validate Page Path
        if not str(row["Page Path"]).startswith("/"):
            errors.append({
                "row": index + 2,
                "error": "Invalid Page Path"
            })

    # Check Duplicates
    duplicates = df[df.duplicated()]

    for index in duplicates.index:
        errors.append({
            "row": index + 2,
            "error": "Duplicate Record"
        })

    return errors