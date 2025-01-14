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

HOME = os.path.expanduser("~")


def data_dir():
    if sys.platform == "darwin":
        return os.path.join(HOME, "Library", "Application Support")
    else:
        default = os.path.join(HOME, ".local", "share")
        return os.getenv("XDG_DATA_HOME", default)


def bin_dir():
    return os.path.join(HOME, ".local", "bin")


def main():
    parser = argparse.ArgumentParser(
        description="Install Python program in an isolated environment"
    )
    parser.add_argument("program", help="package name, path or url")
    parser.parse_args()
