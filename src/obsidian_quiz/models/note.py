from dataclasses import dataclass


@dataclass(frozen=True)
class NoteId():
    value: str | int


# Used frozen because the Note object should be
# re-created if the note itself is modified at all.
@dataclass(frozen=True)
class Note():
    id: NoteId
    name: str
    content: str
