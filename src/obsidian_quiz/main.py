"""
obsidian_quiz.main
------------------

A CLI tool which generates quizzes from your Obsidian notes using
OpenAI's GPT-4o mini. For more details, see the README.

Author: Lewis Dean
License: MIT
Version: 0.1.0
"""
from obsidian_quiz.utils.markdown_file_finder import (
    get_note_for_selected__mode,
)
from obsidian_quiz.utils.user_input_handling import (
    setup_quiz_details,
    give_quiz,
    should_quizzing_continue,
    select_quiz_mode,
)
from obsidian_quiz.core.ai_logic import get_quiz
from obsidian_quiz.config.config_loader import MAX_QUESTIONS
from obsidian_quiz.config.prompts import SYSTEM_PROMPT_TEMPLATE


def main(system_prompt_template: str = SYSTEM_PROMPT_TEMPLATE,
         max_questions: int = MAX_QUESTIONS) -> None:
    try:
        # end argument is to avoid automatic \n ending.
        print("Welcome! ", end="")
        while True:
            mode = select_quiz_mode()
            note_name, note_content = get_note_for_selected__mode(mode)
            system_prompt, num_questions = setup_quiz_details(
                note_name, max_questions, system_prompt_template)

            if num_questions == 0:
                if should_quizzing_continue():
                    continue
                print("See you next time!")
                break

            questions, answers = get_quiz(note_content, system_prompt)
            score = give_quiz(note_name, questions, answers)
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
