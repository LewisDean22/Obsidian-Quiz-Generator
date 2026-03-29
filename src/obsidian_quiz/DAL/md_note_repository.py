import os
import random
from obsidian_quiz.DAL.interfaces import NoteRepository
from obsidian_quiz.models.note import Note, NoteId
from obsidian_quiz.utils.note_utils import get_note_name_from_filepath
from obsidian_quiz.config.config_loader import MINIMUM_LINE_COUNT


class MdNoteRepository(NoteRepository):
    def __init__(self, vault_filepath: str):
        self.vault_filepath = vault_filepath
        self._note_ids = self._load_note_ids()
        # eager loading ids and lazy loading content

    def _load_note_ids(self) -> set[NoteId]:
        note_ids = set()
        for dirpath, _, filenames in os.walk(self.vault_filepath):
            for filename in filenames:
                full_path = os.path.join(dirpath, filename)
                if self._is_valid_md_note(full_path):
                    note_ids.add(NoteId(full_path))
        if not note_ids:
            raise ValueError("No valid .md files found for quiz.")
        return note_ids

    def _is_valid_md_note(self, full_path: str) -> bool:
        if not full_path.endswith(".md"):
            return False

        try:
            with open(full_path, "r", encoding="utf-8") as f:
                return sum(1 for _ in f) >= MINIMUM_LINE_COUNT
        except (FileNotFoundError, PermissionError) as e:
            print(f"Failed to load .md file from vault: {e}")
            return False

    def _create_note(self, note_id: NoteId) -> Note:
        with open(note_id.value, "r", encoding="utf-8") as f:
            return Note(
                id=note_id,
                name=get_note_name_from_filepath(note_id.value),
                content=f.read()
            )

    # PUBLIC

    def get_all_ids(self) -> set[NoteId]:
        return self._note_ids

    def get_by_id(self, note_id: NoteId) -> Note | None:
        if note_id in self._note_ids:
            return self._create_note(note_id)
        return None

    def get_random(self) -> Note:
        note_id = random.choice(list(self._note_ids))
        return self._create_note(note_id)
