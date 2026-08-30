from app.services.chunker import chunk_markdown


def test_chunk_markdown_preserves_paragraphs() -> None:
    content = "# Error\n\nFirst paragraph.\n\nSecond paragraph."

    chunks = chunk_markdown(content, "knowledge/test.md", max_chars=30)

    assert len(chunks) == 2
    assert chunks[0].id == "knowledge/test.md#0"
    assert "First paragraph" in chunks[0].content
