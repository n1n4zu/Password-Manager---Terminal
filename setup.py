from getpass import getuser
import os
from sys import platform
from urllib.request import urlretrieve as wget
import subprocess


user = getuser()
win_path = f'C:\\Users\\{user}\\Documents\\PasswordManager'
linux_path = f'/home/{user}/PasswordManager'


if __name__ == '__main__':
    if platform == 'win32':
        os.makedirs(win_path)
        os.makedirs(win_path + '\\json_files')
        os.makedirs(win_path + '\\python_files')
        os.makedirs(win_path + '\\databases')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/requirements.txt',
             f'{win_path}\\requirements.txt')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/settings.json',
             f'{win_path}\\json_files\\settings.json')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/template_polski.json',
             f'{win_path}\\json_files\\template_polski.json')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/template_english'
             '.json',
             f'{win_path}\\json_files\\template_english.json')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/main.py',
             f'{win_path}\\main.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/__init__.py',
             f'{win_path}\\python_files\\__init__.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/database.py',
             f'{win_path}\\python_files\\database.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/func.py',
             f'{win_path}\\python_files\\func.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/gen_key.py',
             f'{win_path}\\python_files\\gen_key.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/gen_pass.py',
             f'{win_path}\\python_files\\gen_pass.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/settings.py',
             f'{win_path}\\python_files\\settings.py')

        os.system(f'python -m venv {win_path}\\pmvenv')
        os.system(f'{win_path}\\pmvenv\\Scripts\\activate && pip install -r {win_path}\\requirements.txt')

        with open(f'C:\\Users\\{user}\\PasswordManager.bat', 'w') as f:
            f.write(f'cd {win_path} && {win_path}\\pmvenv\\Scripts\\activate && python main.py')

    if platform == 'linux':
        os.makedirs(linux_path)
        os.makedirs(linux_path + '/json_files')
        os.makedirs(linux_path + '/python_files')
        os.makedirs(linux_path + '/databases')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/requirements.txt',
             f'{linux_path}/requirements.txt')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/settings.json',
             f'{linux_path}/json_files/settings.json')
        wget(
            'https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/template_polski.json',
            f'{linux_path}/json_files/template_polski.json')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/json_files/template_english'
             '.json',
             f'{linux_path}/json_files/template_english.json')

        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/main.py',
             f'{linux_path}/main.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/__init__.py',
             f'{linux_path}/python_files/__init__.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/database.py',
             f'{linux_path}/python_files/database.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/func.py',
             f'{linux_path}/python_files/func.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/gen_key.py',
             f'{linux_path}/python_files/gen_key.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/gen_pass.py',
             f'{linux_path}/python_files/gen_pass.py')
        wget('https://raw.githubusercontent.com/n1n4zu/Password-Manager---Terminal/main/python_files/settings.py',
             f'{linux_path}/python_files/settings.py')

        os.system(f'python -m venv {linux_path}/pmvenv')
        subprocess.run(
            [f'{linux_path}/pmvenv/bin/python', '-m', 'pip', 'install', '-r',
             f'{linux_path}/requirements.txt'],
            check=True
        )

        with open(f'/home/{user}/PasswordManager.sh', 'w') as f:
            f.write('#!/bin/bash\n')
            f.write(f'cd {linux_path} && source {linux_path}/pmvenv/bin/activate && python main.py')

        os.system(f'chmod +x /home/{user}/PasswordManager.sh')
