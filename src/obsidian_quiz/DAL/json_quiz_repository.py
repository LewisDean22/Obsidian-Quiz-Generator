from obsidian_quiz.DAL.interfaces import QuizRepository
from obsidian_quiz.models import QuizStats, CachedQuiz, Note
from obsidian_quiz.utils.note_utils import convert_to_slug
import pathlib
import json

STORAGE_PATH = pathlib.Path(
    __file__).resolve().parent.parent / "storage" / "quiz_data.json"


class JSONQuizRepository(QuizRepository):
    def __init__(
        self,
        storage_filepath: pathlib.Path = STORAGE_PATH
    ):
        self._storage_filepath = storage_filepath

    def _get_stats(self, quiz_data: dict) -> QuizStats | None:
        quiz_stats = quiz_data.get("stats")
        if quiz_stats is None:
            return None
        # can build QuizStats using keyword arguments
        return QuizStats(**quiz_stats)

    def _get_cached_quiz(self, note: Note) -> CachedQuiz | None:
        # Need to use hash here to check if a new quiz is needed
        # will always be a cached quiz but return none if quiz
        # is stale
        pass

    def get_quiz_data(
        self,
        note: Note
    ) -> tuple[QuizStats | None, CachedQuiz | None]:
        with open(self._storage_filepath) as f:
            data = json.load(f)
        note_slug = convert_to_slug(note.name)
        quiz_data = data.get(note_slug)
        if quiz_data is None:
            return (None, None)
        return self._get_stats(quiz_data), self._get_cached_quiz(quiz_data)

    def update_stats(
        self,
        existing_stats: QuizStats,
        score: int,
    ) -> None: ...

    def update_cached_quiz(
        self,
        note: Note,
        quiz_string: str,
    ) -> None:
        # create a note hash from the Note content
        # save quiz string
        pass
