import os


def get_note_name_from_filepath(md_filepath: str) -> str:
    def format_word(word: str) -> str:
        has_multiple_capitals = sum(1 for c in word if c.isupper()) > 1
        return word if has_multiple_capitals else word.capitalize()

    name = os.path.basename(md_filepath).removesuffix(".md")
    return " ".join(format_word(word) for word in name.split())


def convert_to_slug(string: str) -> str:
    return string.lower().strip().replace(" ", "_")
