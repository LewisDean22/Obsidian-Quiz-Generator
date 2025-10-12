from obsidian_quiz.utils.exception_handling import assert_type


def remove_md_extension(filename: str) -> str:
    assert_type(filename, str, "Filename")
    filename = filename.strip()
    if not filename.endswith(".md"):
        raise ValueError(f"Filename does not end with '.md': {filename}")
    return filename[:-3]  # removes the last 3 characters


def convert_to_title(text: str) -> str:
    assert_type(text, str, "Title text")
    words = text.split()  # split by spaces
    new_words = [
        word if word.isupper() else word.capitalize()
        for word in words
    ]
    return " ".join(new_words)


def print_quiz_title(note_name: str) -> None:
    assert_type(note_name, str, "Note name")
    tabs = "\t" * 3
    print("\n" + tabs + f"{note_name} Quiz!" + tabs)
    print(tabs + "-" * (6 + len(note_name)) + tabs)
