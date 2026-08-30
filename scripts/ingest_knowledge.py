from pathlib import Path

from app.services.chunker import chunk_markdown
from app.services.chroma_store import ChromaVectorStore
from app.services.embeddings import get_embedding_service


ROOT = Path("knowledge")


def main() -> None:
    chunks = []
    for path in sorted(ROOT.rglob("*.md")):
        chunks.extend(chunk_markdown(path.read_text(encoding="utf-8"), str(path)))

    embeddings = get_embedding_service().encode([chunk.content for chunk in chunks])
    ChromaVectorStore().upsert(chunks, embeddings)
    print(f"Indexed {len(chunks)} chunks into ChromaDB.")


if __name__ == "__main__":
    main()
