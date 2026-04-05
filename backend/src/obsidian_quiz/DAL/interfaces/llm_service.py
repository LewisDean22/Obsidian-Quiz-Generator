from abc import ABC, abstractmethod
from obsidian_quiz.models import Note, Quiz


class LLMService(ABC):

    @abstractmethod
    def generate_quiz(self, note: Note, num_questions: int) -> Quiz:
        """
        Create llm_utils.py and put q/a split regex in there?
        """
        ...
