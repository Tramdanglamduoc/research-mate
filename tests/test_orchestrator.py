"""Tests for the Orchestrator Agent."""

import os
import tempfile
import pytest
from unittest.mock import patch, MagicMock
from agent.orchestrator import Orchestrator


class TestOrchestrator:
    """Test suite for Orchestrator."""

    def setup_method(self):
        self.agent = Orchestrator()

    def test_tools_initialized(self):
        """Test that all tools are properly initialized."""
        assert self.agent.web_search is not None
        assert self.agent.file_reader is not None
        assert self.agent.summarizer is not None
        assert self.agent.calculator is not None
        assert self.agent.paper_reviewer is not None

    def test_format_sources_with_data(self):
        """Test source formatting with actual data."""
        results = [
            {"title": "Article A", "snippet": "About topic A", "source": "Wikipedia", "url": "https://a.com"},
            {"title": "Article B", "snippet": "About topic B", "source": "DuckDuckGo", "url": "https://b.com"},
        ]
        summaries = [
            {"title": "Article A", "content": "Detailed content about topic A...", "url": "https://a.com"},
        ]

        text = self.agent._format_sources(results, summaries)
        assert "Article A" in text
        assert "Detailed content" in text
        # Article B should appear as snippet since it has no summary
        assert "About topic B" in text

    def test_format_sources_empty(self):
        """Test source formatting with no data."""
        text = self.agent._format_sources([], [])
        assert text == "No sources found."

    def test_format_source_list(self):
        """Test the numbered source list output."""
        results = [
            {"title": "Source 1", "url": "https://s1.com", "source": "Wikipedia"},
            {"title": "Source 2", "url": "https://s2.com", "source": "DuckDuckGo"},
        ]
        text = self.agent._format_source_list(results)
        assert "SOURCES:" in text
        assert "[1]" in text
        assert "[2]" in text
        assert "Source 1" in text

    def test_format_source_list_deduplication(self):
        """Test that duplicate sources are removed."""
        results = [
            {"title": "Same Title", "url": "https://a.com", "source": "Wikipedia"},
            {"title": "Same Title", "url": "https://a.com", "source": "Wikipedia"},
        ]
        text = self.agent._format_source_list(results)
        assert text.count("Same Title") == 1

    def test_check_math_with_calculation(self):
        """Test math detection in queries."""
        result = self.agent._check_math("calculate 2 + 3")
        assert result is not None
        assert "5" in result

    def test_check_math_no_math(self):
        """Test that non-math queries return None."""
        result = self.agent._check_math("What is transfer learning?")
        assert result is None

    @patch.object(Orchestrator, "_generate_answer")
    def test_research_qa_basic(self, mock_answer):
        """Test basic Q&A flow with mocked LLM."""
        mock_answer.return_value = "Transfer learning is a technique..."

        answer = self.agent.research_qa("What is transfer learning?")

        assert "Transfer learning" in answer
        mock_answer.assert_called_once()

    @patch.object(Orchestrator, "_generate_answer")
    def test_research_qa_with_file(self, mock_answer):
        """Test Q&A with a local file included."""
        mock_answer.return_value = "Based on the document..."

        # Create a temp file
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("This is research content about neural networks.")
            tmp_path = f.name

        try:
            answer = self.agent.research_qa(
                "Tell me about neural networks", file_path=tmp_path
            )
            assert isinstance(answer, str)
            mock_answer.assert_called_once()
        finally:
            os.unlink(tmp_path)

    def test_review_paper_nonexistent_file(self):
        """Test paper review with a file that does not exist."""
        result = self.agent.review_paper("/tmp/nonexistent_paper.pdf")
        assert "Error" in result or "error" in result.lower()
