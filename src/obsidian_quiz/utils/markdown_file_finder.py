import os
import random
from obsidian_quiz.utils.text_formatting import (
    convert_to_title,
    remove_md_extension,
)
from typing import Final
import pathlib
from obsidian_quiz.config_loader import VAULT_DIRECTORY, MINIMUM_LINE_COUNT


VAULT_DIRECTORY_PATH: Final[pathlib.Path] = pathlib.Path(
    __file__).resolve().parent.parent.parent.parent / VAULT_DIRECTORY


def try_adding_file_to_dict(filename: str, dirpath: str,
                            markdown_files: dict[str, str],
                            min_lines: int = MINIMUM_LINE_COUNT) -> None:

    if not filename.endswith(".md"):
        return

    full_path = os.path.join(dirpath, filename)
    try:
        with open(full_path, "r", encoding="utf-8") as f:
            line_count = sum(1 for _ in f)
            if line_count > min_lines:
                markdown_files[filename] = full_path
    except FileNotFoundError:
        print(f"Warning: File not found -> {full_path}")
    except PermissionError:
        print(f"Warning: Permission denied -> {full_path}")


def find_all_valid_markdown_files(
    root_dir: pathlib.Path = VAULT_DIRECTORY_PATH
) -> dict[str, str]:

    markdown_files: dict[str, str] = {}
    # os.walk recursively goes through all subdirectories.
    for dirpath, _, filenames in os.walk(root_dir):
        for file in filenames:
            # Markdown files dict gets passed by reference
            # so modifications persist outside function
            try_adding_file_to_dict(file, dirpath, markdown_files)
    return markdown_files


def get_random_note_content() -> tuple[str, str]:
    markdown_filepaths = find_all_valid_markdown_files()
    if not markdown_filepaths:
        raise FileNotFoundError("No valid markdown files found for quiz.")

    chosen_note_name = random.choice(list(markdown_filepaths.keys()))
    cleaned_note_name = convert_to_title(remove_md_extension(chosen_note_name))

    chosen_note_path = markdown_filepaths[chosen_note_name]
    with open(chosen_note_path, "r", encoding="utf-8") as f:
        note_content = f.read()
    return cleaned_note_name, note_content
