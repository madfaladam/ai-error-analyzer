from enum import Enum

from pydantic import BaseModel, Field


class ErrorCategory(str, Enum):
    UNKNOWN = "unknown"
    NULL_REFERENCE = "null_reference"
    TYPE_ERROR = "type_error"
    SYNTAX_ERROR = "syntax_error"
    IMPORT_ERROR = "import_error"
    NETWORK_ERROR = "network_error"
    DATABASE_ERROR = "database_error"
    PERMISSION_ERROR = "permission_error"
    FILE_ERROR = "file_error"


class ErrorLog(BaseModel):
    raw_log: str = Field(..., min_length=1, max_length=50000)
    language: str | None = None
    source: str | None = None


class ParsedError(BaseModel):
    exception_type: str | None = None
    message: str | None = None
    file: str | None = None
    line: int | None = None
    function: str | None = None
    category: ErrorCategory = ErrorCategory.UNKNOWN
    raw_log: str


class ErrorAnalysis(BaseModel):
    category: ErrorCategory
    summary: str
    root_cause: str
    suggested_fix: str
    confidence: float = Field(..., ge=0, le=1)
    parsed_error: ParsedError
