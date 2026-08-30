from app.models.error import ErrorCategory
from app.services.parser import classify_exception, parse_error_log


def test_parse_python_traceback() -> None:
    log = '''Traceback (most recent call last):\n  File "app/player.py", line 42, in update\n    self.camera.transform.position\nAttributeError: 'NoneType' object has no attribute 'transform'\n'''

    result = parse_error_log(log)

    assert result.exception_type == "AttributeError"
    assert result.file == "app/player.py"
    assert result.line == 42
    assert result.function == "update"
    assert result.category == ErrorCategory.NULL_REFERENCE


def test_classify_network_error() -> None:
    assert classify_exception("ConnectionError", "connection refused") == ErrorCategory.NETWORK_ERROR


def test_unknown_error() -> None:
    result = parse_error_log("SomethingUnexpected: something happened")

    assert result.exception_type == "SomethingUnexpected"
    assert result.category == ErrorCategory.UNKNOWN
