"""
Configuration module for ResearchMate.
Loads environment variables and provides default settings.
"""

import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()


class Config:
    """Central configuration class for the application."""

    # LLM Settings
    LLM_PROVIDER: str = os.getenv("LLM_PROVIDER", "openai")
    LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-4o-mini")
    LLM_MAX_TOKENS: int = int(os.getenv("LLM_MAX_TOKENS", "2000"))

    # API Keys
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")

    # Tool Settings
    SEARCH_MAX_RESULTS: int = 3
    SUMMARY_MAX_LENGTH: int = 500
    PDF_MAX_PAGES: int = 20

    @classmethod
    def get_api_key(cls) -> str:
        """Return the API key for the configured LLM provider."""
        if cls.LLM_PROVIDER == "openai":
            return cls.OPENAI_API_KEY
        elif cls.LLM_PROVIDER == "anthropic":
            return cls.ANTHROPIC_API_KEY
        else:
            raise ValueError(f"Unknown LLM provider: {cls.LLM_PROVIDER}")

    @classmethod
    def validate(cls) -> bool:
        """Check that required configuration is present."""
        api_key = cls.get_api_key()
        if not api_key or api_key.startswith("your_"):
            print(f"[ERROR] No valid API key found for provider '{cls.LLM_PROVIDER}'.")
            print("Please copy .env.example to .env and add your API key.")
            return False
        return True
