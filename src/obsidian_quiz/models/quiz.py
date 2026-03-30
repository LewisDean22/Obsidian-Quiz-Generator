from dataclasses import dataclass
from datetime import date
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


@dataclass(frozen=True)
class QuizStats:
    # not used NoteId since implementor determines id type
    # which means changing Note Repo implementor would make
    # existing storage inaccessible (change in key)
    note_slug: str
    average: float
    count: int
    last_10_scores: tuple[int, ...]
    last_modified: date


@dataclass(frozen=True)
class CachedQuiz:
    note_hash: str
    quiz_string: str
