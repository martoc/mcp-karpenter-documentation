# Usage Guide

This guide provides detailed instructions for using the MCP Karpenter Documentation Server.

## Installation

### Prerequisites

- Python 3.12 or later
- [uv](https://github.com/astral-sh/uv) package manager
- Docker (optional, for containerised deployment)

### Local Installation

```bash
# Clone the repository
git clone https://github.com/martoc/mcp-karpenter-documentation.git
cd mcp-karpenter-documentation

# Initialise the environment
make init

# Build the documentation index
make index
```

## Configuration

### MCP Client Configuration

#### Claude Code

Add to your project's `.mcp.json` or global `~/.mcp.json`:

```json
{
  "mcpServers": {
    "karpenter-documentation": {
      "command": "uv",
      "args": ["run", "mcp-karpenter-documentation"],
      "cwd": "/Users/martoc/Developer/github.com/martoc/mcp-karpenter-documentation"
    }
  }
}
```

#### Docker Configuration

For production use, use the Docker image:

```json
{
  "mcpServers": {
    "karpenter-documentation": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "mcp-karpenter-documentation"]
    }
  }
}
```

## Using the Tools

### search_documentation

Search Karpenter documentation using full-text search.

**Parameters:**
- `query` (string, required): Search terms
- `section` (string, optional): Filter by section
- `limit` (integer, optional): Maximum results (default: 10, max: 50)

**Example:**
```json
{
  "query": "node provisioning",
  "section": "docs",
  "limit": 5
}
```

**Response:**
```json
{
  "query": "node provisioning",
  "section_filter": "docs",
  "result_count": 5,
  "results": [
    {
      "title": "Provisioning",
      "url": "https://karpenter.sh/docs/concepts/provisioning",
      "path": "docs/concepts/provisioning.md",
      "section": "docs",
      "snippet": "...Karpenter <mark>provisions</mark> <mark>nodes</mark> in response to...",
      "relevance_score": 2.3456
    }
  ]
}
```

### read_documentation

Read the full content of a specific documentation page.

**Parameters:**
- `path` (string, required): Relative path to the document

**Example:**
```json
{
  "path": "docs/concepts/provisioning.md"
}
```

**Response:**
```json
{
  "path": "docs/concepts/provisioning.md",
  "title": "Provisioning",
  "description": "Learn how Karpenter provisions nodes",
  "section": "docs",
  "url": "https://karpenter.sh/docs/concepts/provisioning",
  "content": "# Provisioning\n\nKarpenter provisions nodes..."
}
```

## Indexing

### Index from Git

```bash
# Index from the main branch
uv run karpenter-docs-index index

# Index from a specific branch
uv run karpenter-docs-index index --branch v0.34.0

# Rebuild the index (clear and reindex)
uv run karpenter-docs-index index --rebuild
```

### Index from Local Path

```bash
uv run python -c "
from pathlib import Path
from mcp_karpenter_documentation.database import DocumentDatabase
from mcp_karpenter_documentation.indexer import KarpenterDocsIndexer

db = DocumentDatabase(Path('data/karpenter_docs.db'))
indexer = KarpenterDocsIndexer(db)
count = indexer.index_from_path(Path('/path/to/karpenter-provider-aws/website'))
print(f'Indexed {count} documents')
"
```

### View Statistics

```bash
uv run karpenter-docs-index stats
```

## Docker Deployment

### Building the Image

```bash
# Build the image
make docker-build

# Tag for Docker Hub (optional)
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:latest
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:v0.1.0
```

The Docker build process:
1. Installs dependencies
2. Clones the Karpenter repository
3. Builds the documentation index
4. Packages everything into the image

### Running the Container

```bash
# Interactive mode (for testing)
make docker-run

# As an MCP server (locally built)
docker run -i --rm mcp-karpenter-documentation

# As an MCP server (from Docker Hub)
docker run -i --rm martoc/mcp-karpenter-documentation:latest
```

### Publishing to Docker Hub

```bash
# Build the image
make docker-build

# Tag the image
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:latest
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:v0.1.0

# Push to Docker Hub
docker push martoc/mcp-karpenter-documentation:latest
docker push martoc/mcp-karpenter-documentation:v0.1.0
```

## Development

### Running Tests

```bash
# Run all tests
make test

# Run with coverage
make test

# Run specific test file
uv run pytest tests/test_database.py
```

### Code Quality

```bash
# Format code
make format

# Run linter
make lint

# Run type checker
make typecheck

# Run full build
make build
```

## Troubleshooting

### Database Not Found

If you get a "Database not found" error:

```bash
# Build the index
make index
```

### Git Clone Failures

If the indexer fails to clone the repository:

1. Check your internet connection
2. Verify Git is installed: `git --version`
3. Try cloning manually: `git clone https://github.com/aws/karpenter-provider-aws.git`

### Empty Search Results

If searches return no results:

1. Verify the index is built: `uv run karpenter-docs-index stats`
2. Rebuild the index: `uv run karpenter-docs-index index --rebuild`
3. Try broader search terms

## Performance

### Index Size

- Typical index size: ~10-15 MB
- Index time: ~30-60 seconds
- Documents indexed: ~180-200

### Search Performance

- Average search time: <10ms
- Full-text search with BM25 ranking
- Porter stemming for fuzzy matching

## Advanced Usage

### Custom Database Location

```bash
uv run karpenter-docs-index index --database /custom/path/docs.db
```

### Environment Variables

```bash
# Set custom database path
export KARPENTER_DOCS_DB=/path/to/custom.db

# Run server
uv run mcp-karpenter-documentation
```

## Contributing

See [CODESTYLE.md](CODESTYLE.md) for code style guidelines and [CLAUDE.md](CLAUDE.md) for AI assistant instructions.
