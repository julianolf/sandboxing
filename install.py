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


def data_dir():
    home = os.path.expanduser("~")

    if sys.platform == "darwin":
        return os.path.join(home, "Library", "Application Support")
    else:
        default = os.path.join(home, ".local", "share")
        return os.getenv("XDG_DATA_HOME", default)
