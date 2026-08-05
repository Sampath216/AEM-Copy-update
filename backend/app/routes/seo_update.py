from fastapi import APIRouter, UploadFile, File
import pandas as pd
import shutil

from app.services.seo_service import update_seo_properties

router = APIRouter()


@router.post("/")
async def seo_update(file: UploadFile = File(...)):

    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    df = pd.read_excel(file_path)

    results = []

    for _, row in df.iterrows():
        result = update_seo_properties(row.to_dict())
        results.append(result)

    success_count = sum(1 for r in results if r["status"] == "success")
    failed_count = len(results) - success_count

    return {
        "total_records": len(results),
        "success_count": success_count,
        "failed_count": failed_count,
        "results": results
    }