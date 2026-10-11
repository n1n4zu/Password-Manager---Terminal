from cryptography.hazmat.primitives.asymmetric import ed25519, rsa
from cryptography.hazmat.primitives import serialization
import json as js
from time import sleep
from python_files.func import *
from sys import platform
from getpass import getuser

setting = js.load(open('json_files/settings.json'))
user = getuser()
win_path = f'C:\\Users\\{user}\\.ssh\\'
linux_path = f'/home/{user}/.ssh/'


def private_bytes(password: str, private_key: ed25519.Ed25519PrivateKey | rsa.RSAPrivateKey) -> bytes:
    pb = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.OpenSSH,
        encryption_algorithm=serialization.BestAvailableEncryption(
            password.encode('utf-8')
        )
    )

    return pb


def public_bytes(public_key: ed25519.Ed25519PublicKey | rsa.RSAPublicKey) -> bytes:
    pb = public_key.public_bytes(
        encoding=serialization.Encoding.OpenSSH,
        format=serialization.PublicFormat.OpenSSH
    )

    return pb


def gen_ed25519_key(password: str, key_name: str = 'id_ed25519') -> None:
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    if platform == 'win32':
        with open(win_path + key_name, 'wb') as f:
            f.write(private_bytes(password, private_key))

        with open(win_path + f'{key_name}.pub', 'wb') as f:
            f.write(public_bytes(public_key) + b'\n')
    else:
        with open(linux_path + key_name, 'wb') as f:
            f.write(private_bytes(password, private_key))

        with open(linux_path + f'{key_name}.pub', 'wb') as f:
            f.write(public_bytes(public_key) + b'\n')


def gen_rsa_key(password: str, key_name: str = 'id_rsa', key_size: int = 3072) -> None:
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
    )
    public_key = private_key.public_key()

    if platform == 'win32':
        with open(win_path + key_name, 'wb') as f:
            f.write(private_bytes(password, private_key))

        with open(win_path + f'{key_name}.pub', 'wb') as f:
            f.write(public_bytes(public_key) + b'\n')
    else:
        with open(linux_path + key_name, 'wb') as f:
            f.write(private_bytes(password, private_key))

        with open(linux_path + f'{key_name}.pub', 'wb') as f:
            f.write(public_bytes(public_key) + b'\n')


def ssh_keys() -> None:
    while True:
        lang = setting.get('app_lang')
        template = js.load(open(f'json_files/template_{(lang.lower())}.json'))

        print(f'''1. {template['ed25519']}
2. {template['rsa']}
3. {template['return']}''')
        choice = input('> ')

        match choice:
            case '1':
                key_name = input(f'{template['key_name']}[id_ed25519]\n> ')
                key_pass = ''

                while key_pass == '':
                    key_pass = input(f'{template['key_pass']}\n> ')
                    if key_pass == '':
                        print(f'{template['empty_pass']}')
                        continue

                if key_name == '':
                    gen_ed25519_key(key_pass)
                else:
                    gen_ed25519_key(key_pass, key_name)

                if platform == 'win32':
                    print(f'{template['generated']}: {win_path[:-1]}')
                else:
                    print(f'{template['generated']}: {linux_path[:-1]}')

                sleep(5)
                clear()
            case '2':
                key_name = input(f'{template['key_name']}[id_rsa]\n> ')
                key_pass = ''
                key_size = 0

                while key_pass == '':
                    key_pass = input(f'{template['key_pass']}\n> ')
                    if key_pass == '':
                        print(f'{template['empty_pass']}')
                        continue

                while key_size < 3072:
                    key_size = input(f'{template['key_size']}[3072]\n> ')
                    if key_size == '':
                        key_size = 3072
                    else:
                        try:
                            key_size = int(key_size)

                        except ValueError:
                            print(template['not_num'])
                            sleep(5)
                            clear()
                            continue

                    if key_size < 3072:
                        print(f'{template['weak_key']}')

                if key_name == '':
                    gen_rsa_key(key_pass, key_size=key_size)
                else:
                    gen_rsa_key(key_pass, key_name, key_size)

                if platform == 'win32':
                    print(f'{template['generated']}: {win_path[:-1]}')
                else:
                    print(f'{template['generated']}: {linux_path[:-1]}')

                sleep(5)
                clear()
            case '3':
                return
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue
