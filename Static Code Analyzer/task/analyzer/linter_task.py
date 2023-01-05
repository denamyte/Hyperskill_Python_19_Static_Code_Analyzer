from dataclasses import dataclass
from typing import Callable, List, Iterable
from linters import too_long_linter


@dataclass
class LinterBase:
    code: str
    message: str


@dataclass
class LinterTask(LinterBase):
    func: Callable[[List[str]], Iterable[int]]


@dataclass
class LinterError(LinterBase):
    line_number: int

    def __str__(self):
        return f'Line {self.line_number}: {self.code} {self.message}'


LINTER_TASKS = [LinterTask('S001', 'Too long', too_long_linter)]
