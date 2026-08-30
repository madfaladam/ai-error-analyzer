from fastapi import FastAPI

from app.api.routes import router as analyzer_router
from app.core.config import settings


app = FastAPI(
    title=settings.app_name,
    description="AI-powered developer error analyzer using LLM and RAG.",
    version="0.1.0",
)

app.include_router(analyzer_router)


@app.get("/health", tags=["system"])
def health_check() -> dict[str, str]:
    """Return application health information."""
    return {
        "status": "ok",
        "service": settings.app_name,
        "environment": settings.app_env,
    }
