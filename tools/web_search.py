"""
Web Search Tool for ResearchMate.
Searches the web using DuckDuckGo and Wikipedia to find relevant information.
"""

import urllib.request
import urllib.parse
import json
from typing import Optional


class WebSearchTool:
    """Tool that searches the web for information relevant to a research query."""

    def __init__(self, max_results: int = 3):
        self.max_results = max_results

    def search_wikipedia(self, query: str, max_results: int = 3) -> list[dict]:
        """
        Search Wikipedia for articles matching the query.

        Args:
            query: The search query string.
            max_results: Maximum number of results to return.

        Returns:
            A list of dicts with 'title', 'snippet', and 'url' keys.
        """
        try:
            # Step 1: Search for matching article titles
            search_url = (
                "https://en.wikipedia.org/w/api.php?"
                + urllib.parse.urlencode({
                    "action": "query",
                    "list": "search",
                    "srsearch": query,
                    "srlimit": max_results,
                    "format": "json",
                })
            )

            with urllib.request.urlopen(search_url, timeout=10) as response:
                search_data = json.loads(response.read().decode())

            results = []
            for item in search_data.get("query", {}).get("search", []):
                title = item.get("title", "")
                snippet = item.get("snippet", "")
                # Remove HTML tags from snippet
                snippet = snippet.replace("<span class=\"searchmatch\">", "")
                snippet = snippet.replace("</span>", "")

                results.append({
                    "title": title,
                    "snippet": snippet,
                    "url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(title)}",
                    "source": "Wikipedia",
                })

            return results

        except Exception as e:
            print(f"[WebSearch] Wikipedia search error: {e}")
            return []

    def get_wikipedia_summary(self, title: str) -> Optional[str]:
        """
        Fetch the summary (first few paragraphs) of a Wikipedia article.

        Args:
            title: The exact Wikipedia article title.

        Returns:
            The article summary text, or None if not found.
        """
        try:
            url = (
                "https://en.wikipedia.org/w/api.php?"
                + urllib.parse.urlencode({
                    "action": "query",
                    "titles": title,
                    "prop": "extracts",
                    "exintro": True,
                    "explaintext": True,
                    "format": "json",
                })
            )

            with urllib.request.urlopen(url, timeout=10) as response:
                data = json.loads(response.read().decode())

            pages = data.get("query", {}).get("pages", {})
            for page_id, page_data in pages.items():
                if page_id != "-1":
                    return page_data.get("extract", None)

            return None

        except Exception as e:
            print(f"[WebSearch] Wikipedia summary error: {e}")
            return None

    def search_duckduckgo(self, query: str, max_results: int = 3) -> list[dict]:
        """
        Search DuckDuckGo for web results.

        Args:
            query: The search query string.
            max_results: Maximum number of results to return.

        Returns:
            A list of dicts with 'title', 'snippet', and 'url' keys.
        """
        try:
            from duckduckgo_search import DDGS

            results = []
            with DDGS() as ddgs:
                for r in ddgs.text(query, max_results=max_results):
                    results.append({
                        "title": r.get("title", ""),
                        "snippet": r.get("body", ""),
                        "url": r.get("href", ""),
                        "source": "DuckDuckGo",
                    })

            return results

        except ImportError:
            print("[WebSearch] duckduckgo-search not installed. Using Wikipedia only.")
            return []
        except Exception as e:
            print(f"[WebSearch] DuckDuckGo search error: {e}")
            return []

    def search(self, query: str) -> list[dict]:
        """
        Search both Wikipedia and DuckDuckGo, combine results.

        Args:
            query: The search query string.

        Returns:
            Combined list of search results from all sources.
        """
        results = []

        # Search Wikipedia first (always available, no API key needed)
        wiki_results = self.search_wikipedia(query, max_results=self.max_results)
        results.extend(wiki_results)

        # Also search DuckDuckGo if available
        ddg_results = self.search_duckduckgo(query, max_results=self.max_results)
        results.extend(ddg_results)

        return results

    def search_and_summarize(self, query: str) -> dict:
        """
        Search for information and fetch detailed summaries from Wikipedia.

        Args:
            query: The search query string.

        Returns:
            A dict with 'results' (list of search hits) and 'summaries' (detailed text).
        """
        results = self.search(query)

        # Fetch Wikipedia summaries for richer content
        summaries = []
        for r in results:
            if r["source"] == "Wikipedia":
                summary = self.get_wikipedia_summary(r["title"])
                if summary:
                    summaries.append({
                        "title": r["title"],
                        "content": summary,
                        "url": r["url"],
                    })

        return {
            "results": results,
            "summaries": summaries,
        }
