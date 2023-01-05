from typing import List

from linter_task import LinterError, LINTER_TASKS


def main():
    file_path = input()
    errors: List[LinterError] = []
    with open(file_path, 'r') as f:
        text = f.readlines()
    for task in LINTER_TASKS:
        errors.extend(LinterError(task.code, task.message, n)
                      for n in task.func(text))
    # todo maybe sort by line (in the future)

    if errors:
        print(*errors, sep='\n')


if __name__ == '__main__':
    main()
