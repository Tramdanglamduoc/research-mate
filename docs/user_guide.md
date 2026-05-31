# User Guide

## What is ResearchMate?

ResearchMate is an AI-powered research assistant that runs in your terminal. It has two modes:

- **Research Q&A** — Ask a research question and get an answer with sources
- **Paper Review** — Upload an academic paper and get a structured review

## Installation

### Prerequisites
- Python 3.10 or higher
- An API key from OpenAI or Anthropic

### Steps

```bash
# 1. Clone the repository
git clone https://github.com/Tramdanglamduoc/research-mate
cd research-mate

# 2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate        # Linux/Mac
# venv\Scripts\activate         # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up your API key
cp .env.example .env
# Edit .env and add your API key
```

## Configuration

Edit the `.env` file:

| Variable | Description | Example |
|----------|-------------|---------|
| `LLM_PROVIDER` | Which AI service to use | `openai` or `anthropic` |
| `OPENAI_API_KEY` | Your OpenAI API key | `sk-...` |
| `ANTHROPIC_API_KEY` | Your Anthropic API key | `sk-ant-...` |
| `LLM_MODEL` | The model to use | `gpt-4o-mini` |
| `LLM_MAX_TOKENS` | Max response length | `2000` |

## Usage

### Starting the Program

```bash
python main.py
```

You will see a menu:
```
Select a mode:
  1 — 📚 Research Q&A
  2 — 📝 Paper Review
  3 — 🚪 Exit
```

### Mode 1: Research Q&A

1. Select mode `1`
2. Type your research question
3. Optionally provide a local file path (.txt or .pdf)
4. The system will search the web, read your file, and generate an answer
5. Type `back` to return to the menu

**Example:**
```
❓ Your question: What are the main approaches to neural machine translation?
📎 Include a local file? (path or 'no'): no

🔍 Searching web sources...
📄 Found 5 results, 2 with detailed content
🧠 Synthesizing answer...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Neural machine translation (NMT) primarily uses...
[Source: Wikipedia - Neural machine translation]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

### Mode 2: Paper Review

1. Select mode `2`
2. Enter the path to your paper file (PDF or TXT)
3. Optionally specify the target venue and paper type
4. Wait for the multi-step review to complete
5. Optionally save the review to a file

**Example:**
```
📄 Path to paper (PDF or TXT): ./papers/my_paper.pdf
🏛️  Target venue (optional): EMNLP 2025
📋 Paper type (optional): full research

📖 Reading paper: ./papers/my_paper.pdf
📄 Paper loaded: my_paper.pdf (45230 chars)
🔬 Starting multi-step review...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Paper Review (Target: EMNLP 2025) [full research]

## Structured Summary
...

## Top 10 Priority Actions
1. Add ablation study for the proposed method
2. ...
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💾 Save review to file? (path or 'no'): review_output.md
✅ Review saved to review_output.md
```

## Supported File Types

| Format | Extension | Used In |
|--------|-----------|---------|
| Plain text | `.txt` | Q&A and Review |
| Markdown | `.md` | Q&A and Review |
| PDF | `.pdf` | Q&A and Review |

## Troubleshooting

**"No valid API key found"** — Make sure you copied `.env.example` to `.env` and added your real API key.

**"PyPDF2 is required"** — Run `pip install PyPDF2` to install the PDF reader.

**Empty search results** — Check your internet connection. Wikipedia API requires network access.

**"Unknown LLM provider"** — Check that `LLM_PROVIDER` in `.env` is either `openai` or `anthropic`.
