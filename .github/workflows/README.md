# GitHub Actions Workflows

This directory contains CI/CD workflows for the MCP Karpenter Documentation Server.

## Workflows

### CI (`ci.yml`)

Runs on every push and pull request to `main`:

- **Test Job**:
  - Sets up Python 3.12 and uv
  - Installs dependencies
  - Runs linter (Ruff)
  - Runs type checker (mypy)
  - Runs tests with coverage
  - Uploads coverage reports to Codecov

- **Docker Job**:
  - Builds the Docker image
  - Tests the Docker image

### Docker Publish (`docker-publish.yml`)

Publishes Docker images to Docker Hub:

- **Triggers**:
  - Push to `main` branch → `latest` tag
  - Version tags (`v*`) → version-specific tags
  - GitHub releases → version-specific tags

- **Multi-platform builds**:
  - `linux/amd64`
  - `linux/arm64`

- **Image tags**:
  - `martoc/mcp-karpenter-documentation:latest`
  - `martoc/mcp-karpenter-documentation:v0.1.0`
  - `martoc/mcp-karpenter-documentation:0.1`
  - `martoc/mcp-karpenter-documentation:0`

## Required Secrets

Configure these secrets in your GitHub repository settings:

- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub access token (not password)

### Setting up Docker Hub Access Token

1. Go to https://hub.docker.com/settings/security
2. Click "New Access Token"
3. Give it a descriptive name (e.g., "github-actions-mcp-karpenter")
4. Select permissions: Read & Write
5. Generate token
6. Copy the token and add it to GitHub Secrets as `DOCKER_PASSWORD`

### Adding Secrets to GitHub

1. Go to repository Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `DOCKER_USERNAME` with your Docker Hub username
4. Add `DOCKER_PASSWORD` with your Docker Hub access token

## Manual Docker Publishing

To manually build and publish:

```bash
# Build
make docker-build

# Tag
make docker-tag

# Push (requires Docker Hub login)
make docker-push
```

Or using Docker commands directly:

```bash
# Build
docker build -t mcp-karpenter-documentation .

# Tag
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:latest
docker tag mcp-karpenter-documentation martoc/mcp-karpenter-documentation:v0.1.0

# Push
docker push martoc/mcp-karpenter-documentation:latest
docker push martoc/mcp-karpenter-documentation:v0.1.0
```

## Image Registry

Images are published to Docker Hub:
- Repository: https://hub.docker.com/r/martoc/mcp-karpenter-documentation
- Tags: https://hub.docker.com/r/martoc/mcp-karpenter-documentation/tags

## Badge

Add this badge to your README to show the latest Docker build status:

```markdown
[![Docker Build](https://github.com/martoc/mcp-karpenter-documentation/actions/workflows/docker-publish.yml/badge.svg)](https://github.com/martoc/mcp-karpenter-documentation/actions/workflows/docker-publish.yml)
```
