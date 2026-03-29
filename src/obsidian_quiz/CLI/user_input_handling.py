import sys
import getpass
from InquirerPy import inquirer
from obsidian_quiz.models import Note, Quiz
from obsidian_quiz.config.config_loader import MAX_QUESTIONS
from obsidian_quiz.DAL import MdNoteRepository
from obsidian_quiz.utils.exception_handling import assert_type


def is_user_response_valid(user_response: str) -> bool:
    return user_response in ("y", "n")


def select_quiz_mode() -> str:
    mode = inquirer.select(
        message="Select a quiz mode:",
        choices=["Random note", "Select a note"],
        default="Random note",
        pointer="👉"
    ).execute()
    return mode


def get_note_for_selected_mode(mode: str, note_repo: MdNoteRepository) -> Note:
    match mode:
        case "Random note":
            return note_repo.get_random()
        case "Select a note":
            note_to_id_map = note_repo.get_name_to_id_map()
            chosen_note_id = inquirer.fuzzy(
                message="Search for a Markdown note:",
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
    assert_type(note_name, str, "Note name")
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
        while True:
            user_response = input(
                "\tDid you answer correctly? (y/n): "
            ).strip().lower()

            if not is_user_response_valid(user_response):
                print("\tPlease enter a valid reponse (y/n)")
                continue
            score += user_response == "y"
            break

    return score


def should_quizzing_continue() -> bool:
    while True:
        should_continue = input("\nWould you like to keep quizzing (y/n)? ")
        if not is_user_response_valid(should_continue):
            print("Please enter a valid reponse (y/n): ")
            continue
        break
    return True if should_continue == "y" else False
