from obsidian_quiz.DAL.interfaces import QuizRepository
from obsidian_quiz.models import QuizStats, CachedQuiz, Note, QuizData, Quiz
from obsidian_quiz.utils import convert_to_slug, hash_content
import pathlib
import json
from datetime import date
from collections import deque

STORAGE_PATH = pathlib.Path(
    __file__).resolve().parent.parent / "storage" / "quiz_data.json"


class JSONQuizRepository(QuizRepository):
    def __init__(
        self,
        storage_filepath: pathlib.Path = STORAGE_PATH
    ):
        self._storage_filepath = storage_filepath

    def _load_json(self):
        if not self._storage_filepath.exists():
            return {}  # file will be created when first save is made
        with open(self._storage_filepath) as f:
            return json.load(f)

    def _save_json(self, data: dict) -> None:
        # JSONs must be fully re-written every time,
        # they cannot be written to by key.
        with open(self._storage_filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    def _get_stats(self, quiz_data: dict) -> QuizStats | None:
        quiz_stats = quiz_data.get("stats")
        if quiz_stats is None:
            return None
        return QuizStats(**quiz_stats)

    def _get_cached_quiz(
        self, note: Note,
        quiz_data: dict
    ) -> CachedQuiz | None:
        quiz_cache = quiz_data.get("cache")
        if quiz_cache is None:
            return None
        note_hash = hash_content(note.content)
        print(note_hash)
        if note_hash != quiz_cache["note_hash"]:
            return None  # note changed so quiz is stale
        return CachedQuiz(**quiz_cache)

    def get_quiz_data(self, note: Note) -> QuizData:

        data = self._load_json()
        note_slug = convert_to_slug(note.name)
        quiz_data = data.get(note_slug)
        if quiz_data is None:
            return QuizData(note_slug, None, None)
        return QuizData(
            note_slug,
            self._get_stats(quiz_data),
            self._get_cached_quiz(note, quiz_data)
        )

    def add_quiz_data_to_storage(
        self,
        note: Note,
        quiz: Quiz,
        score: int
    ) -> None:
        data = self._load_json()
        note_slug = convert_to_slug(note.name)

        stats_entry = {
            "average": score,
            "count": 1,
            "last_10_scores": [score],  # JSON cannot store tuples
            "last_modified": date.today().isoformat()
        }
        cache_entry = {
            "note_hash": hash_content(note.content),
            "quiz_string": quiz.quiz_string
        }
        data[note_slug] = {
            "stats": stats_entry,
            "cache": cache_entry
        }
        self._save_json(data)

    def update_quiz_data_in_storage(
        self,
        existing_data: QuizData,
        score: int,
    ) -> None:
        data = self._load_json()
        note_slug = existing_data.note_slug
        existing_stats = existing_data.stats

        new_count = existing_stats.count + 1
        new_average = (
            existing_stats.average*existing_stats.count + score
            ) / new_count
        scores = deque(existing_stats.last_10_scores, maxlen=10)
        scores.appendleft(score)
        new_last_10_scores = list(scores)

        stats_entry = {
            "average": new_average,
            "count": new_count,
            "last_10_scores": new_last_10_scores,
            "last_modified": date.today().isoformat()
        }
        data[note_slug] = {
            **data[note_slug],  # preserve existing entries
            "stats": stats_entry  # overwrite stats
        }
        self._save_json(data)
