from typing import List, Iterable


def too_long_linter(text: List[str]) -> Iterable[int]:
    return (i for i, line in enumerate(text, start=1) if len(line) > 79)
