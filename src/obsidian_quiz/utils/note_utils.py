import os


def get_note_name_from_filepath(md_filepath: str) -> str:
    name = os.path.basename(md_filepath).removesuffix(".md")
    words = name.split()
    return " ".join(
        word if word.isupper() else word.capitalize()
        for word in words
    )
