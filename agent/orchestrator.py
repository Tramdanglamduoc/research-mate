"""
Orchestrator Agent for ResearchMate.
Core agent logic that receives user requests, selects tools, and produces results.
"""

from typing import Optional
from tools.web_search import WebSearchTool
from tools.file_reader import FileReaderTool
from tools.summarizer import SummarizerTool
from tools.calculator import CalculatorTool
from tools.paper_reviewer import PaperReviewerTool
from agent.prompt_templates import QA_SYSTEM_PROMPT, QA_ANSWER_PROMPT
from config import Config


class Orchestrator:
    """
    Central agent that coordinates tool usage to answer user queries.
    Supports two modes: Research Q&A and Paper Review.
    """

    def __init__(self):
        self.web_search = WebSearchTool(max_results=Config.SEARCH_MAX_RESULTS)
        self.file_reader = FileReaderTool()
        self.summarizer = SummarizerTool()
        self.calculator = CalculatorTool()
        self.paper_reviewer = PaperReviewerTool()

    # ── Mode 1: Research Q&A ──────────────────────────────────────────

    def research_qa(
        self, question: str, file_path: Optional[str] = None
    ) -> str:
        """
        Answer a research question using web search and optional file content.

        Args:
            question: The user's research question.
            file_path: Optional path to a local file to include as context.

        Returns:
            A structured answer string with citations.
        """
        print("\n🔍 Searching web sources...")
        search_data = self.web_search.search_and_summarize(question)

        results = search_data["results"]
        summaries = search_data["summaries"]
        print(f"📄 Found {len(results)} results, {len(summaries)} with detailed content")

        # Build sources text for the prompt
        sources_text = self._format_sources(results, summaries)

        # Read file if provided
        file_context = ""
        if file_path:
            print(f"📖 Reading file: {file_path}")
            file_data = self.file_reader.read(file_path)
            if file_data["success"]:
                file_content = file_data["content"]
                # Summarize if the file is very long
                if len(file_content) > 3000:
                    print("📝 File is long, summarizing...")
                    summary_result = self.summarizer.summarize(file_content)
                    if summary_result["success"]:
                        file_content = summary_result["summary"]

                file_context = (
                    f"\nAdditional context from uploaded file "
                    f"({file_data['file_name']}):\n{file_content}"
                )
            else:
                print(f"⚠️  Could not read file: {file_data['error']}")

        # Check if question involves math
        math_result = self._check_math(question)
        if math_result:
            sources_text += f"\n\nCalculation result: {math_result}"

        # Generate answer using LLM
        print("🧠 Synthesizing answer...")
        answer = self._generate_answer(question, sources_text, file_context)

        # Append source list
        source_list = self._format_source_list(results)
        return f"{answer}\n\n{source_list}"

    # ── Mode 2: Paper Review ──────────────────────────────────────────

    def review_paper(
        self,
        file_path: str,
        venue: Optional[str] = None,
        paper_type: Optional[str] = None,
    ) -> str:
        """
        Perform a structured review of an academic paper.

        Args:
            file_path: Path to the paper file (PDF or text).
            venue: Optional target venue name.
            paper_type: Optional paper type description.

        Returns:
            A complete review in markdown format.
        """
        print(f"\n📖 Reading paper: {file_path}")
        file_data = self.file_reader.read(file_path)

        if not file_data["success"]:
            return f"❌ Error reading file: {file_data['error']}"

        paper_text = file_data["content"]
        if len(paper_text.strip()) < 100:
            return "❌ The file appears to be empty or too short for review."

        print(f"📄 Paper loaded: {file_data['file_name']} ({len(paper_text)} chars)")
        print("🔬 Starting multi-step review...\n")

        review_data = self.paper_reviewer.review(
            paper_text=paper_text,
            venue=venue,
            paper_type=paper_type,
        )

        if not review_data["success"]:
            return f"❌ Review failed: {review_data['error']}"

        return review_data["review"]

    # ── Private Helper Methods ────────────────────────────────────────

    def _format_sources(self, results: list, summaries: list) -> str:
        """Format search results and summaries into a text block for the LLM."""
        parts = []

        # Add detailed summaries first (richer content)
        for s in summaries:
            parts.append(f"Source: {s['title']} ({s['url']})\n{s['content'][:2000]}")

        # Add search snippets for results without summaries
        summarized_titles = {s["title"] for s in summaries}
        for r in results:
            if r["title"] not in summarized_titles:
                parts.append(
                    f"Source: {r['title']} ({r['source']})\n{r['snippet']}"
                )

        return "\n\n---\n\n".join(parts) if parts else "No sources found."

    def _format_source_list(self, results: list) -> str:
        """Format a numbered list of sources for display."""
        if not results:
            return ""

        lines = ["SOURCES:"]
        seen = set()
        for i, r in enumerate(results, 1):
            key = r["title"]
            if key not in seen:
                seen.add(key)
                url = r.get("url", "")
                lines.append(f"[{i}] {r['title']} — {url}")

        return "\n".join(lines)

    def _check_math(self, question: str) -> Optional[str]:
        """Check if the question contains a math expression and evaluate it."""
        math_keywords = ["calculate", "compute", "what is", "how much", "percentage"]
        question_lower = question.lower()

        if not any(kw in question_lower for kw in math_keywords):
            return None

        # Try to extract a math expression (simple heuristic)
        import re
        patterns = [
            r"calculate\s+(.+)",
            r"compute\s+(.+)",
            r"what is\s+([\d\.\+\-\*\/\(\)\s\^]+)",
        ]

        for pattern in patterns:
            match = re.search(pattern, question_lower)
            if match:
                expr = match.group(1).strip().rstrip("?.")
                result = self.calculator.calculate(expr)
                if result["success"]:
                    return f"{expr} = {result['result']}"

        return None

    def _generate_answer(
        self, question: str, sources: str, file_context: str
    ) -> str:
        """Generate the final answer by calling the LLM."""
        prompt = QA_ANSWER_PROMPT.format(
            question=question,
            sources=sources,
            file_context=file_context,
        )

        try:
            if Config.LLM_PROVIDER == "openai":
                return self._call_openai(prompt)
            elif Config.LLM_PROVIDER == "anthropic":
                return self._call_anthropic(prompt)
            else:
                return f"[Error: Unknown LLM provider '{Config.LLM_PROVIDER}']"
        except Exception as e:
            return f"[Error generating answer: {e}]"

    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API with system prompt."""
        from openai import OpenAI

        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        response = client.chat.completions.create(
            model=Config.LLM_MODEL,
            messages=[
                {"role": "system", "content": QA_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=Config.LLM_MAX_TOKENS,
        )
        return response.choices[0].message.content

    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API with system prompt."""
        import anthropic

        client = anthropic.Anthropic(api_key=Config.ANTHROPIC_API_KEY)
        response = client.messages.create(
            model=Config.LLM_MODEL,
            max_tokens=Config.LLM_MAX_TOKENS,
            system=QA_SYSTEM_PROMPT,
            messages=[{"role": "user", "content": prompt}],
        )
        return response.content[0].text
