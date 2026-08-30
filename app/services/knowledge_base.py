from pathlib import Path

from app.services.embeddings import EmbeddingService, get_embedding_service
from app.services.vector_store import Document, VectorStore


class KnowledgeBase:
    def __init__(self, root: str = "knowledge", embedding_service: EmbeddingService | None = None) -> None:
        self.root = Path(root)
        self.embedding_service = embedding_service or get_embedding_service()
        self.store = VectorStore()
        self._loaded = False

    def load(self) -> None:
        if self._loaded:
            return

        documents: list[Document] = []
        for path in sorted(self.root.rglob("*.md")):
            content = path.read_text(encoding="utf-8")
            documents.append(
                Document(
                    id=str(path.relative_to(self.root)),
                    content=content,
                    source=str(path),
                    metadata={"language": path.parent.name},
                )
            )

        if documents:
            vectors = self.embedding_service.encode([doc.content for doc in documents])
            self.store.add(documents, vectors)

        self._loaded = True

    def search(self, query: str, top_k: int = 3) -> list[tuple[Document, float]]:
        self.load()
        query_vector = self.embedding_service.encode([query])[0]
        return self.store.search(query_vector, top_k=top_k)


_knowledge_base: KnowledgeBase | None = None


def get_knowledge_base() -> KnowledgeBase:
    global _knowledge_base
    if _knowledge_base is None:
        _knowledge_base = KnowledgeBase()
    return _knowledge_base
