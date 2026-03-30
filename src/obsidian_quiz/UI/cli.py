import sys
import getpass
from InquirerPy import inquirer
from obsidian_quiz.models import Note, Quiz
from obsidian_quiz.config.config_loader import MAX_QUESTIONS
from obsidian_quiz.DAL.interfaces import NoteRepository, LLMService


def is_response_valid(response: str) -> bool:
    return response in ("y", "n")


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
        while True:
            user_response = input(
                "\tDid you answer correctly? (y/n): "
            ).strip().lower()

            if not is_response_valid(user_response):
                print("\tPlease enter a valid response (y/n)")
                continue
            score += user_response == "y"
            break

    return score


def should_quizzing_continue() -> bool:
    while True:
        response = input("\nWould you like to keep quizzing (y/n)? ")
        if is_response_valid(response):
            return response == "y"
        print("Please enter a valid response (y/n).")


def run_quiz_cli(note_repo: NoteRepository, llm_service: LLMService) -> None:
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

            quiz = llm_service.generate_quiz(note, num_questions)
            score = give_quiz(note, quiz)
            print(f"\n\tYou got {score}/{num_questions}!")

            if not should_quizzing_continue():
                print("See you next time!")
                break

    except KeyboardInterrupt:
        print("\nQuiz interrupted. Goodbye!")
