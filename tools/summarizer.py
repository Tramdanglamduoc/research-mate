"""
Summarizer Tool for ResearchMate.
Uses an LLM to summarize long text into concise summaries.
"""

from config import Config


class SummarizerTool:
    """Tool that summarizes long text using an LLM API."""

    def __init__(self):
        self.provider = Config.LLM_PROVIDER
        self.model = Config.LLM_MODEL
        self.max_tokens = Config.LLM_MAX_TOKENS

    def summarize(self, text: str, max_length: int = 500) -> dict:
        """
        Summarize the given text using the configured LLM.

        Args:
            text: The text to summarize.
            max_length: Approximate maximum word count for the summary.

        Returns:
            A dict with 'summary' (the summarized text) and 'success' (bool).
        """
        if not text or len(text.strip()) == 0:
            return {"summary": "", "success": False, "error": "Empty text provided."}

        prompt = (
            f"Summarize the following text in approximately {max_length} words. "
            "Focus on the key points, main arguments, and important findings. "
            "Be concise but preserve important details.\n\n"
            f"Text:\n{text[:8000]}"  # Limit input to avoid token overflow
        )

        try:
            summary = self._call_llm(prompt)
            return {"summary": summary, "success": True, "error": None}
        except Exception as e:
            return {"summary": "", "success": False, "error": str(e)}

    def _call_llm(self, prompt: str) -> str:
        """
        Send a prompt to the configured LLM provider and return the response.

        Args:
            prompt: The prompt string to send.

        Returns:
            The LLM's response text.
        """
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
