from fastapi import APIRouter
from app.database.db import SessionLocal
from app.models.log_model import ExecutionLog

router = APIRouter()


@router.get("/")
def get_logs():

    db = SessionLocal()

    try:
        logs = db.query(ExecutionLog).all()

        result = []

        for log in logs:
            result.append({
                "id": log.id,
                "filename": log.filename,
                "total_rows": log.total_rows,
                "valid_rows": log.valid_rows,
                "error_count": log.error_count,
                "created_at": log.created_at
            })

        return result

    finally:
        db.close()