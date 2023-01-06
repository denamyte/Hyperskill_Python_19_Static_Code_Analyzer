import re
from typing import List, Iterable, Callable

PREDICATE = Callable[[List[str], int, str], bool]

S002 = re.compile('^ *')
S003 = re.compile('^[^#]*;(\\s*$| +#)')
S004 = re.compile('^[^#]*[^# ]+ ?#')
S005 = re.compile('#.*\\btodo\\b', re.IGNORECASE)
S006_3_EMPTY = ['\n'] * 3
P_S001: PREDICATE = lambda text, i, line: len(line) > 79
P_S002: PREDICATE = lambda text, i, line: bool(S002.search(line).end() % 4)
P_S003: PREDICATE = lambda text, i, line: bool(S003.search(line))
P_S004: PREDICATE = lambda text, i, line: bool(S004.search(line))
P_S005: PREDICATE = lambda text, i, line: bool(S005.search(line))
P_S006: PREDICATE = lambda text, i, line: i > 3 and len(line.lstrip()) \
                                          and text[i - 4:i - 1] == S006_3_EMPTY


class Linters:
    @staticmethod
    def pattern(text: List[str], func: PREDICATE) -> Iterable[int]:
        return (i for i, line in enumerate(text, start=1)
                if func(text, i, line))

    @staticmethod
    def s001(text: List[str]) -> Iterable[int]:
        """Check if the line length is 80 or more"""
        return Linters.pattern(text, P_S001)

    @staticmethod
    def s002(text: List[str]) -> Iterable[int]:
        """Check if the line indentation is not multiple of four"""
        return Linters.pattern(text, P_S002)

    @staticmethod
    def s003(text: List[str]) -> Iterable[int]:
        """Check if there is an unnecessary semicolon after a statement"""
        return Linters.pattern(text, P_S003)

    @staticmethod
    def s004(text: List[str]) -> Iterable[int]:
        """Check if there are less than two spaces before an inline comment"""
        return Linters.pattern(text, P_S004)

    @staticmethod
    def s005(text: List[str]) -> Iterable[int]:
        """Check if there are TODOs in a comment"""
        return Linters.pattern(text, P_S005)

    @staticmethod
    def s006(text: List[str]) -> Iterable[int]:
        """Check if a non-empty line is preceded by 3 or more empty lines"""
        return Linters.pattern(text, P_S006)
