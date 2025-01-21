# sandboxing

![Tests](https://github.com/julianolf/sandboxing/actions/workflows/ci.yml/badge.svg?event=push)

Install Python programs in a safe and isolated environment.

This script is intended to be used as an installation tool for Python programs that do not have their own installation method with dependency isolation. It uses Python's built-in modules **venv** and **pip** to create a virtual environment and install the program along with its dependencies inside that environment.

### Requirements

Python 3.7+ with **venv**, **pip**, and **ensurepip** installed.

Most Python installations come with **venv**, **pip**, and **ensurepip** by default.

## Usage

For a better user experience, copy the `install.py` script and define your package and flags directly in the code so users can omit the extra arguments after `python3 -`.

The examples below are for illustration purposes and can be run as-is to test the script.

Installing the latest version of **cowsay** from PyPI:

```sh
curl -sSf https://raw.githubusercontent.com/julianolf/sandboxing/refs/heads/main/install.py | python3 - cowsay
```

Installing a specific version:

```sh
curl -sSf https://raw.githubusercontent.com/julianolf/sandboxing/refs/heads/main/install.py | python3 - cowsay --version=6.0
```

To update a previously installed program, simply run the installation script again.

To uninstall a program:

```sh
curl -sSf https://raw.githubusercontent.com/julianolf/sandboxing/refs/heads/main/install.py | python3 - cowsay --uninstall
```

For more options and usage, run:

```sh
curl -sSf https://raw.githubusercontent.com/julianolf/sandboxing/refs/heads/main/install.py | python3 - --help
```
