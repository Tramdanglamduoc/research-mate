# 🔬 ResearchMate — AI Research Assistant

ResearchMate is a Python-based AI research assistant that helps researchers and students find information, answer research questions, and review academic papers.

## Features

### 📚 Research Q&A
- Automatically searches Wikipedia and DuckDuckGo for relevant information
- Reads user-provided documents (.txt, .pdf)
- Synthesizes answers with source citations
- Supports follow-up questions in an interactive session
- Handles basic mathematical calculations

### 📝 Paper Review
- Performs structured multi-step review of academic papers
- Generates summaries of problem statement, contributions, methodology, and results
- Checks numerical and internal consistency
- Provides critical analysis on novelty, soundness, significance, and clarity
- Produces venue-aware feedback when target venue is specified
- Outputs prioritized top 10 improvement actions

## Project Structure

```
research-mate/
├── main.py                    # CLI entry point
├── config.py                  # Configuration management
├── agent/
│   ├── orchestrator.py        # Core agent logic
│   └── prompt_templates.py    # LLM prompt templates
├── tools/
│   ├── web_search.py          # Wikipedia + DuckDuckGo search
│   ├── file_reader.py         # .txt / .pdf reader
│   ├── summarizer.py          # LLM-based summarization
│   ├── calculator.py          # Safe math evaluation
│   └── paper_reviewer.py      # Multi-step paper review
├── utils/
│   └── data_converter.py      # Format conversion utilities
├── tests/                     # Test suite (pytest)
└── docs/                      # Documentation
```

## Quick Start

### 1. Clone and install

```bash
git clone https://github.com/YOUR_USERNAME/research-mate.git
cd research-mate
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env and add your OpenAI or Anthropic API key
```

### 3. Run

```bash
python main.py
```

## Requirements

- Python 3.10+
- An API key from [OpenAI](https://platform.openai.com/) or [Anthropic](https://console.anthropic.com/)

## Testing

```bash
pytest tests/ -v
```

## Documentation

- [User Guide](docs/user_guide.md) — How to install and use ResearchMate
- [Developer Guide](docs/developer_guide.md) — Architecture, code conventions, how to extend

## Tech Stack

| Component | Technology |
|-----------|-----------|
| Language | Python 3.10+ |
| LLM | OpenAI API / Anthropic API |
| Web Search | Wikipedia API, DuckDuckGo |
| PDF Reading | PyPDF2 |
| Math | SymPy |
| Testing | pytest |
| Config | python-dotenv |

## License

This project is for educational purposes.
