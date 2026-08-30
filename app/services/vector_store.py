from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Document:
    id: str
    content: str
    source: str
    metadata: dict[str, str]


class VectorStore:
    """Small in-memory vector store using cosine similarity."""

    def __init__(self) -> None:
        self._documents: list[Document] = []
        self._vectors: np.ndarray | None = None

    def add(self, documents: list[Document], vectors: list[list[float]]) -> None:
        if len(documents) != len(vectors):
            raise ValueError("Documents and vectors must have the same length")

        self._documents.extend(documents)
        matrix = np.asarray(vectors, dtype=np.float32)
        self._vectors = matrix if self._vectors is None else np.vstack([self._vectors, matrix])

    def search(self, query_vector: list[float], top_k: int = 3) -> list[tuple[Document, float]]:
        if not self._documents or self._vectors is None:
            return []

        query = np.asarray(query_vector, dtype=np.float32)
        scores = self._vectors @ query
        indices = np.argsort(scores)[::-1][:top_k]

        return [(self._documents[i], float(scores[i])) for i in indices]
