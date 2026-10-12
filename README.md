# Password Manager – Terminal

A password manager that lives entirely in your terminal. I built it with remote machines in mind – things like a Raspberry Pi that you usually reach over SSH – so there's no GUI, no browser, and nothing to set up beyond Python.

With it you can create and manage password databases, generate passwords, and generate SSH keys, all from one simple menu.

## Features

- **Databases** – create password databases and manage them
- **Password generator** – generate strong random passwords
- **SSH key generator** – create SSH keys without leaving the app
- **Multiple languages** – the interface is translatable, and adding your own language takes a couple of minutes (see [Adding your own language](#adding-your-own-language))
- **Settings** – change things like the app language

## Requirements

- Python 3.10 or newer (the code uses `match` statements)
- The packages listed in `requirements.txt`:
  - `cryptography`
  - `argon2-cffi`
  - `pyperclip`

> **Heads-up for headless setups:** on Linux, `pyperclip` may need a clipboard tool such as `xclip` or `xsel`. On a server with no graphical environment, clipboard support might not be available.

## Installation

```bash
git clone https://github.com/n1n4zu/Password-Manager---Terminal.git
cd Password-Manager---Terminal
pip install -r requirements.txt
```

If you'd rather keep things tidy, use a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Usage

Start the app with:

```bash
python main.py
```

You'll land in the main menu, where you can open your databases, generate an SSH key, generate a password, change the settings, or exit. Just type the number of the option you want.

## Project structure

```
Password-Manager---Terminal/
├── main.py              # Entry point and main menu loop
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

One thing to watch out for: the language name you add to `settings.json` has to match your file name. The app loads `template_<language>.json` using the lowercase version of the language name, so `Deutsch` in the settings will look for `template_deutsch.json`.

If you've made a translation you think others could use, feel free to open a pull request.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.