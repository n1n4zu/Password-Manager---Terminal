import secrets
import string
import pyperclip as pcp
import json as js
from time import sleep
from python_files.func import *


setting = js.load(open('json_files/settings.json'))


def gen_pass(x: int = 20) -> str:
    chars = string.ascii_letters + string.digits + string.punctuation
    pas = ''.join(secrets.choice(chars) for _ in range(x))
    return pas


def password() -> None:
    while True:
        lang = setting.get('app_lang')
        template = js.load(open(f'json_files/template_{(lang.lower())}.json'))

        print(f'''1. {template['gen_pass']}
2. {template['return']}''')
        choice = input('> ')

        match choice:
            case '1':
                print(f'{template['pass_len']}')

                try:
                    x = int(input('> '))

                except ValueError:
                    print(template['not_num'])
                    sleep(5)
                    clear()
                    continue

                if x >= 8:
                    pas = gen_pass(x)
                    print(f'{template['pass']}: {pas}')
                    pcp.copy(pas)
                    print(f'{template['copy']}')
                    sleep(5)
                    return
                else:
                    print(template['wrong_pass_len'])
                    sleep(5)
                    clear()
            case '2':
                return
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue
