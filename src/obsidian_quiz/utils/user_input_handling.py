import sys
from obsidian_quiz.utils.text_formatting import print_quiz_title
import getpass
from InquirerPy import inquirer


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


def setup_quiz_details(note_name: str, max_questions: int,
                       system_prompt_template: str) -> tuple[str, int]:
    print(f"You will be quizzed on {note_name}.")
    while True:
        user_input_str = input("How many questions would you like? ").strip()
        if not user_input_str.isdigit():
            print("Please enter a valid number of questions...")
            continue
        user_input = int(user_input_str)
        if user_input > max_questions:
            print(f"The maximum number of questions is {max_questions}.")
            continue
        system_prompt_vals = {"num_questions": user_input}
        break

    # Unpacked mapping passed into format to populate the template.
    system_prompt = system_prompt_template.format(**system_prompt_vals)
    return system_prompt, user_input  # user_input = number of questions


def give_quiz(note_name: str, questions: list[str], answers: list[str]) -> int:
    print_quiz_title(note_name)

    score = 0
    for count, (q, a) in enumerate(zip(questions, answers), start=1):
        print(f"\tQ{count}: {q}\t")

        print("\tPress Enter to see the answer...", end="", flush=True)
        # Used instead of input() so "non-Enter-key" characters do not show.
        getpass.getpass(prompt="")
        sys.stdout.write("\033[F")  # Cursor up one line
        sys.stdout.write("\033[K")  # Erases line

        print(f"\tA{count}: {a}\t")
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
