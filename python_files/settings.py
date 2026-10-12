import json as js
from json import JSONDecoder
from time import sleep
from python_files.func import *


setting = js.load(open('json_files/settings.json'))


def change(template: JSONDecoder) -> None:
    while True:
        print(f'{template['lang_choices']}:')

        i = 1
        for j in setting['languages']:
            print(f'{i}. {j}')
            i += 1

        try:
            choice = int(input('> '))

        except ValueError:
            print(template['not_num'])
            sleep(5)
            clear()
            continue

        if 1 <= choice < i:
            setting['app_lang'] = setting['languages'][choice - 1]
            return
        else:
            print(template['range'])
            sleep(5)
            clear()


def settings() -> None:
    while True:
        lang = setting.get('app_lang')
        template = js.load(open(f'json_files/template_{(lang.lower())}.json'))

        print(f'''{template['curr_lang']}: {setting['app_lang']}
1. {template['change_lang']}
2. {template['return']}''')
        choice = input('> ')

        match choice:
            case '1':
                clear()
                change(template)
                clear()
            case '2':
                js.dump(setting, fp=open('json_files/settings.json', 'w'))
                return
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue
