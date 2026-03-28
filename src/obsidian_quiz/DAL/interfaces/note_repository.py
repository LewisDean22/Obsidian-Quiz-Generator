from abc import ABC, abstractmethod
from src.obsidian_quiz.models.note import Note, NoteId


class NoteRepository(ABC):
    """
    Abstract repository for accessing notes.
    Implementators must return Note domain objects.
    """
    @abstractmethod
    def get_all_ids(self) -> list[NoteId]:
        """
        Fetches all notes from the repository, returning a
        list of Notes.
        """
        ...

    @abstractmethod
    def get_by_id(self, note_id: NoteId) -> Note | None:
        """
        Returns the Note with the given ID, or None if no note exists
        with that ID.
        """
        ...

    @abstractmethod
    def get_random(self) -> Note:
        """
        Return a Note object built from a random note in the
        repository.
        """
        ...
