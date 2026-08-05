from fastapi import FastAPI
from datetime import datetime
from app.utils.folder_setup import *
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import upload
from app.routes import logs
from app.routes import preview
from app.routes import payload_preview
from app.routes import mock_update
from app.routes import update_preview
from app.routes import execute_update
from app.routes import seo_update
from app.routes import component_update


app = FastAPI(
    title="Author Automation Portal"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    upload.router,
    prefix="/upload",
    tags=["Upload"]
)

app.include_router(
    logs.router,
    prefix="/logs",
    tags=["Logs"]
)

app.include_router(
    preview.router,
    prefix="/preview",
    tags=["Preview"]
)


app.include_router(
    payload_preview.router,
    prefix="/payload-preview",
    tags=["Payload Preview"]
)

app.include_router(
    mock_update.router,
    prefix="/mock-update",
    tags=["Mock Update"]
)

app.include_router(
    update_preview.router,
    prefix="/update-preview",
    tags=["Update Preview"]
)

app.include_router(
    execute_update.router,
    prefix="/execute-update",
    tags=["Execute Update"]
)

app.include_router(
    seo_update.router,
    prefix="/seo-update",
    tags=["SEO Update"]
)

app.include_router(
    component_update.router,
    prefix="/component-update",
    tags=["Component Update"]
)

@app.get("/")
def home():
    return {
        "message": "Portal Running"
    }