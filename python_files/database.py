import json as js
from json import JSONDecoder
from time import sleep
import cryptography
from python_files.func import *
import os
from sys import platform
from getpass import getuser, getpass
from argon2.low_level import hash_secret_raw, Type
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from python_files.gen_pass import gen_pass
from pathlib import Path


setting = js.load(open('json_files/settings.json'))
user = getuser()
win_path = f'C:\\Users\\{user}\\.ssh\\'
linux_path = f'/home/{user}/.ssh/'
db_path = 'databases/'


def derive_key(password: str, salt: bytes, keyfile_data: bytes = b'') -> bytes:
    """
    Change password and optional keyfile data into 32-byte key
    :param password: Password given by user or generated automatically
    :param salt: Random bytes
    :param keyfile_data: Data from keyfile
    :return: Encrypted key
    """
    combined_secret = password.encode() + keyfile_data
    key = hash_secret_raw(
        secret=combined_secret,
        salt=salt,
        time_cost=3,
        memory_cost=65536,
        parallelism=4,
        hash_len=32,
        type=Type.ID
    )
    return key


def load_keyfile(path: str) -> bytes:
    """
    Load bytes from keyfile in given path
    :param path: Path to the keyfile
    :return: Bytes in the keyfile
    """
    with open(path, 'rb') as f:
        return f.read()


def encrypt_database(data: dict, password: str, keyfile_data: bytes = b'') -> bytes:
    """
    Change Python dictionary into encrypted data
    :param data: Python dictionary
    :param password: Password given by user or generated automatically
    :param keyfile_data: Data from keyfile
    :return: Encrypted data
    """
    salt = os.urandom(16)
    nonce = os.urandom(12)
    key = derive_key(password, salt, keyfile_data)

    aesgcm = AESGCM(key)
    plaintext = js.dumps(data).encode()
    ciphertext = aesgcm.encrypt(nonce, plaintext, associated_data=None)

    return salt + nonce + ciphertext


def decrypt_database(blob: bytes, password: str, keyfile_data: bytes = b'') -> dict:
    """
    Change encrypted data into Python dictionary
    :param blob: Encrypted data
    :param password: Password needed to unlock data
    :param keyfile_data: Data from keyfile
    :return: Python dictionary
    """
    salt, nonce, ciphertext = blob[:16], blob[16:28], blob[28:]
    key = derive_key(password, salt, keyfile_data)

    aesgcm = AESGCM(key)
    try:
        plaintext = aesgcm.decrypt(nonce, ciphertext, associated_data=None)
    except cryptography.exceptions.InvalidTag:
        raise NoKeyError()
    return js.loads(plaintext)


def save_database(data: dict, path: str, password: str, keyfile_path: str | None = None) -> None:
    """
    Save encrypted data to database
    :param data: Encrypted data
    :param path: Path to directory with databases
    :param password: Password given by user or generated automatically
    :param keyfile_path: Path to the keyfile
    """
    keyfile_data = load_keyfile(keyfile_path) if keyfile_path else b''
    blob = encrypt_database(data, password, keyfile_data)
    with open(path, 'wb') as f:
        f.write(blob)


def open_database(path: str, password: str, keyfile_path: str | None = None) -> dict:
    """
    Open encrypted database
    :param path: Path to the database
    :param password: Password needed to unlock the database
    :param keyfile_path: Path to the keyfile
    :return: Python dictionary
    """
    keyfile_data = load_keyfile(keyfile_path) if keyfile_path else b''
    with open(path, 'rb') as f:
        blob = f.read()
    return decrypt_database(blob, password, keyfile_data)


def find_db(db_name: str) -> bool:
    """
    Look for database in the directory
    :param db_name: Database name
    :return: Bool value
    """
    for dirpath, dirnames, filenames in os.walk(db_path):
        if db_name in filenames:
            return True
    return False


def find_key(keyfile: str) -> bool:
    """
    Look for the keyfile in the directory
    :param keyfile: Keyfile name or path to the keyfile
    :return: Bool value
    """
    if '/' not in keyfile and '\\' not in keyfile:
        if platform == 'win32':
            path = win_path
        else:
            path = linux_path

        key = keyfile
    else:
        file = Path(keyfile)

        key = file.name
        path = file.parent

    for dirpath, dirnames, filenames in os.walk(path):
        if key in filenames:
            return True
    return False


def manage_db(db: dict, template: JSONDecoder, db_name: str, db_password: str, keyfile_path: str | None = None) -> None:
    """
    Manage database content
    :param db: Python dictionary
    :param template: Json file with values written in terminal
    :param db_name: Name of database needed to save changes
    :param db_password: Password to the database to save changes
    :param keyfile_path: Path to the keyfile to save changes
    """
    while True:
        clear()
        print(f'''1. {template['list_content']}
2. {template['add_pass']}
3. {template['del_pass']}
4. {template['rec_info']}
5. {template['edit_pass']}
6. {template['return']}''')
        choice = input('> ')

        match choice:
            case '1':
                clear()
                for i in db:
                    print(i)
                input(f'{template['continue']}')
            case '2':
                record_name = ''
                password = ''

                while record_name == '':
                    record_name = input(f'{template['record_name']}\n> ')
                    if record_name == '':
                        print(template['empty_rec_name'])
                        continue
                    if record_name in db:
                        print(template['double_rec'])
                        continue

                db[record_name] = {
                    'username': '',
                    'password': '',
                    'URL/Service': ''
                }

                username = input(f'{template['rec_user']}\n> ')
                url_service = input(f'{template['rec_url_ser']}\n> ')

                db[record_name]['username'] = username
                db[record_name]['URL/Service'] = url_service

                print(f'''1. {template['gen_pass']}
2. {template['rec_pass']}''')

                c = input('> ')

                match c:
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
                            password = gen_pass(x)
                            print(f'{template['pass']}: {password}')

                            db[record_name]['password'] = password

                        else:
                            print(template['wrong_pass_len'])
                    case '2':
                        while password == '':
                            password = getpass(f'{template['rec_pass']}\n> ')

                            db[record_name]['password'] = password

                            if password == '':
                                print(template['empty_pass'])
                                continue

                del password, url_service, username, record_name

                save_database(db, db_path + db_name, db_password, keyfile_path)
            case '3':
                record_name = ''

                while record_name == '':
                    record_name = input(f'{template['record_name']}\n> ')
                    confirm = False

                    if record_name == '':
                        print(template['empty_rec_name'])
                        continue

                    if record_name not in db:
                        print(template['no_rec'])
                        sleep(5)
                        clear()
                        continue

                    c = input(f'{template['confirm_del_rec']}\n>' )
                    if c.lower() == 'y':
                        confirm = True

                    if confirm:
                        db.pop(record_name)

                    save_database(db, db_path + db_name, db_password, keyfile_path)
            case '4':
                record_name = ''

                while record_name == '':
                    record_name = input(f'{template['record_name']}\n> ')

                    if record_name == '':
                        print(template['empty_rec_name'])
                        continue

                    if record_name not in db:
                        print(template['no_rec'])
                        sleep(5)
                        clear()
                        continue

                    clear()

                    print(f'''{template['rec_name']}: {record_name}
{template['username']}: {db[record_name]['username']}
{template['password']}: {db[record_name]['password']}
{template['URL/Service']}: {db[record_name]['URL/Service']}''')

                    input(f'{template['continue']}')
            case '5':
                record_name = ''

                while record_name == '':
                    record_name = input(f'{template['record_name']}\n> ')
                    if record_name == '':
                        print(template['empty_rec_name'])
                        continue

                if record_name not in db:
                    print(template['no_rec'])
                    sleep(5)
                    clear()
                    continue

                while True:
                    print(f'''{template['edit_q']}
1. {template['username']}
2. {template['password']}
3. {template['URL/Service']}
4. {template['rec_name']}
5. {template['return']}''')
                    choice = input('> ')

                    match choice:
                        case '1':
                            username = input(f'{template['rec_user']}\n> ')

                            db[record_name]['username'] = username
                        case '2':
                            print(f'''1. {template['gen_pass']}
2. {template['rec_pass']}''')

                            c = input('> ')

                            password = ''

                            match c:
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
                                        password = gen_pass(x)
                                        print(f'{template['pass']}: {password}')
                                    else:
                                        print(template['wrong_pass_len'])
                                case '2':
                                    while password == '':
                                        password = getpass(f'{template['rec_pass']}\n> ')
                                        if password == '':
                                            print(template['empty_pass'])
                                            continue

                            db[record_name]['password'] = password
                        case '3':
                            url_service = input(f'{template['rec_url_ser']}\n> ')

                            db[record_name]['URL/Service'] = url_service
                        case '4':
                            new_record_name = ''

                            while new_record_name == '':
                                new_record_name = input(f'{template['record_name']}\n> ')
                                if new_record_name == '':
                                    print(template['empty_rec_name'])
                                    continue
                            db[new_record_name] = db[record_name]

                            db.pop(record_name)

                            record_name = new_record_name
                        case '5':
                            return
                        case _:
                            print(template['wrong_choice'])
                            sleep(5)
                            clear()
                            continue

                    save_database(db, db_path + db_name, db_password, keyfile_path)
            case '6':
                return
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue


def database() -> None:
    """
    Main function to manage databases with passwords
    """
    while True:
        clear()
        lang = setting.get('app_lang')
        template = js.load(open(f'json_files/template_{(lang.lower())}.json'))
        last_db = setting.get('last_used_db')

        print(f'''1. {template['last_db']}
2. {template['db_list']}
3. {template['choose_db']}
4. {template['create_db']}
5. {template['del_db']}
6. {template['return']}''')
        choice = input('> ')

        match choice:
            case '1':
                if setting['last_used_db'] == '':
                    print(template['no_last_db'])
                    sleep(5)
                    clear()
                    continue

                password = ''
                keyfile_path = input(f'{template['db_key']}\n> ')

                if keyfile_path != '':
                    keyfile_exists = find_key(keyfile_path)

                    if not keyfile_exists:
                        print(template['no_key'])
                        sleep(5)
                        clear()
                        continue

                    if '/' not in keyfile_path and '\\' not in keyfile_path:
                        if platform == 'win32':
                            keyfile_path = win_path + keyfile_path
                        else:
                            keyfile_path = linux_path + keyfile_path

                while password == '':
                    password = getpass(f'{template['db_pass']}\n> ')
                    if password == '':
                        print(f'{template['empty_pass']}')
                        continue

                try:
                    db = open_database(db_path + last_db, password, keyfile_path)
                except NoKeyError:
                    print(template['no_key_encryption'])
                    sleep(5)
                    clear()
                    continue

                clear()

                manage_db(db, template, last_db, password, keyfile_path)

                del password, keyfile_path
            case '2':
                clear()
                i = 1
                for j in os.listdir(db_path):
                    if j.endswith('.pmdb'):
                        print(f'{i}. {j[:-5]}')
                        i += 1

                input(f'{template['continue']}')
            case '3':
                db_name = input(f'{template['db_name']}\n> ')

                db_exists = find_db(db_name + '.pmdb')
                
                if not db_exists:
                    print(template['no_db'])
                    sleep(5)
                    clear()
                    continue

                if db_name == '':
                    print(template['empty_db_name'])
                    sleep(5)
                    clear()
                    continue

                password = ''
                keyfile_path = input(f'{template['db_key']}\n> ')

                if keyfile_path != '':
                    keyfile_exists = find_key(keyfile_path)

                    if not keyfile_exists:
                        print(template['no_key'])
                        sleep(5)
                        clear()
                        continue

                    if '/' not in keyfile_path and '\\' not in keyfile_path:
                        if platform == 'win32':
                            keyfile_path = win_path + keyfile_path
                        else:
                            keyfile_path = linux_path + keyfile_path

                while password == '':
                    password = getpass(f'{template['db_pass']}\n> ')
                    if password == '':
                        print(f'{template['empty_pass']}')
                        continue

                try:
                    db = open_database(db_path + db_name + '.pmdb', password, keyfile_path)
                except NoKeyError:
                    print(template['no_key_encryption'])
                    sleep(5)
                    clear()
                    continue

                clear()

                manage_db(db, template, db_name + '.pmdb', password, keyfile_path)

                del password, keyfile_path

                setting['last_used_db'] = db_name + '.pmdb'

                js.dump(setting, fp=open('json_files/settings.json', 'w'))
            case '4':
                db_name = input(f'{template['db_name']}\n> ')

                db_exists = find_db(db_name + '.pmdb')

                if db_exists:
                    print(template['db_exists'])
                    sleep(5)
                    clear()
                    continue

                if db_name == '':
                    print(template['empty_db_name'])
                    sleep(5)
                    clear()
                    continue

                password = ''
                keyfile_path = input(f'{template['db_key']}\n> ')

                if keyfile_path != '':
                    keyfile_exists = find_key(keyfile_path)

                    if not keyfile_exists:
                        print(template['no_key'])
                        sleep(5)
                        clear()
                        continue

                    if '/' not in keyfile_path and '\\' not in keyfile_path:
                        if platform == 'win32':
                            keyfile_path = win_path + keyfile_path
                        else:
                            keyfile_path = linux_path + keyfile_path

                while password == '':
                    password = getpass(f'{template['db_pass']}\n> ')
                    if password == '':
                        print(f'{template['empty_pass']}')
                        continue

                save_database({}, db_path + db_name + '.pmdb', password, keyfile_path)
                del password, keyfile_path
            case '5':
                db_name = input(f'{template['db_name']}\n> ')
                confirm = False

                db_exists = find_db(db_name + '.pmdb')

                if not db_exists:
                    print(template['no_db'])
                    sleep(5)
                    clear()
                    continue

                if db_name == '':
                    print(template['empty_db_name'])
                    continue

                c = input(f'{template['confirm_del_db']}\n>')
                if c.lower() == 'y':
                    confirm = True

                if confirm:
                    os.remove(db_path + db_name + '.pmdb')

                setting['last_used_db'] = ''

                js.dump(setting, fp=open('json_files/settings.json', 'w'))
            case '6':
                return
            case _:
                print(template['wrong_choice'])
                sleep(5)
                clear()
                continue
