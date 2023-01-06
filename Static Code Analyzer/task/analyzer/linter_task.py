from dataclasses import dataclass
from typing import Callable, List, Iterable
from linters import Linters


@dataclass
class LinterBase:
    code: str
    message: str


@dataclass
class LinterTask(LinterBase):
    exec: Callable[[List[str]], Iterable[int]]


@dataclass
class LinterError(LinterBase):
    line_number: int

    def __str__(self):
        return f'Line {self.line_number}: {self.code} {self.message}'


LINTER_TASKS = [
    LinterTask('S001', 'Too long', Linters.s001),
    LinterTask('S002', 'Indentation is not a multiple of four', Linters.s002),
    LinterTask(
        's003', 'Unnecessary semicolon after a statement', Linters.s003),
    LinterTask(
        's004', 'Less than two spaces before inline comments', Linters.s004),
    LinterTask('s005', 'TODO found', Linters.s005),
    LinterTask('s006', 'More than two blank lines used before this line',
               Linters.s006)]
