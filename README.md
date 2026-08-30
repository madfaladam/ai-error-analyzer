# AI Error Analyzer

AI-powered developer error analyzer using **LLM, RAG, and FastAPI**.

The goal is to help developers understand application errors by turning raw logs and stack traces into a structured diagnosis with likely root causes and suggested fixes.

## Project Goals

- Parse and normalize developer error logs
- Classify common error types
- Analyze errors with an LLM
- Retrieve relevant technical knowledge using RAG
- Return structured, actionable recommendations
- Expose the analyzer through a REST API
- Add automated tests, Docker support, and CI

## Planned Architecture

```text
Error Log
   |
   v
Parser / Normalizer
   |
   v
Error Classification
   |
   +------> Knowledge Retrieval (RAG)
   |                    |
   +--------------------+
                        v
                   LLM Analysis
                        |
                        v
              Structured Diagnosis
                        |
                        v
                   REST API / UI
```

## Tech Stack

- Python
- FastAPI
- Pydantic
- OpenRouter-compatible LLM API
- RAG / vector search
- Pytest
- Docker
- GitHub Actions

## Status

🚧 Phase 1 — project foundation in progress.

## License

MIT
