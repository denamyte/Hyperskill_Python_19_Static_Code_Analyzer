import ast
import re
from dataclasses import dataclass
from typing import List, Iterable, Callable, Pattern

PREDICATE = Callable[[List[str], int, str], bool]


@dataclass
class LinterBase:
    code: str
    message: str


@dataclass
class LinterTask(LinterBase):
    test: PREDICATE


@dataclass
class LinterError(LinterBase):
    file_name: str
    line_number: int

    def __str__(self):
        return f'{self.file_name}: Line {self.line_number}: {self.code} ' \
               f'{self.message}'


S002 = re.compile(r'^ *')
S003 = re.compile(r'^[^#]*;(\s*$| +#)')
S004 = re.compile(r'^[^#]*[^# ]+ ?#')
S005 = re.compile(r'#.*\btodo\b', re.IGNORECASE)
S006_3_EMPTY = ['\n'] * 3
S007 = re.compile(r'(class|def) {2,}\w')
S008 = re.compile(r'class +([a-z]\w*\b|[A-Z](?:\w*_\w*)\b)')
S009 = re.compile(r'def +([A-Z][a-z]*)+')
S010 = re.compile(r'([A-Z][a-z]*)+')
S011 = S010

P_S001: PREDICATE = lambda text, i, line: len(line) > 79
P_S002: PREDICATE = lambda text, i, line: bool(S002.search(line).end() % 4)
P_S003: PREDICATE = lambda text, i, line: bool(S003.search(line))
P_S004: PREDICATE = lambda text, i, line: bool(S004.search(line))
P_S005: PREDICATE = lambda text, i, line: bool(S005.search(line))
P_S006: PREDICATE = lambda text, i, line: i > 3 and len(line.lstrip()) \
                                          and text[i - 4:i - 1] == S006_3_EMPTY
P_S007: PREDICATE = lambda text, i, line: bool(S007.search(line))
P_S008: PREDICATE = lambda text, i, line: bool(S008.search(line))
P_S009: PREDICATE = lambda text, i, line: bool(S009.search(line))

LINTER_TASKS = [
    LinterTask('S001', 'Too long', P_S001),
    LinterTask('S002', 'Indentation is not a multiple of four', P_S002),
    LinterTask('S003', 'Unnecessary semicolon after a statement', P_S003),
    LinterTask(
        'S004', 'Less than two spaces before inline comments', P_S004),
    LinterTask('S005', 'TODO found', P_S005),
    LinterTask(
        'S006', 'More than two blank lines used before this line', P_S006),
    LinterTask('S007', "Too many spaces after 'class|def'", P_S007),
    LinterTask('S008', 'Class name should use CamelCase', P_S008),
    LinterTask(
        'S009', 'Function name should be written in snake_case', P_S009)]


class Linters:
    @staticmethod
    def examine_text(text: List[str], file_name: str) -> Iterable[LinterError]:
        errors: List[LinterError] = []
        for i, line in enumerate(text, start=1):
            errors.extend(LinterError(task.code, task.message, file_name, i)
                          for task in LINTER_TASKS if task.test(text, i, line))
        errors.extend(Linters._examine_with_ast(text, file_name))
        return errors

    @staticmethod
    def _examine_with_ast(text: List[str], file_name: str) \
            -> Iterable[LinterError]:
        errors: List[LinterError] = []
        for node in ast.walk(ast.parse(''.join(text))):
            if isinstance(node, ast.FunctionDef):
                func: ast.FunctionDef = node
                var_names = []
                for arg in func.args.args:
                    if S010.search(arg.arg):
                        errors.append(LinterError(
                            'S010',
                            f"Argument name '{arg.arg}' should be "
                            'written in snake_case', file_name,
                            arg.lineno))
                for item in func.body:
                    if isinstance(item, ast.Assign):
                        for target in item.targets:
                            name = target.attr if isinstance(target, ast.Attribute) else target.id
                            if name not in var_names:
                                if S011.search(name):
                                    errors.append(LinterError('S011', f"Variable '{name}' should be written in snake_case", file_name, item.lineno))
                                var_names.append(name)
                for value in func.args.defaults:
                    if isinstance(value, (ast.List, ast.Dict, ast.Set)):
                        errors.append(LinterError(
                            'S012', 'The default argument value is mutable',
                            file_name, func.lineno))
                        break
        return errors
