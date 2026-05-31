"""
Data Converter Utility for ResearchMate.
Handles format conversion between different tools and components.
"""

import json
from typing import Any


class DataConverter:
    """Converts data between formats used by different tools."""

    @staticmethod
    def search_results_to_text(results: list[dict]) -> str:
        """
        Convert search result dicts into a plain text block.

        Args:
            results: List of search result dicts with 'title', 'snippet', 'url'.

        Returns:
            Formatted text string.
        """
        if not results:
            return "No results found."

        lines = []
        for i, r in enumerate(results, 1):
            lines.append(
                f"{i}. {r.get('title', 'Untitled')}\n"
                f"   {r.get('snippet', 'No description')}\n"
                f"   URL: {r.get('url', 'N/A')}"
            )
        return "\n\n".join(lines)

    @staticmethod
    def review_to_markdown(review_data: dict) -> str:
        """
        Convert a review dict (from PaperReviewerTool) into clean markdown.

        Args:
            review_data: The review dict with 'sections' and 'review' keys.

        Returns:
            Markdown-formatted review string.
        """
        if not review_data.get("success"):
            return f"Review failed: {review_data.get('error', 'Unknown error')}"
        return review_data.get("review", "")

    @staticmethod
    def truncate_text(text: str, max_chars: int = 5000) -> str:
        """
        Truncate text to a maximum number of characters.
        Adds an indicator if text was truncated.

        Args:
            text: The text to truncate.
            max_chars: Maximum character count.

        Returns:
            Truncated text with indicator if needed.
        """
        if len(text) <= max_chars:
            return text
        return text[:max_chars] + "\n\n[... text truncated ...]"

    @staticmethod
    def dict_to_json(data: Any) -> str:
        """Convert a Python object to a formatted JSON string."""
        return json.dumps(data, indent=2, ensure_ascii=False)

    @staticmethod
    def clean_text(text: str) -> str:
        """
        Clean extracted text by removing excessive whitespace and empty lines.

        Args:
            text: Raw text content.

        Returns:
            Cleaned text.
        """
        lines = text.split("\n")
        cleaned = []
        prev_empty = False

        for line in lines:
            stripped = line.strip()
            if not stripped:
                if not prev_empty:
                    cleaned.append("")
                prev_empty = True
            else:
                cleaned.append(stripped)
                prev_empty = False

        return "\n".join(cleaned).strip()
