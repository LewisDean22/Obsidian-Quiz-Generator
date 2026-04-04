from dataclasses import dataclass
from datetime import date
# Should I use the noteId for the quiz ID?
# No because I could create two notes from the same
# quiz, just with different amount of Qs


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
    quiz_string: str  # raw LLM output, preserved for caching


@dataclass(frozen=True)
class QuizStats:
    average: float
    count: int
    last_10_scores: tuple[int, ...]
    last_modified: date  # TODO - I think this is actually an ISO date string


@dataclass(frozen=True)
class CachedQuiz:
    note_hash: str
    quiz_string: str


@dataclass(frozen=True)
class QuizData:
    # not used NoteId since implementor determines id type
    # which means changing Note Repo implementor would make
    # existing storage inaccessible (change in key)
    note_slug: str
    stats: QuizStats | None
    cached_quiz: CachedQuiz | None
