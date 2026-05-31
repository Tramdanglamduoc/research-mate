"""
Paper Reviewer Tool for ResearchMate.
Performs structured academic paper review using multi-step LLM analysis.
"""

from typing import Optional
from config import Config


class PaperReviewerTool:
    """Tool that performs a structured review of an academic paper."""

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.model = Config.LLM_MODEL
        self.max_tokens = Config.LLM_MAX_TOKENS

    def review(
        self,
        paper_text: str,
        venue: Optional[str] = None,
        paper_type: Optional[str] = None,
    ) -> dict:
        """
        Perform a full structured review of a paper.

        Args:
            paper_text: The full text content of the paper.
            venue: Optional target venue (e.g., "NeurIPS", "TOSEM").
            paper_type: Optional paper type (e.g., "full research", "short paper").

        Returns:
            A dict with 'review' (full review text), 'sections' (individual parts),
            and 'success' (bool).
        """
        if not paper_text or len(paper_text.strip()) < 100:
            return {
                "review": "",
                "sections": {},
                "success": False,
                "error": "Paper text is too short or empty.",
            }

        venue_context = self._build_venue_context(venue, paper_type)

        try:
            sections = {}

            # Step 1: Structured Summary
            sections["summary"] = self._step_summary(paper_text, venue_context)

            # Step 2: Numerical & Consistency Checks
            sections["consistency"] = self._step_consistency(paper_text, venue_context)

            # Step 3: Critical Analysis
            sections["analysis"] = self._step_analysis(paper_text, venue_context)

            # Step 4: Actionable Feedback
            sections["feedback"] = self._step_feedback(paper_text, venue_context)

            # Step 5: Top 10 Actions
            sections["top_actions"] = self._step_top_actions(paper_text, venue_context)

            # Combine into final review
            full_review = self._compile_review(sections, venue, paper_type)

            return {
                "review": full_review,
                "sections": sections,
                "success": True,
                "error": None,
            }
        except Exception as e:
            return {
                "review": "",
                "sections": {},
                "success": False,
                "error": str(e),
            }

    def _build_venue_context(
        self, venue: Optional[str], paper_type: Optional[str]
    ) -> str:
        """Build context string for venue-aware review."""
        if venue or paper_type:
            parts = []
            if venue:
                parts.append(f"target venue: {venue}")
            if paper_type:
                parts.append(f"paper type: {paper_type}")
            return (
                f"Review this paper considering it is intended for {', '.join(parts)}. "
                "Consider typical standards, expectations, and scope for this venue."
            )
        return ""

    def _step_summary(self, paper_text: str, venue_context: str) -> str:
        """Step 1: Generate a structured summary of the paper."""
        prompt = (
            f"{venue_context}\n\n"
            "Read the following academic paper and produce a structured summary with:\n"
            "1. Problem Statement — What problem does the paper address? Why does it matter?\n"
            "2. Contributions — What are the claimed contributions? (list them)\n"
            "3. Approach/Methodology — How do the authors solve the problem?\n"
            "4. Key Results — What are the main findings/metrics?\n"
            "5. Limitations — What are the acknowledged and unacknowledged limitations?\n\n"
            f"Paper:\n{paper_text[:6000]}"
        )
        return self._call_llm(prompt)

    def _step_consistency(self, paper_text: str, venue_context: str) -> str:
        """Step 2: Check numerical and internal consistency."""
        prompt = (
            f"{venue_context}\n\n"
            "Analyze the following paper for numerical and consistency issues:\n"
            "- Do numbers in the text match tables and figures?\n"
            "- Are statistics (p-values, confidence intervals) consistent?\n"
            "- Are percentages and calculations correct?\n"
            "- Are acronyms defined on first use?\n"
            "- Is terminology used consistently throughout?\n"
            "- Are there any broken references or citation issues?\n\n"
            "Report any issues found, or state that no issues were detected.\n\n"
            f"Paper:\n{paper_text[:6000]}"
        )
        return self._call_llm(prompt)

    def _step_analysis(self, paper_text: str, venue_context: str) -> str:
        """Step 3: Critical analysis on multiple dimensions."""
        prompt = (
            f"{venue_context}\n\n"
            "Critically analyze this paper on the following dimensions:\n"
            "- Novelty: Is this genuinely new? How does it differ from prior work?\n"
            "- Soundness: Is the methodology rigorous? Are experiments well-designed?\n"
            "- Significance: Does this advance the field meaningfully?\n"
            "- Clarity: Is the paper well-written and well-structured?\n"
            "- Reproducibility: Could someone replicate this from the paper alone?\n"
            "- Related Work: Is positioning against prior work fair and complete?\n\n"
            f"Paper:\n{paper_text[:6000]}"
        )
        return self._call_llm(prompt)

    def _step_feedback(self, paper_text: str, venue_context: str) -> str:
        """Step 4: Generate actionable feedback."""
        prompt = (
            f"{venue_context}\n\n"
            "Provide structured feedback on this paper:\n"
            "- Strengths: What does the paper do well? (cite specific sections)\n"
            "- Weaknesses: What needs improvement? (suggest specific fixes)\n"
            "- Questions for Authors: What needs clarification?\n"
            "- Minor Issues: Typos, formatting, citation problems\n\n"
            f"Paper:\n{paper_text[:6000]}"
        )
        return self._call_llm(prompt)

    def _step_top_actions(self, paper_text: str, venue_context: str) -> str:
        """Step 5: Prioritized list of top 10 improvements."""
        prompt = (
            f"{venue_context}\n\n"
            "Based on the following paper, list the TOP 10 most immediate actions "
            "the author should address. These should be the ones that bring the most "
            "benefit relative to the effort of implementing them. "
            "Rank them from most impactful to least impactful.\n\n"
            f"Paper:\n{paper_text[:6000]}"
        )
        return self._call_llm(prompt)

    def _compile_review(
        self,
        sections: dict,
        venue: Optional[str],
        paper_type: Optional[str],
    ) -> str:
        """Compile all review sections into a single markdown document."""
        header = "# Paper Review"
        if venue:
            header += f" (Target: {venue})"
        if paper_type:
            header += f" [{paper_type}]"

        review = f"""{header}

## Structured Summary
{sections.get('summary', 'N/A')}

## Numerical & Consistency Checks
{sections.get('consistency', 'N/A')}

## Critical Analysis
{sections.get('analysis', 'N/A')}

## Actionable Feedback
{sections.get('feedback', 'N/A')}

## Top 10 Priority Actions
{sections.get('top_actions', 'N/A')}
"""
        return review

    def _call_llm(self, prompt: str) -> str:
        """Send a prompt to the configured LLM and return the response."""
        if self.provider == "openai":
            return self._call_openai(prompt)
        elif self.provider == "anthropic":
            return self._call_anthropic(prompt)
        else:
            raise ValueError(f"Unknown LLM provider: {self.provider}")

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API."""
        from openai import OpenAI

        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API."""
        import anthropic

        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
