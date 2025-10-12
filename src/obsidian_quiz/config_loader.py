import configparser
import pathlib
from typing import Final


config = configparser.ConfigParser()
config.read(
    pathlib.Path(__file__).resolve().parent.parent.parent / "config.ini")

MAX_QUESTIONS: Final[int] = config.getint("quiz_settings", "max_questions",
                                          fallback=5)
MINIMUM_LINE_COUNT: Final[int] = config.getint("quiz_settings",
                                               "minimum_line_count",
                                               fallback=3)
VAULT_DIRECTORY: Final[str] = config.get("quiz_settings", "vault_directory",
                                         fallback="./")
