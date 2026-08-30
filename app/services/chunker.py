from dataclasses import dataclass


@dataclass(frozen=True)
class TextChunk:
    id: str
    content: str
    metadata: dict[str, str]


def chunk_markdown(content: str, source: str, max_chars: int = 1200) -> list[TextChunk]:
    """Split markdown into bounded chunks while preserving paragraph boundaries."""
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    chunks: list[TextChunk] = []
    current: list[str] = []
    size = 0

    for paragraph in paragraphs:
        if current and size + len(paragraph) + 2 > max_chars:
            chunks.append(
                TextChunk(
                    id=f"{source}#{len(chunks)}",
                    content="\n\n".join(current),
                    metadata={"source": source},
                )
            )
            current = []
            size = 0
        current.append(paragraph)
        size += len(paragraph) + 2

    if current:
        chunks.append(
            TextChunk(
                id=f"{source}#{len(chunks)}",
                content="\n\n".join(current),
                metadata={"source": source},
            )
        )

    return chunks
