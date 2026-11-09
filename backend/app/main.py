from fastapi import FastAPI

app = FastAPI(
    title="IoT Asset Management System",
    description="API for managing and monitoring IoT devices",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"message": "IoT Asset Management API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}