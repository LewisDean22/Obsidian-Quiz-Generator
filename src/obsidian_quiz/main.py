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
    get_random_note_content,
)
from obsidian_quiz.utils.user_input_handling import (
    setup_quiz_details,
    give_quiz,
    should_quizzing_continue,
)
from obsidian_quiz.core.ai_logic import get_quiz
from obsidian_quiz.config_loader import MAX_QUESTIONS
from typing import Final


SYSTEM_PROMPT_TEMPLATE: Final[str] = """You are a quiz generator. Make a
{num_questions}-question quiz strictly in the following format:
Q1: Question text
A1: Answer text
Q2: Question text
A2: Answer text
… and so on for all {num_questions} questions.
Only respond with the quiz in this exact format. Questions should be general
and not specific to a given project, but should come
directly from content found within the inputted text.
"""


def main(system_prompt_template: str = SYSTEM_PROMPT_TEMPLATE,
         max_questions: int = MAX_QUESTIONS) -> None:
    try:
        # end argument is to avoid automatic \n ending.
        print("Welcome! ", end="")
        while True:
            note_name, note_content = get_random_note_content()
            system_prompt, num_questions = setup_quiz_details(
                note_name, max_questions, system_prompt_template)
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
