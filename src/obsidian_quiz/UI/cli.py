import sys
import getpass
from InquirerPy import inquirer
from obsidian_quiz.models import Note, Quiz, QuizData
from obsidian_quiz.utils import create_quiz_object
from obsidian_quiz.config.config_loader import MAX_QUESTIONS
from obsidian_quiz.DAL.interfaces import (
    NoteRepository,
    LLMService,
    QuizRepository
)


def get_valid_response(question: str) -> bool:
    while True:
        response = input(question).strip().lower()
        if response in ("y", "n"):
            return response
        print("Please enter a valid response (y/n).")


def select_quiz_mode() -> str:
    mode = inquirer.select(
        message="Select a quiz mode:",
        choices=["Random note", "Select a note"],
        default="Random note",
        pointer="👉"
    ).execute()
    return mode


def get_note_for_selected_mode(mode: str, note_repo: NoteRepository) -> Note:
    match mode:
        case "Random note":
            return note_repo.get_random()
        case "Select a note":
            note_to_id_map = note_repo.get_name_to_id_map()
            chosen_note_id = inquirer.fuzzy(
                message="Search for a note:",
                choices=list(note_to_id_map.keys())
            ).execute()
            return note_repo.get_by_id(note_to_id_map[chosen_note_id])
        case _:
            raise ValueError("Invalid mode inputted")


def get_num_questions() -> int:
    while True:
        user_input_str = input("How many questions would you like? ").strip()
        if not user_input_str.isdigit():
            print("Please enter a valid number of questions...")
            continue
        num_questions = int(user_input_str)
        if num_questions > MAX_QUESTIONS:
            print(f"The maximum number of questions is {MAX_QUESTIONS}.")
            continue
        break
    return num_questions


def print_quiz_title(note_name: str) -> None:
    tabs = "\t" * 3
    print("\n" + tabs + f"{note_name} Quiz!" + tabs)
    print(tabs + "-" * (6 + len(note_name)) + tabs)


def give_quiz(note: Note, quiz: Quiz) -> int:
    print_quiz_title(note.name)

    score = 0
    for count, question in enumerate(quiz.questions, start=1):
        print(f"\tQ{count}: {question.text}\t")

        print("\tPress Enter to see the answer...", end="", flush=True)
        # Used instead of input() so "non-Enter-key" characters do not show.
        getpass.getpass(prompt="")
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\033[K")  # Erases line

        print(f"\tA{count}: {question.answer}\t")
        response = get_valid_response(
            "\tDid you answer correctly? (y/n): "
        )
        score += response == "y"

    return score


def print_quiz_stats(quiz_data: QuizData) -> None:
    quiz_stats = quiz_data.stats
    print(f"\tYou last completed this quiz on {quiz_stats.last_modified}.")
    print(f"\tThe average score for this quiz is {quiz_stats.average:.2f}.")
    num_previous_scores = len(quiz_stats.last_10_scores)
    print(f"\tYour last {num_previous_scores} "
          f"score{'s' if num_previous_scores > 1 else ''} "
          f"are {quiz_stats.last_10_scores}.")


def should_quizzing_continue() -> bool:
    response = get_valid_response("\nWould you like to keep quizzing (y/n)? ")
    return response == "y"


def run_quiz_cli(
    note_repo: NoteRepository,
    llm_service: LLMService,
    quiz_repo: QuizRepository
) -> None:
    try:
        # end argument is to avoid automatic \n ending.
        print("Welcome! ", end="")
        while True:
            mode = select_quiz_mode()
            note = get_note_for_selected_mode(mode, note_repo)
            print(f"You will be quizzed on {note.name}.")

            quiz_data = quiz_repo.get_quiz_data(note)
            cached_quiz = quiz_data.cached_quiz

            use_cache = False
            if cached_quiz is not None:
                # Checks to see if cached quiz should be used instead
                # of generating one with a LLM.
                response = get_valid_response(
                    "\nWould you like to use the cached quiz (y/n)? "
                    )
                use_cache = response == "y"
            if use_cache:
                quiz_string = cached_quiz.quiz_string
                quiz = create_quiz_object(note.name, quiz_string)
                num_questions = len(quiz.questions)
            else:
                num_questions = get_num_questions()
                if num_questions == 0:
                    if should_quizzing_continue():
                        continue
                    print("See you next time!")
                    break

                quiz = llm_service.generate_quiz(
                    note,
                    num_questions
                )

            score = give_quiz(note, quiz)
            print(f"\n\tYou got {score}/{num_questions}!\n")

            if use_cache:
                print_quiz_stats(quiz_data)
                quiz_repo.update_quiz_data_in_storage(quiz_data, score)
            else:
                # Covers two cases:
                # 1. No cached quiz exists yet - creates new entry
                # 2. User chose to regenerate - overwrites existing entry
                quiz_repo.add_quiz_data_to_storage(
                    note,
                    quiz,
                    score
                )

            if not should_quizzing_continue():
                print("See you next time!")
                break

    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")
