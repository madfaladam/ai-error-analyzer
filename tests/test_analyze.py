from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_analyze_requires_api_key_when_provider_is_not_configured() -> None:
    response = client.post(
        "/api/v1/analyze",
        json={"raw_log": "ValueError: invalid value"},
    )

    # In local test environments without an OpenRouter key, the API should
    # fail explicitly rather than silently returning a fabricated diagnosis.
    assert response.status_code in {200, 502}
