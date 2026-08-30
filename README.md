# AI Error Analyzer

AI-powered developer error analyzer using **Python, FastAPI, LLM, and RAG**.

The goal is to help developers understand application errors by turning raw logs and stack traces into a structured diagnosis with likely root causes and suggested fixes.

## Current Features

- Parse common Python, JavaScript/TypeScript, and C# stack traces
- Deterministically classify common error categories
- Analyze parsed errors with an OpenRouter-compatible LLM
- Return structured diagnosis data through a REST API
- Keep API credentials in environment variables
- Automated parser and API tests
- Docker-ready application

## API

Start the development server:

```bash
uvicorn app.main:app --reload
```

Health check:

```text
GET /health
```

Parse an error without using an LLM:

```text
POST /api/v1/parse
```

Analyze an error with an LLM:

```text
POST /api/v1/analyze
```

Example request:

```json
{
  "raw_log": "Traceback (most recent call last):\n  File \"app/player.py\", line 42, in update\n    self.camera.transform.position\nAttributeError: 'NoneType' object has no attribute 'transform'"
}
```

Example analysis shape:

```json
{
  "category": "null_reference",
  "summary": "The application attempted to access a member on a null object.",
  "root_cause": "The camera reference is likely not initialized before update().",
  "suggested_fix": "Initialize and validate the camera reference before accessing transform.",
  "confidence": 0.87
}
```

## Configuration

Copy `.env.example` to `.env` and provide an OpenRouter API key:

```text
OPENROUTER_API_KEY=your_api_key_here
OPENROUTER_MODEL=deepseek/deepseek-chat
```

Never commit `.env` or real API keys.

## Architecture

```text
Raw Error Log
      |
      v
Parser / Normalizer
      |
      v
Deterministic Classifier
      |
      +--------------------+
      |                    |
      v                    v
 Structured Error       RAG Retrieval
      |                    |
      +---------+----------+
                v
             LLM
                |
                v
      Structured Diagnosis
                |
                v
             REST API
```

## Roadmap

- [x] FastAPI foundation
- [x] Structured error models
- [x] Error parser and classifier
- [x] OpenRouter LLM integration
- [x] `/api/v1/analyze` endpoint
- [ ] Knowledge base ingestion
- [ ] Embeddings and vector search
- [ ] RAG-enhanced diagnosis
- [ ] Web UI
- [ ] GitHub Actions CI
- [ ] Production deployment

## Tech Stack

- Python 3.12+
- FastAPI
- Pydantic
- OpenRouter-compatible LLM API
- RAG / vector search (planned)
- Pytest
- Docker
- GitHub Actions (planned)

## License

MIT
