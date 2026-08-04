from app.database.db import engine
from app.models.log_model import Base

Base.metadata.create_all(bind=engine)

print("Database Created Successfully")