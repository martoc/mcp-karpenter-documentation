# Code Style Guide

This document outlines the code style and conventions used in the MCP Karpenter Documentation Server project.

## Python Style

We follow **PEP 8** guidelines with some specific conventions:

### Language

- Use **British English** for all code, comments, and documentation
- Examples: "initialise" not "initialize", "colour" not "color"

### Imports

```python
# Standard library imports first
import json
import logging
from pathlib import Path

# Third-party imports
from fastmcp import FastMCP
import frontmatter

# Local imports
from mcp_karpenter_documentation.database import DocumentDatabase
from mcp_karpenter_documentation.models import Document
```

### Type Hints

All functions and methods must include type hints:

```python
def search(self, query: str, section: str | None = None, limit: int = 10) -> list[SearchResult]:
    """Search documents using FTS5."""
    ...
```

### Docstrings

We use **Google-style docstrings**:

```python
def parse_file(self, file_path: Path, base_path: Path) -> Document | None:
    """Parse a markdown file and extract metadata and content.

    Args:
        file_path: Path to the markdown file.
        base_path: Base path of the documentation directory.

    Returns:
        Document instance or None if parsing fails.
    """
    ...
```

## Code Organisation

### Module Structure

```
src/mcp_karpenter_documentation/
├── __init__.py          # Package initialisation
├── models.py            # Data models
├── database.py          # Database operations
├── parser.py            # Document parsing
├── indexer.py           # Documentation indexing
├── server.py            # MCP server
└── cli.py               # Command-line interface
```

### File Naming

- Python files: `snake_case.py`
- Test files: `test_*.py`
- Configuration files: `lowercase.ext`

### Class Naming

```python
class DocumentDatabase:          # PascalCase for classes
    def get_document(self):      # snake_case for methods
        pass

def search_documentation():      # snake_case for functions
    pass

CONSTANT_VALUE = "value"         # UPPER_CASE for constants
```

## Error Handling

### Explicit Error Handling

Prefer explicit error handling over silent failures:

```python
# Good
def parse_file(self, file_path: Path) -> Document | None:
    try:
        post = frontmatter.load(file_path)
        return self._process_document(post)
    except Exception:
        return None

# Avoid
def parse_file(self, file_path: Path) -> Document:
    post = frontmatter.load(file_path)  # May raise exception
    return self._process_document(post)
```

### Return Types

Use `Optional[T]` or `T | None` for functions that may not return a value:

```python
def get_document(self, path: str) -> Document | None:
    """Retrieve a document by path."""
    cursor = conn.execute("SELECT * FROM documents WHERE path = ?", (path,))
    row = cursor.fetchone()
    return Document(...) if row else None
```

## Testing

### Test Organisation

```python
# tests/test_database.py
import pytest
from mcp_karpenter_documentation.database import DocumentDatabase


@pytest.fixture
def temp_db() -> Iterator[DocumentDatabase]:
    """Create a temporary database for testing."""
    ...


def test_search_documents(temp_db: DocumentDatabase) -> None:
    """Test full-text search."""
    ...
```

### Test Naming

- Test files: `test_<module>.py`
- Test functions: `test_<functionality>`
- Use descriptive names that explain what is being tested

### Assertions

```python
# Good
assert retrieved is not None
assert retrieved.title == "Expected Title"
assert len(results) > 0

# Avoid magic numbers
assert retrieved.score > 0.0  # Not: assert retrieved.score > 0.5
```

## Documentation

### Comments

- Write comments for complex logic
- Avoid obvious comments
- Use British English

```python
# Good
# Remove Hugo shortcodes from content
content = re.sub(r"\{\{<.*?>\}\}", "", content)

# Avoid
# This removes shortcodes
content = re.sub(r"\{\{<.*?>\}\}", "", content)
```

### README Files

- Use markdown format
- Include usage examples
- Keep documentation up to date with code changes

## Database Operations

### Context Managers

Always use context managers for database connections:

```python
@contextmanager
def _get_connection(self) -> Generator[sqlite3.Connection, None, None]:
    conn = sqlite3.connect(self.db_path)
    try:
        yield conn
    finally:
        conn.close()
```

### Parameterised Queries

Always use parameterised queries to prevent SQL injection:

```python
# Good
cursor = conn.execute("SELECT * FROM documents WHERE path = ?", (path,))

# Never
cursor = conn.execute(f"SELECT * FROM documents WHERE path = '{path}'")
```

## Git Workflow

### Commit Messages

Follow [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: add support for custom database paths
fix: correct URL computation for Hugo docs
docs: update usage examples in README
test: add tests for parser edge cases
refactor: simplify database connection handling
```

### Branch Naming

- `feature/description` - New features
- `bugfix/description` - Bug fixes
- `docs/description` - Documentation changes
- `refactor/description` - Code refactoring

## Tools and Automation

### Code Formatting

```bash
# Format code with Ruff
make format
```

### Linting

```bash
# Run Ruff linter
make lint
```

### Type Checking

```bash
# Run mypy
make typecheck
```

### Running Tests

```bash
# Run pytest with coverage
make test
```

### Full Build

```bash
# Run all checks
make build
```

## Dependencies

### Adding Dependencies

1. Add to `pyproject.toml`
2. Run `make generate` to update `uv.lock`
3. Run `make init` to install

### Version Pinning

- Use version ranges for flexibility: `>=2.0.0,<3.0.0`
- Pin major versions to avoid breaking changes
- Keep dependencies up to date

## Performance Considerations

### Database Queries

- Use FTS5 for full-text search
- Add indexes for frequently queried columns
- Use BM25 ranking for relevance scoring

### Memory Usage

- Use generators for large result sets
- Clean up temporary files and directories
- Close database connections properly

### Indexing Performance

- Use shallow git clones with sparse checkout
- Index only markdown files
- Batch database operations

## Security

### SQL Injection

Always use parameterised queries:

```python
conn.execute("SELECT * FROM documents WHERE path = ?", (path,))
```

### File System Access

Validate paths and use Path objects:

```python
def parse_file(self, file_path: Path, base_path: Path) -> Document | None:
    # Ensure file is within base_path
    relative_path = file_path.relative_to(base_path)
    ...
```

### Subprocess Execution

Use explicit arguments, avoid shell injection:

```python
# Good
subprocess.run(["git", "clone", "--depth", "1", repo_url], check=True)

# Avoid
subprocess.run(f"git clone {repo_url}", shell=True)
```

## Maintenance

### Regular Tasks

- Update dependencies: `make generate`
- Run tests: `make test`
- Rebuild index: `uv run karpenter-docs-index index --rebuild`
- Check for security vulnerabilities
- Review and update documentation

### Code Reviews

- Check for type hints
- Verify test coverage
- Ensure British English usage
- Validate documentation
- Test locally before committing
