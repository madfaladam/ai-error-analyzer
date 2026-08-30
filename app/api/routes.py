from fastapi import APIRouter, HTTPException

from app.models.error import ErrorAnalysis, ErrorLog, ParsedError
from app.services.llm import LLMServiceError, OpenRouterService
from app.services.parser import parse_error_log


router = APIRouter(prefix="/api/v1", tags=["analyzer"])
llm_service = OpenRouterService()


@router.post("/parse", response_model=ParsedError)
def parse_log(payload: ErrorLog) -> ParsedError:
    """Parse a raw stack trace into structured error information."""
    return parse_error_log(payload.raw_log)


@router.post("/analyze", response_model=ErrorAnalysis)
async def analyze_log(payload: ErrorLog) -> ErrorAnalysis:
    """Parse an error and ask the configured LLM for a diagnosis."""
    parsed_error = parse_error_log(payload.raw_log)

    try:
        return await llm_service.analyze(parsed_error)
    except LLMServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc
