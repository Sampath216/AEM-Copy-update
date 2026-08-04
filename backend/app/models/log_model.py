from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    total_rows = Column(Integer)
    valid_rows = Column(Integer)
    error_count = Column(Integer)

    # Timestamp Column
    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )