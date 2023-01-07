import re
from typing import List, Iterable, Callable

PREDICATE = Callable[[List[str], int, str], bool]

S002 = re.compile(r'^ *')
S003 = re.compile(r'^[^#]*;(\s*$| +#)')
S004 = re.compile(r'^[^#]*[^# ]+ ?#')
S005 = re.compile(r'#.*\btodo\b', re.IGNORECASE)
S006_3_EMPTY = ['\n'] * 3
S007 = re.compile(r'(class|def) {2,}\w')
S008 = re.compile(r'class +([a-z]\w*\b|[A-Z](?:\w*_\w*)\b)')
S009 = re.compile(r'def +([A-Z][a-z]*)+')

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

    @staticmethod
    def s007(text: List[str]) -> Iterable[int]:
        """
        Check if there are two or more spaces between class|def and their names
        """
        return Linters.pattern(text, P_S007)

    @staticmethod
    def s008(text: List[str]) -> Iterable[int]:
        """Check if there are some none-camel-case class names"""
        return Linters.pattern(text, P_S008)

    @staticmethod
    def s009(text: List[str]) -> Iterable[int]:
        """Check if there are some camel-case function names"""
        return Linters.pattern(text, P_S009)
