import sys

MIN_VERSION = (3, 7)

if sys.version_info[:2] < MIN_VERSION:
    current = ".".join(map(str, sys.version_info[:2]))
    required = ".".join(map(str, MIN_VERSION)) + "+"
    error = f"Unsupported Python version {current}, requires {required}"
    print(error, file=sys.stderr)
    exit(1)

SUPPORTED_PLATFORMS = ("cygwin", "darwin", "linux")

if sys.platform not in SUPPORTED_PLATFORMS:
    platforms = ", ".join(SUPPORTED_PLATFORMS)
    error = f"Unsupported platform {sys.platform}, must be one of: {platforms}"
    print(error, file=sys.stderr)
    exit(1)

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
