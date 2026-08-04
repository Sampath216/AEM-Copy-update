from app.database.db import SessionLocal
from app.models.log_model import ExecutionLog


def save_log(filename, total_rows, valid_rows, error_count):

    db = SessionLocal()

    try:
        log = ExecutionLog(
            filename=filename,
            total_rows=total_rows,
            valid_rows=valid_rows,
            error_count=error_count
        )

        db.add(log)
        db.commit()

    finally:
        db.close()