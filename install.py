import sys

MIN_VERSION = (3, 7)

if sys.version_info[:2] < MIN_VERSION:
    current = ".".join(map(str, sys.version_info[:2]))
    required = ".".join(map(str, MIN_VERSION)) + "+"
    error = f"Unsupported Python version {current}, requires {required}"
    sys.exit(error)

SUPPORTED_PLATFORMS = ("darwin", "linux")

if sys.platform not in SUPPORTED_PLATFORMS:
    platforms = ", ".join(SUPPORTED_PLATFORMS)
    error = f"Unsupported platform {sys.platform}, must be one of: {platforms}"
    sys.exit(error)

import importlib.util

if not importlib.util.find_spec("ensurepip"):
    error = "Missing required package 'ensurepip'"
    sys.exit(error)

import argparse
import fnmatch
import os
import shutil
import subprocess
import venv

PREFIX = "/usr/local"
HOME = os.path.expanduser("~")


def prefix_dir(args):
    if args.user:
        return os.path.join(HOME, ".local")

    if args.prefix != PREFIX:
        return os.path.abspath(os.path.expanduser(args.prefix))

    return PREFIX


def run(*cmd):
    res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    if res.returncode != 0:
        error = res.stdout.decode()
        sys.exit(error)

    return res.stdout.decode()


def pkg_src(args):
    src = args.path or args.url or args.package

    if args.version and not args.path and not args.url:
        src += f"=={args.version}"

    return src


def pkg_scripts(venv_bin):
    scripts = set()
    ignore = ("activate*", "deactivate*", "easy_install*", "pip*", "python*")

    def shouldnt_ignore(filename):
        return not any(fnmatch.fnmatch(filename.lower(), pattern) for pattern in ignore)

    with os.scandir(venv_bin) as it:
        for entry in it:
            if entry.is_file() and shouldnt_ignore(entry.name):
                scripts.add(entry.name)

    return scripts


def link(venv_bin, user_bin):
    for script in pkg_scripts(venv_bin):
        src = os.path.join(venv_bin, script)
        dst = os.path.join(user_bin, script)

        if os.path.islink(dst) and os.path.realpath(dst) == src:
            continue

        try:
            os.symlink(src, dst)
        except FileExistsError:
            error = f"{dst} already exists, cannot create symlink"
            sys.exit(error)


def unlink(venv_bin, user_bin):
    for script in pkg_scripts(venv_bin):
        src = os.path.join(venv_bin, script)
        dst = os.path.join(user_bin, script)

        if os.path.islink(dst) and os.path.realpath(dst) == src:
            os.unlink(dst)


def install(args):
    base_dir = prefix_dir(args)
    venv_dir = os.path.join(base_dir, args.package)
    venv_bin = os.path.join(venv_dir, "bin")
    venv.create(venv_dir, clear=True, with_pip=True)

    python = os.path.join(venv_bin, "python")
    source = pkg_src(args)
    run(python, "-m", "pip", "install", "--disable-pip-version-check", "--upgrade", "pip")
    run(python, "-m", "pip", "install", source)

    user_bin = os.path.join(base_dir, "bin")

    if not os.path.exists(user_bin):
        os.makedirs(user_bin, mode=0o755)

    link(venv_bin, user_bin)

    print(
        f"{args.package} installed at: {venv_dir}\n"
        f"Symbolic links were created at: {user_bin}\n"
        f'Add `export PATH="{user_bin}:$PATH"` to your shell configuration file.'
    )


def uninstall(args):
    base_dir = prefix_dir(args)
    venv_dir = os.path.join(base_dir, args.package)
    venv_bin = os.path.join(venv_dir, "bin")
    user_bin = os.path.join(base_dir, "bin")

    if os.path.isdir(venv_bin) and os.path.isdir(user_bin):
        unlink(venv_bin, user_bin)
        shutil.rmtree(venv_dir)

        print(f"Removed symbolic links from: {user_bin}\nDeleted directory: {venv_dir}")


def main():
    parser = argparse.ArgumentParser(
        prog="install.py",
        description="Install Python programs in a safe and isolated environment.",
    )
    parser.add_argument("package", help="the name of the package containing the program")
    parser.add_argument("-v", "--version", help="the version of the package to install")
    parser.add_argument("-u", "--url", help="the url from which to install the package")
    parser.add_argument("-p", "--path", help="the path from which to install the package")
    parser.add_argument(
        "--user",
        action="store_true",
        default=False,
        help="install the package in the user's local directory (typically: ~/.local)",
    )
    parser.add_argument(
        "--prefix",
        default=PREFIX,
        help="the directory to install the package (default: %(default)s)",
    )
    parser.add_argument("--uninstall", action="store_true", default=False, help="uninstall package")
    args = parser.parse_args()

    try:
        if args.uninstall:
            uninstall(args)
        else:
            install(args)
    except PermissionError as error:
        sys.exit(error.strerror)


if __name__ == "__main__":
    main()
