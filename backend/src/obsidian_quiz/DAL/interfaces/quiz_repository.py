"""
TODO - could add overall_stats which gets average across
entire vault. Is this a good idea for a JSON implementor?
Hard to query...
"""
from abc import ABC, abstractmethod
from obsidian_quiz.models import Note, QuizData, Quiz


class QuizRepository(ABC):
    @abstractmethod
    def get_quiz_data(self, note: Note) -> QuizData: ...

    @abstractmethod
    def add_quiz_data_to_storage(
        self,
        note: Note,
        quiz: Quiz,
        score: int
    ) -> None:
        """
        Used when no existing stats or cached quiz in the quiz
        repository. Also used if the quiz has become stale because
        of the user opting to regenerate or because of changes to the .md
        file.
        """
        ...

    @abstractmethod
    def update_quiz_data_in_storage(
        self,
        existing_data: QuizData,
        score: int
    ) -> None:
        """
        Used for updating an existing entry in the quiz repository.
        """
        ...
