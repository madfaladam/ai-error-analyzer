import json
from typing import Any

import httpx

from app.core.config import settings
from app.models.error import AnalysisSource, ErrorAnalysis, ParsedError
from app.services.vector_store import Document


SYSTEM_PROMPT = """You are a senior software debugging assistant.
Analyze the provided structured error and supporting technical knowledge.
Use the knowledge only when it is relevant. Do not invent facts that are not supported.
If uncertain, say so.
Return ONLY valid JSON with these fields:
summary (string), root_cause (string), suggested_fix (string), confidence (number 0..1).
"""


class LLMServiceError(RuntimeError):
    """Raised when the LLM provider cannot produce a valid response."""


class OpenRouterService:
    def __init__(self) -> None:
        self.base_url = settings.openrouter_base_url.rstrip("/")
        self.model = settings.openrouter_model

    async def analyze(
        self,
        error: ParsedError,
        context_documents: list[tuple[Document, float]] | None = None,
    ) -> ErrorAnalysis:
        if not settings.openrouter_api_key:
            raise LLMServiceError("OPENROUTER_API_KEY is not configured")

        context_documents = context_documents or []
        context = "\n\n".join(
            f"SOURCE: {doc.source}\nRELEVANCE: {score:.3f}\n{doc.content}"
            for doc, score in context_documents
        )

        user_content = {
            "error": error.model_dump(),
            "supporting_knowledge": context or "No supporting knowledge was retrieved.",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": json.dumps(user_content, ensure_ascii=False),
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
            sources = [
                AnalysisSource(source=doc.source, relevance=score)
                for doc, score in context_documents
            ]
            return ErrorAnalysis(
                category=error.category,
                parsed_error=error,
                sources=sources,
                **parsed,
            )
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            raise LLMServiceError("OpenRouter returned an invalid analysis response") from exc
