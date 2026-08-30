from pathlib import Path

import chromadb

from app.services.chunker import TextChunk


class ChromaVectorStore:
    """Persistent vector store backed by ChromaDB."""

    def __init__(self, path: str = "vector_store", collection_name: str = "error_knowledge") -> None:
        Path(path).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert(self, chunks: list[TextChunk], embeddings: list[list[float]]) -> None:
        if not chunks:
            return
        self.collection.upsert(
            ids=[chunk.id for chunk in chunks],
            documents=[chunk.content for chunk in chunks],
            embeddings=embeddings,
            metadatas=[chunk.metadata for chunk in chunks],
        )

    def search(self, query_embedding: list[float], top_k: int = 3) -> list[tuple[str, str, float]]:
        result = self.collection.query(query_embeddings=[query_embedding], n_results=top_k)
        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        distances = result.get("distances", [[]])[0]

        # Chroma cosine distance is 0 for identical vectors; convert to a
        # bounded similarity score for the public API.
        return [
            (doc_id, document, max(-1.0, min(1.0, 1.0 - float(distance))))
            for doc_id, document, distance in zip(ids, documents, distances)
        ]
