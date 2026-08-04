from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil

from app.services.json_generator import generate_json

router = APIRouter()


@router.post("/")
async def preview(
    file: UploadFile = File(...)
):

    path = f"uploads/{file.filename}"

    with open(path, "wb") as buffer:
        shutil.copyfileobj(
            file.file,
            buffer
        )

    df = pd.read_excel(path)

    payload = generate_json(df)

    return payload