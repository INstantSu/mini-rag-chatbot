from fastapi import FastAPI

from app.config import settings


app = FastAPI(title=settings.app_name)


@app.get("/health")
def health_check():
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "environment": settings.app_env,
    }
