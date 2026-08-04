from fastapi import APIRouter, UploadFile, File
import shutil
import pandas as pd

from app.validators.excel_validator import validate_excel
from app.services.log_service import save_log

router = APIRouter()


@router.get("/")
def upload_home():
    return {
        "message": "Upload API Working"
    }


@router.post("/")
async def upload_file(
    file: UploadFile = File(...)
):

    # Save uploaded file
    file_path = f"uploads/{file.filename}"

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Read Excel
    df = pd.read_excel(file_path)

    # Run validations
    errors = validate_excel(df)

    total_rows = len(df)
    valid_rows = total_rows - len(errors)
    error_count = len(errors)

    # Save execution log
    save_log(
        filename=file.filename,
        total_rows=total_rows,
        valid_rows=valid_rows,
        error_count=error_count
    )

    return {
        "status": "success",
        "filename": file.filename,
        "total_rows": total_rows,
        "valid_rows": valid_rows,
        "error_count": error_count,
        "errors": errors
    }