"""Tests for the Data Converter Utility."""

import pytest
from utils.data_converter import DataConverter


class TestDataConverter:
    """Test suite for DataConverter."""

    def test_search_results_to_text(self):
        """Test converting search results to text."""
        results = [
            {"title": "AI Overview", "snippet": "AI is a field of CS.", "url": "https://example.com"},
            {"title": "ML Basics", "snippet": "ML is a subset of AI.", "url": "https://example2.com"},
        ]
        text = DataConverter.search_results_to_text(results)
        assert "AI Overview" in text
        assert "ML Basics" in text
        assert "https://example.com" in text

    def test_search_results_to_text_empty(self):
        """Test with empty results list."""
        text = DataConverter.search_results_to_text([])
        assert text == "No results found."

    def test_truncate_text_short(self):
        """Test that short text is not truncated."""
        text = "Hello world"
        result = DataConverter.truncate_text(text, max_chars=100)
        assert result == text

    def test_truncate_text_long(self):
        """Test that long text is truncated with indicator."""
        text = "A" * 200
        result = DataConverter.truncate_text(text, max_chars=50)
        assert len(result) < 200
        assert "truncated" in result

    def test_clean_text_removes_extra_whitespace(self):
        """Test that clean_text removes excessive blank lines."""
        text = "Line 1\n\n\n\n\nLine 2\n\n\nLine 3"
        result = DataConverter.clean_text(text)
        # Should have at most one blank line between paragraphs
        assert "\n\n\n" not in result
        assert "Line 1" in result
        assert "Line 2" in result
        assert "Line 3" in result

    def test_clean_text_strips_whitespace(self):
        """Test that clean_text strips leading/trailing whitespace from lines."""
        text = "  Hello  \n  World  "
        result = DataConverter.clean_text(text)
        assert result == "Hello\nWorld"

    def test_dict_to_json(self):
        """Test JSON serialization."""
        data = {"key": "value", "number": 42}
        result = DataConverter.dict_to_json(data)
        assert '"key": "value"' in result
        assert '"number": 42' in result

    def test_review_to_markdown_success(self):
        """Test converting a successful review to markdown."""
        review_data = {
            "success": True,
            "review": "# Paper Review\n\nThis is a review.",
        }
        result = DataConverter.review_to_markdown(review_data)
        assert "# Paper Review" in result

    def test_review_to_markdown_failure(self):
        """Test converting a failed review."""
        review_data = {"success": False, "error": "API timeout"}
        result = DataConverter.review_to_markdown(review_data)
        assert "failed" in result.lower()
