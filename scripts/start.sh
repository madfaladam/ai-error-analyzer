#!/bin/sh
set -eu

if [ "${SKIP_KNOWLEDGE_INGEST:-false}" != "true" ]; then
  python scripts/ingest_knowledge.py
fi

exec uvicorn app.main:app --host 0.0.0.0 --port "${PORT:-8000}"
