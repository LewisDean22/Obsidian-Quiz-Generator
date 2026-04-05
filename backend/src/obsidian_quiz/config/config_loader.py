import configparser
import pathlib


config = configparser.ConfigParser()
config_path = pathlib.Path(__file__).resolve().parent / "config.ini"
if not config_path.exists():
    raise FileNotFoundError(
        f"config.ini not found at {config_path}. "
        "Rename config.ini_sample to config.ini and fill in your settings."
    )

config.read(config_path)

MAX_QUESTIONS = config.getint("quiz_settings", "max_questions",
                              fallback=5)
MINIMUM_LINE_COUNT = config.getint("quiz_settings",
                                   "minimum_line_count",
                                   fallback=3)

try:
    VAULT_DIRECTORY = config.get("quiz_settings", "vault_directory")
except (configparser.NoSectionError, configparser.NoOptionError):
    raise ValueError(
        f"vault_directory must be set in {config_path} "
        "under [quiz_settings]"
    )
