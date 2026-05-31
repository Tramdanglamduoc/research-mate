"""
File Reader Tool for ResearchMate.
Reads and extracts text from .txt and .pdf files.
"""

import os
from typing import Optional


class FileReaderTool:
    """Tool that reads text content from local files (.txt, .pdf)."""

    SUPPORTED_EXTENSIONS = [".txt", ".pdf", ".md"]

    def read(self, file_path: str) -> dict:
        """
        Read a file and return its text content.

        Args:
            file_path: Path to the file to read.

        Returns:
            A dict with 'content' (extracted text), 'file_name', 'file_type',
            and 'success' (bool).
        """
        file_path = os.path.expanduser(file_path)

        if not os.path.exists(file_path):
            return {
                "content": "",
                "file_name": file_path,
                "file_type": "",
                "success": False,
                "error": f"File not found: {file_path}",
            }

        ext = os.path.splitext(file_path)[1].lower()

        if ext not in self.SUPPORTED_EXTENSIONS:
            return {
                "content": "",
                "file_name": os.path.basename(file_path),
                "file_type": ext,
                "success": False,
                "error": f"Unsupported file type: {ext}. Supported: {self.SUPPORTED_EXTENSIONS}",
            }

        try:
            if ext == ".pdf":
                content = self._read_pdf(file_path)
            else:
                content = self._read_text(file_path)

            return {
                "content": content,
                "file_name": os.path.basename(file_path),
                "file_type": ext,
                "success": True,
                "error": None,
            }
        except Exception as e:
            return {
                "content": "",
                "file_name": os.path.basename(file_path),
                "file_type": ext,
                "success": False,
                "error": str(e),
            }

    def _read_text(self, file_path: str) -> str:
        """Read a plain text or markdown file."""
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()

    def _read_pdf(self, file_path: str, max_pages: Optional[int] = None) -> str:
        """
        Read a PDF file and extract text from all (or limited) pages.

        Args:
            file_path: Path to the PDF file.
            max_pages: Maximum number of pages to read. None means all pages.

        Returns:
            Extracted text content from the PDF.
        """
        try:
            from PyPDF2 import PdfReader
        except ImportError:
            raise ImportError(
                "PyPDF2 is required to read PDF files. "
                "Install it with: pip install PyPDF2"
            )

        reader = PdfReader(file_path)
        total_pages = len(reader.pages)

        if max_pages is not None:
            pages_to_read = min(max_pages, total_pages)
        else:
            pages_to_read = total_pages

        text_parts = []
        for i in range(pages_to_read):
            page = reader.pages[i]
            page_text = page.extract_text()
            if page_text:
                text_parts.append(f"--- Page {i + 1} ---\n{page_text}")

        if not text_parts:
            return "[No text could be extracted from this PDF]"

        return "\n\n".join(text_parts)

    def get_pdf_metadata(self, file_path: str) -> dict:
        """
        Extract metadata from a PDF file (title, author, page count).

        Args:
            file_path: Path to the PDF file.

        Returns:
            A dict with PDF metadata fields.
        """
        try:
            from PyPDF2 import PdfReader

            reader = PdfReader(file_path)
            meta = reader.metadata

            return {
                "title": meta.title if meta and meta.title else "Unknown",
                "author": meta.author if meta and meta.author else "Unknown",
                "pages": len(reader.pages),
                "success": True,
            }
        except Exception as e:
            return {
                "title": "Unknown",
                "author": "Unknown",
                "pages": 0,
                "success": False,
                "error": str(e),
            }
