from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil

from app.services.json_generator import generate_json
from app.services.payload_generator import build_payload

router = APIRouter()


@router.post("/")
async def preview_payload(
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

    payloads = []

    for record in records:

        payload = build_payload(
            record
        )

        payloads.append(payload)

    return payloads