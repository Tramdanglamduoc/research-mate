# Developer Guide

## Project Architecture

ResearchMate follows a modular architecture with three main layers:

```
main.py (CLI Interface)
    │
    ▼
agent/orchestrator.py (Agent Logic)
    │
    ├── tools/web_search.py
    ├── tools/file_reader.py
    ├── tools/summarizer.py
    ├── tools/calculator.py
    └── tools/paper_reviewer.py
```

### Layer 1: CLI Interface (`main.py`)
Handles user interaction — mode selection, input collection, and output display. This layer knows nothing about how tools work; it only talks to the Orchestrator.

### Layer 2: Agent / Orchestrator (`agent/orchestrator.py`)
The core decision-making component. It receives user requests, decides which tools to call and in what order, collects results, and produces the final output. This is where the "agent logic" lives.

### Layer 3: Tools (`tools/`)
Each tool is a self-contained module with a single responsibility. Tools do not call each other — they are only called by the Orchestrator.

## Adding a New Tool

1. Create a new file in `tools/`, e.g., `tools/my_tool.py`
2. Define a class with a clear public method:

```python
class MyTool:
    def run(self, input_data: str) -> dict:
        # Process input
        return {"result": ..., "success": True, "error": None}
```

3. Import and initialize the tool in `agent/orchestrator.py`
4. Add logic in the orchestrator to decide when to call this tool
5. Write tests in `tests/test_my_tool.py`

## Configuration

All configuration is centralized in `config.py`, which reads from `.env` files. To add a new config value:

1. Add the variable to `.env.example`
2. Add the corresponding attribute to the `Config` class in `config.py`

## Running Tests

```bash
# Run all tests
pytest tests/ -v

# Run a specific test file
pytest tests/test_calculator.py -v

# Run with output shown
pytest tests/ -v -s
```

## Code Conventions

- **Type hints** on all function signatures
- **Docstrings** on all public classes and methods (Google style)
- **Return dicts** from tools with at least `success` and `error` keys
- **No cross-imports** between tools — tools are independent modules
