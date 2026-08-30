import re

from app.models.error import ErrorCategory, ParsedError


# Common exception patterns across Python, JavaScript/TypeScript, Java, and C#.
_EXCEPTION_PATTERN = re.compile(
    r"(?P<type>[A-Za-z_][\w.]*(?:Error|Exception|Fault))(?::|\s+-\s+)?\s*(?P<message>[^\n\r]*)",
    re.MULTILINE,
)

_PYTHON_LOCATION_PATTERN = re.compile(
    r'File [\"\'](?P<file>[^\"\']+)[\"\'], line (?P<line>\d+), in (?P<function>[^\n\r]+)'
)

_JS_LOCATION_PATTERN = re.compile(
    r"at\s+(?:(?P<function>[\w.$<>-]+)\s+)?\(?(?P<file>[^():\s]+):(?P<line>\d+):(?P<column>\d+)\)?"
)

_CSHARP_LOCATION_PATTERN = re.compile(
    r"at\s+(?P<function>[^\r\n]+)\s+in\s+(?P<file>[^:]+):line\s+(?P<line>\d+)"
)


def classify_exception(exception_type: str | None, message: str | None) -> ErrorCategory:
    """Classify an exception using deterministic rules before invoking an LLM."""
    text = f"{exception_type or ''} {message or ''}".lower()

    rules = [
        (ErrorCategory.NULL_REFERENCE, ("nullreference", "attributeerror", "noneType".lower())),
        (ErrorCategory.TYPE_ERROR, ("typeerror", "type mismatch", "invalidcast")),
        (ErrorCategory.SYNTAX_ERROR, ("syntaxerror", "parseerror", "compilationerror")),
        (ErrorCategory.IMPORT_ERROR, ("importerror", "modulenotfound", "filenotfounderror")),
        (ErrorCategory.NETWORK_ERROR, ("connectionerror", "timeouterror", "networkerror", "socketerror")),
        (ErrorCategory.DATABASE_ERROR, ("databaseerror", "sqlerror", "sqlexception", "dberror")),
        (ErrorCategory.PERMISSION_ERROR, ("permissionerror", "accessdenied", "unauthorized", "forbidden")),
        (ErrorCategory.FILE_ERROR, ("ioerror", "oserror", "filenotfound")),
    ]

    for category, keywords in rules:
        if any(keyword in text for keyword in keywords):
            return category

    return ErrorCategory.UNKNOWN


def parse_error_log(raw_log: str) -> ParsedError:
    """Extract useful structured fields from a raw stack trace."""
    exception_match = _EXCEPTION_PATTERN.search(raw_log)
    exception_type = exception_match.group("type") if exception_match else None
    message = exception_match.group("message").strip() if exception_match else None

    location_match = _PYTHON_LOCATION_PATTERN.search(raw_log)
    if not location_match:
        location_match = _JS_LOCATION_PATTERN.search(raw_log)
    if not location_match:
        location_match = _CSHARP_LOCATION_PATTERN.search(raw_log)

    file = line = function = None
    if location_match:
        groups = location_match.groupdict()
        file = groups.get("file")
        function = groups.get("function")
        line_text = groups.get("line")
        line = int(line_text) if line_text else None

    category = classify_exception(exception_type, message)

    return ParsedError(
        exception_type=exception_type,
        message=message,
        file=file,
        line=line,
        function=function,
        category=category,
        raw_log=raw_log,
    )
