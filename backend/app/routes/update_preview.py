from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil

from app.services.json_generator import generate_json
from app.services.payload_generator import build_payload
from app.services.preview_service import create_preview_record

router = APIRouter()


@router.post("/")
async def update_preview(
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

    preview_records = []

    for record in records:

        payload = build_payload(record)

        preview = create_preview_record(
            payload
        )

        preview_records.append(
            preview
        )

    return preview_records