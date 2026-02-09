"""Indexer for Karpenter documentation from aws/karpenter-provider-aws repository."""

import logging
import subprocess
import tempfile
from pathlib import Path

from mcp_karpenter_documentation.database import DocumentDatabase
from mcp_karpenter_documentation.parser import DocumentParser

logger = logging.getLogger(__name__)


class KarpenterDocsIndexer:
    """Indexes Karpenter documentation from the aws/karpenter-provider-aws GitHub repository."""

    KARPENTER_REPO = "https://github.com/aws/karpenter-provider-aws.git"
    DOCS_PATH = "website"

    def __init__(self, database: DocumentDatabase) -> None:
        """Initialise indexer with database instance.

        Args:
            database: DocumentDatabase instance for storing documents.
        """
        self.database = database
        self.parser = DocumentParser()

    def index_from_git(self, branch: str = "main", shallow: bool = True) -> int:
        """Clone aws/karpenter-provider-aws repo and index documentation.

        Args:
            branch: Git branch to clone.
            shallow: Whether to do a shallow clone.

        Returns:
            Number of documents indexed.
        """
        with tempfile.TemporaryDirectory() as temp_dir:
            repo_path = Path(temp_dir) / "karpenter-provider-aws"
            self._clone_repository(repo_path, branch, shallow)
            return self._index_directory(repo_path / self.DOCS_PATH)

    def index_from_path(self, docs_path: Path) -> int:
        """Index documentation from a local path.

        Args:
            docs_path: Path to the documentation directory.

        Returns:
            Number of documents indexed.
        """
        return self._index_directory(docs_path)

    def _clone_repository(self, target_path: Path, branch: str, shallow: bool) -> None:
        """Clone the aws/karpenter-provider-aws repository.

        Args:
            target_path: Directory to clone into.
            branch: Git branch to clone.
            shallow: Whether to do a shallow clone.
        """
        cmd = ["git", "clone"]
        if shallow:
            cmd.extend(["--depth", "1", "--filter=blob:none", "--sparse"])
        cmd.extend(["--branch", branch, self.KARPENTER_REPO, str(target_path)])

        logger.info("Cloning aws/karpenter-provider-aws repository...")
        subprocess.run(cmd, check=True, capture_output=True)  # noqa: S603

        # For sparse checkout, specify only the website directory
        if shallow:
            logger.info("Setting up sparse checkout for website directory...")
            subprocess.run(  # noqa: S603
                ["git", "-C", str(target_path), "sparse-checkout", "set", self.DOCS_PATH],  # noqa: S607
                check=True,
                capture_output=True,
            )

        logger.info("Repository cloned successfully")

    def _index_directory(self, docs_path: Path) -> int:
        """Index all markdown files in the documentation directory.

        Args:
            docs_path: Path to the documentation directory.

        Returns:
            Number of documents indexed.

        Raises:
            ValueError: If the documentation path does not exist.
        """
        if not docs_path.exists():
            msg = f"Documentation path does not exist: {docs_path}"
            raise ValueError(msg)

        indexed_count = 0
        md_files = list(docs_path.rglob("*.md")) + list(docs_path.rglob("*.markdown"))

        logger.info("Found %d markdown files to index", len(md_files))

        for file_path in md_files:
            document = self.parser.parse_file(file_path, docs_path)
            if document:
                self.database.upsert_document(document)
                indexed_count += 1
                logger.debug("Indexed: %s", document.path)
            else:
                logger.warning("Failed to parse: %s", file_path)

        logger.info("Successfully indexed %d documents", indexed_count)
        return indexed_count

    def rebuild_index(self, branch: str = "main") -> int:
        """Clear existing index and rebuild from scratch.

        Args:
            branch: Git branch to index from.

        Returns:
            Number of documents indexed.
        """
        logger.info("Clearing existing index...")
        self.database.clear()
        return self.index_from_git(branch)
