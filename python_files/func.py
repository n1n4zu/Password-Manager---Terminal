from sys import platform
from os import system


def clear() -> int:
    """
    Clear screen
    :return: Code of process or code of finished command
    """
    if platform == 'win32':
        return system('cls')
    return system('clear')


class NoKeyError(Exception):
    """
    Exception raised when no key is found
    """
    pass
