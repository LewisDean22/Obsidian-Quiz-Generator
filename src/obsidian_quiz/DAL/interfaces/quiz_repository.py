"""
TODO - could add overall_stats which gets average across
entire vault. Is this a good idea for a JSON implementor?
Hard to query...
"""
from abc import ABC, abstractmethod
from obsidian_quiz.models import QuizStats, CachedQuiz, Note


class QuizRepository(ABC):
    @abstractmethod
    def get_quiz_data(
        self,
        note: Note
    ) -> tuple[QuizStats | None, CachedQuiz | None]: ...

    @abstractmethod
    def update_stats(
        self,
        existing_stats: QuizStats,
        score: int,
    ) -> None: ...

    @abstractmethod
    def update_cached_quiz(
        self,
        note: Note,
        quiz_string: str,
    ) -> None: ...
