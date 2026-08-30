from fastapi import APIRouter, HTTPException

from app.models.error import ErrorAnalysis, ErrorLog, ParsedError
from app.services.knowledge_base import get_knowledge_base
from app.services.llm import LLMServiceError, OpenRouterService
from app.services.parser import parse_error_log


router = APIRouter(prefix="/api/v1", tags=["analyzer"])
llm_service = OpenRouterService()
knowledge_base = get_knowledge_base()


@router.post("/parse", response_model=ParsedError)
def parse_log(payload: ErrorLog) -> ParsedError:
    """Parse a raw stack trace into structured error information."""
    return parse_error_log(payload.raw_log)


@router.post("/analyze", response_model=ErrorAnalysis)
async def analyze_log(payload: ErrorLog) -> ErrorAnalysis:
    """Parse an error, retrieve relevant knowledge, and ask the LLM for a diagnosis."""
    parsed_error = parse_error_log(payload.raw_log)
    query = " ".join(
        part for part in [
            payload.language or "",
            parsed_error.exception_type or "",
            parsed_error.message or "",
            parsed_error.category.value,
        ] if part
    )
    retrieved = knowledge_base.search(query, top_k=3)

    try:
        return await llm_service.analyze(parsed_error, context_documents=retrieved)
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
