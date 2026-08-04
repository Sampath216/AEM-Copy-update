from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil

from app.services.json_generator import generate_json
from app.services.payload_generator import build_payload
from app.services.aem_service import update_component

router = APIRouter()


@router.post("/")
async def mock_update(
    file: UploadFile = File(...)
):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    df = pd.read_excel(file_path)

    records = generate_json(df)

    results = []

    for record in records:

        payload = build_payload(record)

        result = update_component(payload)

        results.append(result)

    return results