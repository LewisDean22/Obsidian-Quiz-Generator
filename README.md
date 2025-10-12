# Obsidian Quiz Generator

![Version](https://img.shields.io/badge/version-0.1.0-8B5CF6?style=for-the-badge)
![MIT License](https://img.shields.io/badge/license-MIT-8B5CF6?style=for-the-badge&logo=appveyor)

**Disclaimer:** This project is not affiliated with, endorsed by, or sponsored by Obsidian.md. It is in fact compatible with any collection of Markdown files.

Obsidian Quiz Generator is a CLI tool that uses OpenAI's GPT-4o mini to create interactive quizzes from your Markdown notes.

### Features

- **Random Quiz Mode** - a random note is selected from your vault and generates a quiz based on its content.
- **Option to Continue Playing** - at the end of a quiz, you choose whether to continue with a quiz on another note or to exit.
- **Customisable Question Count** - input the desired number of questions for the selected note through the CLI. Enter `0` for the option to continue with a different random note.
- **Interactive Questioning** - questions appear one at a time. Press Enter to reveal the answer and self-report whether you answered correctly.

### Installation

> **⚠️ NOTE:** To use Obsidian Quiz Generator, you will need an OpenAI API account and API key. While costs are generally low for moderately sized notes, you are responsible for any usage charges. You can monitor your usage via the OpenAI API Platform dashboard.

1. Clone the repository:
    ```
    git clone https://github.com/LewisDean22/obsidian-quiz-generator.git
    ```
2. Run `poetry install` inside the project's root directory (that with `pyproject.toml`). If you do not have Poetry, install it via pip.
3. Rename `.env_sample` to `.env` and add your own OpenAI API key to its `OPENAI_API_KEY` variable.
4. Rename `config.ini_sample` to `config.ini` and modify the following variables:
    - `vault_directory` - the path to where Markdown files will be sourced from.
    - `minimum_line_count` - below this, a note will not be considered valid for quiz generation.
    - `max_questions` - limits how many questions can be requested through the CLI. This is useful so too many tokens are never outputted by the LLM for a single request!


### Usage

Navigate to the project's root directory and run the following command:

```
poetry run obsidian_quiz
```

**Bonus:** If you are on a Windows device and would like an *Obsidian Quiz Generator shortcut*:

1. Rename `windows_obsidian_quiz.vbs_sample` to  `windows_obsidian_quiz.vbs` and modify the following variables:
    - `strPoetry` - path to your Poetry executable
    - `strProjectDir`- path to this project's directory
2. Create a shortcut to the VBS file and (optionally) set the shortcut icon to the `obsidian-icon.ico` file included in this repository.


### Roadmap

1. Quiz Statistics:
    - Use a JSON to store last-k quiz scores for each note, along with each note's average quiz score and the overall average across all Obsidian quizzes taken.
    - Display these statistics at the end of each quiz.
2. Additional Quiz Modes:
    - Search Mode – use a fuzzy search to find Markdown notes to be quizzed on. Navigate the top-k matches with arrow keys to select the desired note.
    - Spaced Repetition Mode (for more effective learning).
    - RAG-sourced Quizzes - store the Obsidian vault in a vector database and generate quizzes on an arbitrary topic according to the user's query.

---

Created by [Lewis Dean](https://www.lewismdean.uk/)
