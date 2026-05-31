"""Tests for the Paper Reviewer Tool."""

import pytest
from unittest.mock import patch, MagicMock
from tools.paper_reviewer import PaperReviewerTool


SAMPLE_PAPER = """
Title: A Survey of Transfer Learning in NLP

Abstract: Transfer learning has become the dominant paradigm in natural
language processing. This paper surveys recent advances in transfer learning
methods, comparing BERT, GPT, and T5 architectures across multiple benchmarks.

1. Introduction
Transfer learning allows models pretrained on large corpora to be fine-tuned
for specific downstream tasks. This approach has led to significant improvements
in accuracy across NLP tasks including sentiment analysis, named entity
recognition, and question answering.

2. Methodology
We compare three architectures on the GLUE benchmark:
- BERT: 88.5% average accuracy
- GPT-2: 85.3% average accuracy
- T5: 90.1% average accuracy

3. Results
T5 outperforms both BERT and GPT-2 on 7 out of 8 GLUE tasks.
The average improvement over BERT is 1.6 percentage points.

4. Conclusion
Transfer learning continues to advance rapidly. Future work should
explore more efficient fine-tuning methods.
"""


class TestPaperReviewerTool:
    """Test suite for PaperReviewerTool."""

    def setup_method(self):
        self.tool = PaperReviewerTool()

    def test_review_empty_text(self):
        """Test that empty paper text returns an error."""
        result = self.tool.review(paper_text="")
        assert result["success"] is False
        assert "too short" in result["error"].lower()

    def test_review_short_text(self):
        """Test that very short text is rejected."""
        result = self.tool.review(paper_text="Short.")
        assert result["success"] is False

    def test_build_venue_context_with_venue(self):
        """Test venue context generation with venue specified."""
        context = self.tool._build_venue_context("NeurIPS", "full research")
        assert "NeurIPS" in context
        assert "full research" in context

    def test_build_venue_context_empty(self):
        """Test venue context generation with no venue."""
        context = self.tool._build_venue_context(None, None)
        assert context == ""

    @patch.object(PaperReviewerTool, "_call_llm")
    def test_review_full_pipeline(self, mock_llm):
        """Test the full review pipeline with mocked LLM."""
        mock_llm.return_value = "This is a mock LLM response for the review step."

        result = self.tool.review(
            paper_text=SAMPLE_PAPER,
            venue="EMNLP",
            paper_type="full research",
        )

        assert result["success"] is True
        assert "review" in result
        assert len(result["review"]) > 0
        assert "sections" in result
        assert "summary" in result["sections"]
        assert "consistency" in result["sections"]
        assert "analysis" in result["sections"]
        assert "feedback" in result["sections"]
        assert "top_actions" in result["sections"]

        # LLM should be called 5 times (one per review step)
        assert mock_llm.call_count == 5

    @patch.object(PaperReviewerTool, "_call_llm")
    def test_review_without_venue(self, mock_llm):
        """Test review without specifying venue."""
        mock_llm.return_value = "Mock response."

        result = self.tool.review(paper_text=SAMPLE_PAPER)

        assert result["success"] is True
        assert mock_llm.call_count == 5

    @patch.object(PaperReviewerTool, "_call_llm")
    def test_review_llm_failure(self, mock_llm):
        """Test that LLM failure is handled gracefully."""
        mock_llm.side_effect = Exception("API connection failed")

        result = self.tool.review(paper_text=SAMPLE_PAPER)

        assert result["success"] is False
        assert "API connection failed" in result["error"]

    def test_compile_review_format(self):
        """Test that compiled review has correct markdown structure."""
        sections = {
            "summary": "Summary content",
            "consistency": "No issues found",
            "analysis": "Novel approach",
            "feedback": "Strong methodology",
            "top_actions": "1. Add more experiments",
        }
        review = self.tool._compile_review(sections, "ICSE", "full research")

        assert "# Paper Review" in review
        assert "ICSE" in review
        assert "full research" in review
        assert "Summary content" in review
        assert "No issues found" in review
