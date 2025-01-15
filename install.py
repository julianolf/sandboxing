import sys

MIN_VERSION = (3, 7)

if sys.version_info[:2] < MIN_VERSION:
    current = ".".join(map(str, sys.version_info[:2]))
    required = ".".join(map(str, MIN_VERSION)) + "+"
    error = f"Unsupported Python version {current}, requires {required}"
    sys.exit(error)

SUPPORTED_PLATFORMS = ("cygwin", "darwin", "linux")

if sys.platform not in SUPPORTED_PLATFORMS:
    platforms = ", ".join(SUPPORTED_PLATFORMS)
    error = f"Unsupported platform {sys.platform}, must be one of: {platforms}"
    sys.exit(error)

import importlib.util

if not importlib.util.find_spec("ensurepip"):
    error = "Missing required package 'ensurepip'"
    sys.exit(error)

import argparse
import os
import venv

HOME = os.path.expanduser("~")


def data_dir():
    if sys.platform == "darwin":
        return os.path.join(HOME, "Library", "Application Support")
    else:
        default = os.path.join(HOME, ".local", "share")
        return os.getenv("XDG_DATA_HOME", default)


def bin_dir():
    return os.path.join(HOME, ".local", "bin")


def install(args):
    venv_dir = os.path.join(data_dir(), args.package, "venv")
    venv.create(venv_dir, clear=True, with_pip=True)


def main():
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Install Python programs in a safe and isolated environment.",
    )
    parser.add_argument("package", help="the name of the package containing the program")
    parser.add_argument("-v", "--version", help="the version of the package to install")
    parser.add_argument("-u", "--url", help="the url from which to install the package")
    parser.add_argument("-p", "--path", help="the path from which to install the package")
    args = parser.parse_args()

    install(args)


if __name__ == "__main__":
    main()
