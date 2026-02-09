[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP](https://img.shields.io/badge/MCP-Model%20Context%20Protocol-green.svg)](https://modelcontextprotocol.io/)
[![Docker Build](https://github.com/martoc/mcp-karpenter-documentation/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/martoc/mcp-karpenter-documentation/actions/workflows/docker-publish.yml)
[![Docker Hub](https://img.shields.io/docker/pulls/martoc/mcp-karpenter-documentation)](https://hub.docker.com/r/martoc/mcp-karpenter-documentation)

# MCP Karpenter Documentation Server

An MCP (Model Context Protocol) server that provides search and retrieval tools for [AWS Karpenter](https://karpenter.sh) documentation. This server enables AI assistants like Claude to search and read Karpenter documentation directly.

## Features

- **Full-text search** using SQLite FTS5 with BM25 ranking and Porter stemming
- **Section filtering** to narrow search results by documentation category
- **Sparse checkout** for efficient cloning of only the website directory from aws/karpenter-provider-aws
- **Docker support** for portable deployment across projects
- **STDIO transport** for seamless MCP client integration

## Quick Start

### Using Docker (Recommended)

```bash
# Pull from Docker Hub (easiest)
docker pull martoc/mcp-karpenter-documentation:latest

# Or build locally (includes pre-indexed documentation)
make docker-build

# Test the server
make docker-run
```

### Using uv (Local Development)

```bash
# Initialise the environment
make init

# Build the documentation index
make index

# Run the server
make run
```

## Configuration

### Claude Code / Claude Desktop

Add to your `.mcp.json` or global settings:

```json
{
  "mcpServers": {
    "karpenter-documentation": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "martoc/mcp-karpenter-documentation:latest"]
    }
  }
}
```

For a locally built Docker image:

```json
{
  "mcpServers": {
    "karpenter-documentation": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "martoc/mcp-karpenter-documentation"]
    }
  }
}
```

For local development without Docker:

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

## MCP Tools

| Tool | Description |
|------|-------------|
| `search_documentation` | Search Karpenter documentation by keyword query with optional section filtering |
| `read_documentation` | Retrieve the full content of a specific documentation page |

### search_documentation

Search AWS Karpenter documentation using full-text search with stemming support.

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `query` | string | Yes | - | Search terms (supports stemming) |
| `section` | string | No | None | Filter by section (e.g., docs, guides, concepts) |
| `limit` | integer | No | 10 | Maximum results (1-50) |

**Common Sections:** `docs`, `guides`, `concepts`, `reference`, `troubleshooting`, `faq`

### read_documentation

Retrieve the full content of a documentation page.

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `path` | string | Yes | Relative path to document (from search results) |

## CLI Commands

```bash
# Build/rebuild the documentation index
uv run karpenter-docs-index index
uv run karpenter-docs-index index --rebuild
uv run karpenter-docs-index index --branch main

# Show index statistics
uv run karpenter-docs-index stats
```

## Development

```bash
make init         # Initialise development environment
make build        # Run full build (lint, typecheck, test)
make test         # Run tests with coverage
make format       # Format code
make lint         # Run linter
make typecheck    # Run type checker
make docker-build # Build Docker image
make docker-tag   # Tag for Docker Hub
make docker-push  # Push to Docker Hub
```

## Docker Hub

The official Docker image is available at:
- `martoc/mcp-karpenter-documentation:latest` - Latest stable release
- `martoc/mcp-karpenter-documentation:v0.1.0` - Specific version

The image includes pre-indexed Karpenter documentation (~181 documents) and is ready to use immediately.

## Documentation

- [USAGE.md](USAGE.md) - Detailed usage instructions
- [CODESTYLE.md](CODESTYLE.md) - Code style guidelines
- [CLAUDE.md](CLAUDE.md) - Claude Code instructions

## Licence

This project is licensed under the MIT Licence - see the [LICENSE](LICENSE) file for details.
