from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_parse_endpoint_returns_structured_error() -> None:
    response = client.post(
        "/api/v1/parse",
        json={
            "language": "python",
            "raw_log": 'File "player.py", line 10, in update\nValueError: invalid state',
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["exception_type"] == "ValueError"
    assert data["line"] == 10
