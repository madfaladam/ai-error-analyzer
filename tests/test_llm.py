import json

import httpx
import pytest

from app.core.config import settings
from app.models.error import ErrorCategory
from app.services.llm import OpenRouterService
from app.services.parser import parse_error_log


@pytest.mark.anyio
async def test_llm_service_parses_provider_response(monkeypatch: pytest.MonkeyPatch) -> None:
    error = parse_error_log("ValueError: invalid player state")

    async def mock_post(self, url, **kwargs):
        payload = {
            "choices": [
                {
                    "message": {
                        "content": json.dumps(
                            {
                                "summary": "The value supplied to the operation is invalid.",
                                "root_cause": "The application received an invalid player state.",
                                "suggested_fix": "Validate the state before processing it.",
                                "confidence": 0.91,
                            }
                        )
                    }
                }
            ]
        }
        return httpx.Response(200, json=payload, request=httpx.Request("POST", url))

    monkeypatch.setattr(httpx.AsyncClient, "post", mock_post)
    monkeypatch.setattr(settings, "openrouter_api_key", "test-key")

    result = await OpenRouterService().analyze(error)

    assert result.category == ErrorCategory.UNKNOWN
    assert result.confidence == 0.91
    assert result.summary.startswith("The value supplied")
