"""
ResearchMate — AI Research Assistant
Entry point for the command-line interface.

Usage:
    python main.py
"""

from agent.orchestrator import Orchestrator
from config import Config


BANNER = """
╔══════════════════════════════════════════╗
║   🔬 ResearchMate                        ║
║   AI Research Assistant                  ║
╚══════════════════════════════════════════╝
"""


def mode_research_qa(agent: Orchestrator) -> None:
    """Run the Research Q&A interactive loop."""
    print("\n📚 Research Q&A Mode")
    print("Ask any research question. Type 'back' to return to menu.\n")

    while True:
        question = input("❓ Your question: ").strip()

        if not question:
            continue
        if question.lower() in ("back", "exit", "quit"):
            break

        # Ask if user wants to include a local file
        file_path = input("📎 Include a local file? (path or 'no'): ").strip()
        if file_path.lower() in ("no", "n", ""):
            file_path = None

        # Run the research pipeline
        answer = agent.research_qa(question=question, file_path=file_path)

        print("\n" + "━" * 50)
        print(answer)
        print("━" * 50 + "\n")


def mode_paper_review(agent: Orchestrator) -> None:
    """Run the Paper Review workflow."""
    print("\n📝 Paper Review Mode")
    print("Provide a paper file for structured review. Type 'back' to return.\n")

    file_path = input("📄 Path to paper (PDF or TXT): ").strip()
    if file_path.lower() in ("back", "exit", "quit"):
        return

    venue = input("🏛️  Target venue (optional, press Enter to skip): ").strip() or None
    paper_type = input("📋 Paper type (e.g. 'full research', optional): ").strip() or None

    # Run the review pipeline
    review = agent.review_paper(
        file_path=file_path, venue=venue, paper_type=paper_type
    )

    print("\n" + "━" * 50)
    print(review)
    print("━" * 50)

    # Offer to save the review
    save = input("\n💾 Save review to file? (path or 'no'): ").strip()
    if save.lower() not in ("no", "n", ""):
        try:
            with open(save, "w", encoding="utf-8") as f:
                f.write(review)
            print(f"✅ Review saved to {save}")
        except Exception as e:
            print(f"⚠️  Could not save: {e}")


def main() -> None:
    """Main entry point."""
    print(BANNER)

    # Validate configuration
    if not Config.validate():
        return

    agent = Orchestrator()

    while True:
        print("\nSelect a mode:")
        print("  1 — 📚 Research Q&A")
        print("  2 — 📝 Paper Review")
        print("  3 — 🚪 Exit")

        choice = input("\nYour choice (1/2/3): ").strip()

        if choice == "1":
            mode_research_qa(agent)
        elif choice == "2":
            mode_paper_review(agent)
        elif choice == "3":
            print("\nGoodbye! 👋")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main()
