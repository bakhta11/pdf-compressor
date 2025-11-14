from fastapi import FastAPI
from app.api.v1.endpoints import router as api_router

app = FastAPI(
    title="PDF Compressor",
    version="1.0.0",
)

app.include_router(api_router, prefix="/api/v1")
