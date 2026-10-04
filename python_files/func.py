from sys import platform
from os import system


def clear() -> int:
    if platform == 'win32':
        return system('cls')
    return system('clear')
