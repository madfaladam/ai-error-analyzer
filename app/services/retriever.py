from dataclasses import dataclass
from pathlib import Path

from app.models.error import ErrorCategory


@dataclass(frozen=True)
class KnowledgeDocument:
    path: str
    content: str
    score: int


class KnowledgeRetriever:
    """Simple deterministic retriever used as the first RAG implementation.

    It deliberately avoids a heavyweight vector database for the MVP. The
    interface can later be backed by embeddings/vector search without changing
    the API layer.
    """

    def __init__(self, knowledge_dir: str = "knowledge") -> None:
        self.knowledge_dir = Path(knowledge_dir)

    def retrieve(
        self,
        query: str,
        category: ErrorCategory,
        top_k: int = 3,
    ) -> list[KnowledgeDocument]:
        if not self.knowledge_dir.exists():
            return []

        query_terms = set(query.lower().split())
        category_terms = set(category.value.replace("_", " ").split())
        documents: list[KnowledgeDocument] = []

        for path in self.knowledge_dir.rglob("*.md"):
            content = path.read_text(encoding="utf-8")
            haystack = content.lower()
            score = sum(1 for term in query_terms if term and term in haystack)
            score += sum(2 for term in category_terms if term and term in haystack)

            if score > 0:
                documents.append(
                    KnowledgeDocument(
                        path=str(path),
                        content=content,
                        score=score,
                    )
                )

        return sorted(documents, key=lambda item: item.score, reverse=True)[:top_k]
