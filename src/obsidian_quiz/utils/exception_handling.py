from typing import Any


def assert_type(value: Any, expected: Any, name: str = "value") -> None:
    if not isinstance(value, expected):
        raise TypeError(f"""{name} must be {expected.__name__},
                        got {type(value).__name__}""")
