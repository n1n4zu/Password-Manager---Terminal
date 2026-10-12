import json as js
import cryptography as cg
import keyring as kr
import pyperclip as pcp
import argon2
import os
from time import sleep
from python_files.func import *
from python_files.settings import settings
from python_files.gen_pass import password
from python_files.gen_key import ssh_keys
from python_files.database import database


setting = js.load(open('json_files/settings.json'))

if __name__ == '__main__':
    """
    Main loop of the program
    """
    clear()
    while True:
        lang = setting.get('app_lang')
        template = js.load(open(f'json_files/template_{(lang.lower())}.json'))

        print(f'''Menu:
1. {template['db_list']}
2. {template['generate_key']}
3. {template['generate_pass']}
4. {template['settings']}
5. {template['exit']}''')

        choice = input('> ')
        match choice:
            case '1':
                clear()
                database()
                clear()
            case '2':
                clear()
                ssh_keys()
                clear()
            case '3':
                clear()
                password()
                clear()
            case '4':
                clear()
                settings()
                setting = js.load(open('json_files/settings.json'))
                clear()
            case '5':
                js.dump(setting, fp=open('json_files/settings.json', 'w'))
                exit()
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue
