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
    file_name: str
    line_number: int

    def __str__(self):
        return f'{self.file_name}: Line {self.line_number}: {self.code} ' \
               f'{self.message}'


LINTER_TASKS = [
    LinterTask('S001', 'Too long', Linters.s001),
    LinterTask('S002', 'Indentation is not a multiple of four', Linters.s002),
    LinterTask(
        'S003', 'Unnecessary semicolon after a statement', Linters.s003),
    LinterTask(
        'S004', 'Less than two spaces before inline comments', Linters.s004),
    LinterTask('S005', 'TODO found', Linters.s005),
    LinterTask('S006', 'More than two blank lines used before this line',
               Linters.s006),
    LinterTask('S007', "Too many spaces after 'class|def'", Linters.s007),
    LinterTask('S008', 'Class name should use CamelCase', Linters.s008),
    LinterTask('S009', 'Function name should be written in snake_case',
               Linters.s009)]
