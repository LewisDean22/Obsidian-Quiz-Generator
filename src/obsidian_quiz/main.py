"""
obsidian_quiz.main
------------------

A CLI tool which generates quizzes from your Obsidian notes using
OpenAI's GPT-4o mini. For more details, see the README.

Author: Lewis Dean
License: MIT
Version: 0.1.0
"""
from obsidian_quiz.DAL import OpenAIService, MdNoteRepository
from obsidian_quiz.UI.cli import run_quiz_cli


def main() -> None:
    open_ai_service = OpenAIService()
    note_repo = MdNoteRepository()
    run_quiz_cli(note_repo, open_ai_service)


if __name__ == "__main__":
    main()
