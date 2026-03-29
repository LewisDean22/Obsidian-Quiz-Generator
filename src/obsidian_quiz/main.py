"""
obsidian_quiz.main
------------------

A CLI tool which generates quizzes from your Obsidian notes using
OpenAI's GPT-4o mini. For more details, see the README.

Author: Lewis Dean
License: MIT
Version: 0.1.0
"""
from obsidian_quiz.CLI.user_input_handling import (
    get_note_for_selected_mode,
    get_num_questions,
    give_quiz,
    should_quizzing_continue,
    select_quiz_mode
)
from obsidian_quiz.DAL import OpenAIService, MdNoteRepository


def main() -> None:
    open_ai_service = OpenAIService()
    note_repo = MdNoteRepository()
    try:
        # end argument is to avoid automatic \n ending.
        print("Welcome! ", end="")
        while True:
            mode = select_quiz_mode()
            note = get_note_for_selected_mode(mode, note_repo)
            print(f"You will be quizzed on {note.name}.")
            num_questions = get_num_questions()

            if num_questions == 0:
                if should_quizzing_continue():
                    continue
                print("See you next time!")
                break

            quiz = open_ai_service.generate_quiz(note, num_questions)
            score = give_quiz(note, quiz)
            print(f"\n\tYou got {score}/{num_questions}!")

            if not should_quizzing_continue():
                print("See you next time!")
                break

    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")
    except Exception as e:
        print(f"\nUnexpected error: {e}")


if __name__ == "__main__":
    main()
