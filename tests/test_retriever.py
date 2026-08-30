from app.models.error import ErrorCategory
from app.services.retriever import KnowledgeRetriever


def test_retriever_finds_null_reference_knowledge() -> None:
    retriever = KnowledgeRetriever("knowledge")

    results = retriever.retrieve(
        "AttributeError NoneType transform",
        ErrorCategory.NULL_REFERENCE,
    )

    assert results
    assert results[0].path.endswith("python/null-reference.md")
