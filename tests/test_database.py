"""Tests for database operations."""

import tempfile
from collections.abc import Iterator
from pathlib import Path

import pytest

from mcp_karpenter_documentation.database import DocumentDatabase
from mcp_karpenter_documentation.models import Document


@pytest.fixture
def temp_db() -> Iterator[DocumentDatabase]:
    """Create a temporary database for testing."""
    with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
        db_path = Path(f.name)
    db = DocumentDatabase(db_path)
    yield db
    db_path.unlink()


def test_upsert_document(temp_db: DocumentDatabase) -> None:
    """Test document insertion and update."""
    doc = Document(
        path="docs/test.md",
        title="Test Document",
        description="A test document",
        section="docs",
        content="This is test content",
        url="https://karpenter.sh/docs/test",
    )

    temp_db.upsert_document(doc)
    retrieved = temp_db.get_document("docs/test.md")

    assert retrieved is not None
    assert retrieved.title == "Test Document"
    assert retrieved.content == "This is test content"


def test_search_documents(temp_db: DocumentDatabase) -> None:
    """Test full-text search."""
    doc1 = Document(
        path="docs/scaling.md",
        title="Scaling Guide",
        description="How to scale with Karpenter",
        section="docs",
        content="Karpenter automatically scales your Kubernetes cluster",
        url="https://karpenter.sh/docs/scaling",
    )
    doc2 = Document(
        path="docs/provisioning.md",
        title="Provisioning",
        description="Node provisioning",
        section="docs",
        content="Karpenter provisions nodes based on pending pods",
        url="https://karpenter.sh/docs/provisioning",
    )

    temp_db.upsert_document(doc1)
    temp_db.upsert_document(doc2)

    results = temp_db.search("scale")
    assert len(results) > 0
    assert results[0].title == "Scaling Guide"


def test_get_document_count(temp_db: DocumentDatabase) -> None:
    """Test document count."""
    assert temp_db.get_document_count() == 0

    doc = Document(
        path="docs/test.md",
        title="Test",
        description=None,
        section="docs",
        content="Content",
        url="https://karpenter.sh/docs/test",
    )
    temp_db.upsert_document(doc)

    assert temp_db.get_document_count() == 1


def test_clear_database(temp_db: DocumentDatabase) -> None:
    """Test clearing all documents."""
    doc = Document(
        path="docs/test.md",
        title="Test",
        description=None,
        section="docs",
        content="Content",
        url="https://karpenter.sh/docs/test",
    )
    temp_db.upsert_document(doc)
    assert temp_db.get_document_count() == 1

    temp_db.clear()
    assert temp_db.get_document_count() == 0
