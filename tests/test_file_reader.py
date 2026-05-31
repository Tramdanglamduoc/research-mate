"""Tests for the File Reader Tool."""

import os
import tempfile
import pytest
from tools.file_reader import FileReaderTool


class TestFileReaderTool:
    """Test suite for FileReaderTool."""

    def setup_method(self):
        self.tool = FileReaderTool()

    def test_read_txt_file(self):
        """Test reading a plain text file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("This is a test document.\nWith two lines.")
            tmp_path = f.name

        try:
            result = self.tool.read(tmp_path)
            assert result["success"] is True
            assert "This is a test document." in result["content"]
            assert result["file_type"] == ".txt"
        finally:
            os.unlink(tmp_path)

    def test_read_md_file(self):
        """Test reading a markdown file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".md", delete=False, encoding="utf-8"
        ) as f:
            f.write("# Heading\n\nSome markdown content.")
            tmp_path = f.name

        try:
            result = self.tool.read(tmp_path)
            assert result["success"] is True
            assert "# Heading" in result["content"]
        finally:
            os.unlink(tmp_path)

    def test_read_nonexistent_file(self):
        """Test reading a file that does not exist."""
        result = self.tool.read("/tmp/nonexistent_file_12345.txt")
        assert result["success"] is False
        assert "not found" in result["error"].lower()

    def test_read_unsupported_extension(self):
        """Test reading a file with unsupported extension."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".xyz", delete=False
        ) as f:
            f.write("test")
            tmp_path = f.name

        try:
            result = self.tool.read(tmp_path)
            assert result["success"] is False
            assert "unsupported" in result["error"].lower()
        finally:
            os.unlink(tmp_path)

    def test_read_empty_file(self):
        """Test reading an empty text file."""
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("")
            tmp_path = f.name

        try:
            result = self.tool.read(tmp_path)
            assert result["success"] is True
            assert result["content"] == ""
        finally:
            os.unlink(tmp_path)
