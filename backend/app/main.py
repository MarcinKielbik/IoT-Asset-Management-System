from fastapi import FastAPI
from app.api.v1.endpoints.devices import router as devices_router


app = FastAPI(
    title="IoT Asset Management System",
    description="API for managing and monitoring IoT devices",
    version="1.0.0",
)

app.include_router(
    devices_router,
    prefix="/api/v1",
)

@app.get("/")
async def root():
    return {"message": "IoT Asset Management API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}