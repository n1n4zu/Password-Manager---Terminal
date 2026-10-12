# Password Manager – Terminal

A password manager that lives entirely in your terminal. I built it with remote machines in mind – things like a Raspberry Pi that you usually reach over SSH – so there's no GUI, no browser, and nothing to set up beyond Python.

With it you can create and manage password databases, generate passwords, and generate SSH keys, all from one simple menu.

## Features

- **Databases** – create password databases and manage them
- **Password generator** – generate strong random passwords
- **SSH key generator** – create SSH keys without leaving the app
- **One-step setup** – a setup script installs everything and creates a launcher, so you can start the app with a single command
- **Multiple languages** – the interface is translatable, and adding your own language takes a couple of minutes (see [Adding your own language](#adding-your-own-language))
- **Settings** – change things like the app language

## Requirements

- Windows or Linux (including Raspberry Pi OS)
- Python 3.10 or newer, available as `python` in your terminal (the code uses `match` statements)
- The packages listed in `requirements.txt` (the setup script installs them for you):
  - `cryptography`
  - `argon2-cffi`
  - `pyperclip`

> **Heads-up for Debian-based systems:** if creating the virtual environment fails, you may need to install the venv module first, e.g. `sudo apt install python3-venv`.

> **Heads-up for headless setups:** on Linux, `pyperclip` may need a clipboard tool such as `xclip` or `xsel`. On a server with no graphical environment, clipboard support might not be available.

## Installation

### Quick install (recommended)

The easiest way is the `setup.py` script. It does all the boring work for you:

1. Creates the `PasswordManager` folder with `json_files`, `python_files` and `databases` subfolders
2. Downloads the latest program files from this repository
3. Creates a virtual environment (`pmvenv`) and installs the dependencies into it
4. Creates a launcher file in your home directory, so you can start the app without activating the environment yourself

Download `setup.py` and run it:

```bash
python setup.py
```

Here's where everything ends up:

| | Windows | Linux |
|---|---|---|
| App folder | `C:\Users\<user>\Documents\PasswordManager` | `/home/<user>/PasswordManager` |
| Launcher | `C:\Users\<user>\PasswordManager.bat` | `/home/<user>/PasswordManager.sh` |

After the setup finishes, just run the launcher.

On Windows, double-click `PasswordManager.bat` or run it from a terminal:

```bat
C:\Users\<user>\PasswordManager.bat
```

On Linux:

```bash
~/PasswordManager.sh
```

A couple of things to keep in mind:

- The script needs an internet connection, since it downloads the files from GitHub.
- It won't overwrite an existing installation. If the `PasswordManager` folder already exists, the script stops with an error – move or delete the old folder first (back up your `databases` folder if it contains anything you want to keep!).
- Only the Polish and English language files are downloaded. See [Adding your own language](#adding-your-own-language) if you want to add another one.

### Manual install

If you'd rather set things up yourself:

```bash
git clone https://github.com/n1n4zu/Password-Manager---Terminal.git
cd Password-Manager---Terminal
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Usage

Start the app with the launcher created by `setup.py` (or with `python main.py` if you installed it manually).

You'll land in the main menu, where you can open your databases, generate an SSH key, generate a password, change the settings, or exit. Just type the number of the option you want.

## Project structure

```
Password-Manager---Terminal/
├── main.py              # Entry point and main menu loop
├── setup.py             # Automated installer (folders, files, venv, launcher)
├── requirements.txt     # Python dependencies
├── LICENSE              # GPL-3.0
├── json_files/          # Settings and language files (template_*.json)
└── python_files/        # The app's modules (databases, generators, settings)
```

## Adding your own language

You don't need to touch any Python code to translate the app. Here's how:

1. Go to the `json_files/` folder, copy one of the existing `template_*.json` files, and name the copy `template_<your_language>.json` (for example, `template_deutsch.json`).
2. Open your new file and translate the values. Leave the keys as they are – only change the text on the right-hand side.
3. Open `json_files/settings.json` and add your language to the list of languages. This is what makes it show up as an option in the app's settings.
4. Start the app, open **Settings**, and pick your language.

If you installed the app with `setup.py`, the `json_files` folder you're looking for is inside the app folder (see the table above).

One thing to watch out for: the language name you add to `settings.json` has to match your file name. The app loads `template_<language>.json` using the lowercase version of the language name, so `Deutsch` in the settings will look for `template_deutsch.json`.

If you've made a translation you think others could use, feel free to open a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.