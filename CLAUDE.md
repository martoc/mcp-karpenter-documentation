# Claude Code Instructions

This document provides instructions for Claude Code when working with the MCP Karpenter Documentation Server project.

## Project Overview

This is a Python-based MCP (Model Context Protocol) server that provides search and retrieval tools for AWS Karpenter documentation. The server:

- Clones the aws/karpenter-provider-aws repository
- Indexes markdown documentation from the `website/` directory
- Provides full-text search using SQLite FTS5
- Exposes two MCP tools: `search_documentation` and `read_documentation`

## Development Workflow

### Initialisation

When starting work on this project:

```bash
make init       # Install dependencies and set up environment
make index      # Build the documentation index
```

### Making Changes

1. Make your code changes
2. Run `make format` to format the code
3. Run `make build` to validate (lint, typecheck, test)
4. Test the changes locally

### Testing

```bash
make test       # Run all tests with coverage
make lint       # Run linter only
make typecheck  # Run type checker only
```

### Running the Server

```bash
make run        # Run the MCP server locally
```

## Code Style Requirements

### Language

- Use **British English** throughout:
  - "initialise" not "initialize"
  - "colour" not "color"
  - "organise" not "organize"

### Type Hints

All functions must have type hints:

```python
def search(self, query: str, section: str | None = None) -> list[SearchResult]:
    ...
```

### Docstrings

Use Google-style docstrings:

```python
def parse_file(self, file_path: Path, base_path: Path) -> Document | None:
    """Parse a markdown file and extract metadata and content.

    Args:
        file_path: Path to the markdown file.
        base_path: Base path of the documentation directory.

    Returns:
        Document instance or None if parsing fails.
    """
```

### Error Handling

Prefer explicit error handling:

```python
try:
    result = risky_operation()
    return result
except Exception:
    return None
```

## Project Structure

```
mcp-karpenter-documentation/
├── src/mcp_karpenter_documentation/
│   ├── __init__.py          # Package info
│   ├── models.py            # Data models (Document, SearchResult)
│   ├── database.py          # SQLite FTS5 operations
│   ├── parser.py            # Markdown parsing with frontmatter
│   ├── indexer.py           # Git clone and indexing logic
│   ├── server.py            # FastMCP server with tools
│   └── cli.py               # Command-line interface
├── tests/
│   ├── test_database.py     # Database tests
│   └── test_parser.py       # Parser tests
├── data/                    # SQLite database storage
├── pyproject.toml           # Project configuration
├── Makefile                 # Build automation
├── Dockerfile               # Container image
└── README.md                # Project documentation
```

## Key Components

### Models (models.py)

- `DocumentMetadata`: Frontmatter metadata
- `Document`: Full document with content
- `SearchResult`: Search result with snippet and score

### Database (database.py)

- `DocumentDatabase`: SQLite FTS5 wrapper
- Full-text search with BM25 ranking
- Porter stemming for fuzzy matching

### Parser (parser.py)

- `DocumentParser`: Markdown parser
- Extracts YAML frontmatter
- Cleans Hugo shortcodes and HTML
- Computes karpenter.sh URLs

### Indexer (indexer.py)

- `KarpenterDocsIndexer`: Git clone and indexing
- Sparse checkout for efficiency
- Indexes from main branch by default

### Server (server.py)

- FastMCP server with two tools:
  - `search_documentation`: Full-text search
  - `read_documentation`: Retrieve full content

### CLI (cli.py)

- `index`: Build/rebuild index
- `stats`: Show document count

## Common Tasks

### Adding a New Feature

1. Update the relevant module (e.g., `server.py` for new tools)
2. Add type hints and docstrings
3. Write tests in `tests/`
4. Run `make build` to verify
5. Update documentation

### Fixing a Bug

1. Add a test that reproduces the bug
2. Fix the bug in the source code
3. Verify the test passes
4. Run `make build` to ensure no regressions

### Updating Dependencies

1. Edit `pyproject.toml`
2. Run `make generate` to update `uv.lock`
3. Run `make init` to install
4. Test the changes

### Changing the Indexer

When modifying `indexer.py`:

- Remember to update `KARPENTER_REPO` and `DOCS_PATH` if needed
- Test with `make index`
- Check `uv run karpenter-docs-index stats` after indexing

### Modifying Search Behaviour

When changing search in `database.py`:

- FTS5 queries use MATCH syntax
- BM25 weights: (5.0 for title, 2.0 for description, 1.0 for content)
- Test with different queries to ensure relevance

## Testing Guidelines

### Writing Tests

```python
def test_feature_name(temp_db: DocumentDatabase) -> None:
    """Test description in British English."""
    # Arrange
    doc = Document(...)

    # Act
    temp_db.upsert_document(doc)

    # Assert
    assert temp_db.get_document_count() == 1
```

### Test Coverage

- Aim for >90% coverage on core modules
- 100% coverage on models and database operations
- CLI and server may have lower coverage (integration tests)

### Running Specific Tests

```bash
# Run a single test file
uv run pytest tests/test_database.py

# Run a specific test
uv run pytest tests/test_database.py::test_search_documents

# Run with verbose output
uv run pytest -vv
```

## Docker

### Building

```bash
make docker-build
```

The Dockerfile:
1. Installs git and uv
2. Copies project files
3. Installs dependencies
4. Builds the index at build time
5. Runs the server

### Testing Docker

```bash
make docker-run
```

### Publishing to Docker Hub

```bash
# Build and tag
make docker-build
make docker-tag

# Push to registry
make docker-push
```

The image is published as `martoc/mcp-karpenter-documentation` on Docker Hub with both `latest` and version-specific tags.

## Git Workflow

### Commit Messages

Use Conventional Commits format:

```
feat: add section filtering to search
fix: correct URL computation for nested paths
docs: update README with Docker instructions
test: add tests for parser edge cases
refactor: simplify database connection handling
```

### Before Committing

Always run:

```bash
make build
```

This runs:
1. Clean (remove build artefacts)
2. Lint (Ruff)
3. Type check (mypy)
4. Test (pytest with coverage)

## Troubleshooting

### Import Errors

If you see import errors:

```bash
make init       # Reinstall dependencies
```

### Test Failures

```bash
make clean      # Clean build artefacts
make test       # Run tests again
```

### Index Issues

```bash
uv run karpenter-docs-index index --rebuild
```

### Type Check Failures

- Ensure all functions have type hints
- Use `str | None` not `Optional[str]`
- Generator fixtures need `Iterator` type hint

## Performance Tips

### Indexing

- Uses sparse checkout to fetch only `website/` directory
- Shallow clone with `--depth 1`
- Processes ~180-200 markdown files

### Search

- FTS5 is very fast (<10ms per query)
- BM25 ranking for relevance
- Porter stemming for fuzzy matching

### Database

- SQLite with FTS5 virtual table
- Typical size: 10-15 MB
- In-memory processing for speed

## Security Considerations

### SQL Injection

Always use parameterised queries:

```python
# Good
conn.execute("SELECT * FROM documents WHERE path = ?", (path,))

# Never
conn.execute(f"SELECT * FROM documents WHERE path = '{path}'")
```

### File System Access

- Use `Path` objects for file operations
- Validate paths relative to base directory
- Don't trust user-supplied paths

### Subprocess Calls

- Use list format, not shell strings
- Set `check=True` to handle errors
- Avoid shell=True

```python
# Good
subprocess.run(["git", "clone", url], check=True)

# Avoid
subprocess.run(f"git clone {url}", shell=True)
```

## Documentation Standards

### README Files

- Use British English
- Include examples
- Keep up to date with code

### Code Comments

- Explain "why" not "what"
- Use British English
- Keep concise

### API Documentation

- Document all public functions
- Include parameter types and descriptions
- Provide usage examples

## MCP Integration

### Configuration

The server is configured in `.mcp.json`:

```json
{
  "mcpServers": {
    "karpenter-documentation": {
      "command": "uv",
      "args": ["run", "mcp-karpenter-documentation"]
    }
  }
}
```

### Testing Tools

You can test the MCP tools using Claude Code or any MCP client.

## Maintenance

### Regular Tasks

- Update dependencies quarterly
- Rebuild index when Karpenter releases new versions
- Run `make build` before each commit
- Keep documentation in sync with code

### Version Updates

1. Update version in `src/mcp_karpenter_documentation/__init__.py`
2. Update version in `pyproject.toml`
3. Tag the release
4. Build and push Docker image

## Questions and Support

For questions about:
- MCP protocol: See https://modelcontextprotocol.io/
- Karpenter: See https://karpenter.sh/
- FastMCP: See https://github.com/jlowin/fastmcp
- uv: See https://github.com/astral-sh/uv

## Summary for Claude

When working on this project:

1. **Always use British English** in code and docs
2. **Run `make build`** before committing
3. **Add type hints** to all functions
4. **Write tests** for new features
5. **Use parameterised SQL queries**
6. **Follow PEP 8** and Google-style docstrings
7. **Test with `make index` and `make run`** after changes

The project is well-structured, follows modern Python practices, and uses uv for fast dependency management. Focus on maintaining code quality and documentation accuracy.
