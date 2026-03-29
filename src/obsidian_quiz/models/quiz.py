from dataclasses import dataclass
# Should I use the noteId for the quiz ID?
# No because I could create two notes from the same
# quiz, just with different amount of Qs
# If I implemented a Quiz ID, would I need an autoincrementer?


@dataclass(frozen=True)
class Question:
    text: str
    answer: str


@dataclass(frozen=True)
class Quiz:
    note_name: str
    questions: tuple[Question, ...]
    # tuple since you can append to lists,
    # which defeats the purpose of frozen=True
