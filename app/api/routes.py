from fastapi import APIRouter

from app.models.error import ErrorLog, ParsedError
from app.services.parser import parse_error_log


router = APIRouter(prefix="/api/v1", tags=["analyzer"])


@router.post("/parse", response_model=ParsedError)
def parse_log(payload: ErrorLog) -> ParsedError:
    """Parse a raw stack trace into structured error information."""
    return parse_error_log(payload.raw_log)
