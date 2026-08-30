import json
from typing import Any

import httpx

from app.core.config import settings
from app.models.error import ErrorAnalysis, ParsedError


SYSTEM_PROMPT = """You are a senior software debugging assistant.
Analyze the provided structured error and return a concise diagnosis.
Do not invent facts that are not supported by the error. If uncertain, say so.
Return ONLY valid JSON with these fields:
summary (string), root_cause (string), suggested_fix (string), confidence (number 0..1).
"""


class LLMServiceError(RuntimeError):
    """Raised when the LLM provider cannot produce a valid response."""


class OpenRouterService:
    def __init__(self) -> None:
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.model = settings.openrouter_model

    async def analyze(self, error: ParsedError) -> ErrorAnalysis:
        if not settings.openrouter_api_key:
            raise LLMServiceError("OPENROUTER_API_KEY is not configured")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(error.model_dump(), ensure_ascii=False),
                },
            ],
            "temperature": 0.1,
        }

        headers = {
            "Authorization": f"Bearer {settings.openrouter_api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/madfaladam/ai-error-analyzer",
            "X-Title": settings.app_name,
        }

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload,
            )

        if response.is_error:
            raise LLMServiceError(
                f"OpenRouter request failed ({response.status_code}): {response.text[:500]}"
            )

        try:
            data: dict[str, Any] = response.json()
            content = data["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            return ErrorAnalysis(
                category=error.category,
                parsed_error=error,
                **parsed,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMServiceError("OpenRouter returned an invalid analysis response") from exc
