"""Tests for document parser."""

import tempfile
from pathlib import Path

from mcp_karpenter_documentation.parser import DocumentParser


def test_parse_file_with_frontmatter() -> None:
    """Test parsing a markdown file with frontmatter."""
    parser = DocumentParser()

    content = """---
title: Test Document
description: This is a test
---

# Test Content

This is the main content.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        file_path = base_path / "docs" / "test.md"
        file_path.parent.mkdir(parents=True)
        file_path.write_text(content)

        doc = parser.parse_file(file_path, base_path)

        assert doc is not None
        assert doc.title == "Test Document"
        assert doc.description == "This is a test"
        assert doc.section == "docs"
        assert "Test Content" in doc.content


def test_parse_file_without_frontmatter() -> None:
    """Test parsing a markdown file without frontmatter."""
    parser = DocumentParser()

    content = """# Test Document

This is content without frontmatter.
"""

    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = Path(temp_dir)
        file_path = base_path / "test-doc.md"
        file_path.write_text(content)

        doc = parser.parse_file(file_path, base_path)

        assert doc is not None
        assert doc.title == "Test Doc"  # Generated from filename
        assert doc.description is None


def test_url_computation() -> None:
    """Test URL computation for documentation pages."""
    parser = DocumentParser()

    # Test standard doc path
    path = Path("docs/concepts/scheduling.md")
    url = parser._compute_url(path)
    assert url == "https://karpenter.sh/docs/concepts/scheduling"

    # Test with content/en/docs prefix (Hugo pattern)
    path = Path("content/en/docs/guides/deprovisioning.md")
    url = parser._compute_url(path)
    assert "karpenter.sh" in url


def test_clean_content() -> None:
    """Test content cleaning."""
    parser = DocumentParser()

    content = """
    {{< hint info >}}
    This is a Hugo shortcode
    {{< /hint >}}

    <!-- HTML comment -->

    <div>HTML tags</div>

    Regular content
    """

    cleaned = parser._clean_content(content)

    assert "{{<" not in cleaned
    assert "<!--" not in cleaned
    assert "<div>" not in cleaned
    assert "Regular content" in cleaned
