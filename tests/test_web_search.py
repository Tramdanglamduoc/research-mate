"""Tests for the Web Search Tool."""

import pytest
from tools.web_search import WebSearchTool


class TestWebSearchTool:
    """Test suite for WebSearchTool."""

    def setup_method(self):
        self.tool = WebSearchTool(max_results=2)

    def test_wikipedia_search_returns_results(self):
        """Test that Wikipedia search returns at least one result."""
        results = self.tool.search_wikipedia("machine learning", max_results=2)
        assert len(results) > 0
        assert "title" in results[0]
        assert "url" in results[0]
        assert "source" in results[0]
        assert results[0]["source"] == "Wikipedia"

    def test_wikipedia_search_empty_query(self):
        """Test that an empty query returns an empty list."""
        results = self.tool.search_wikipedia("")
        assert isinstance(results, list)

    def test_wikipedia_summary_valid_title(self):
        """Test fetching a Wikipedia summary for a known article."""
        summary = self.tool.get_wikipedia_summary("Python (programming language)")
        assert summary is not None
        assert len(summary) > 50

    def test_wikipedia_summary_invalid_title(self):
        """Test fetching summary for a non-existent article."""
        summary = self.tool.get_wikipedia_summary("Xyzzy_nonexistent_article_12345")
        assert summary is None

    def test_search_combined_returns_list(self):
        """Test that the combined search returns a list."""
        results = self.tool.search("deep learning")
        assert isinstance(results, list)
        assert len(results) > 0

    def test_search_and_summarize_structure(self):
        """Test that search_and_summarize returns expected structure."""
        data = self.tool.search_and_summarize("natural language processing")
        assert "results" in data
        assert "summaries" in data
        assert isinstance(data["results"], list)
        assert isinstance(data["summaries"], list)
