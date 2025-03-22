import argparse
import contextlib
import os
import pathlib
import tempfile
import unittest

import install


class TestPrefixDir(unittest.TestCase):
    def test_with_default_value(self):
        args = argparse.Namespace(user=False, prefix=install.PREFIX)
        self.assertEqual(install.prefix_dir(args), install.PREFIX)

    def test_with_user_flag_on(self):
        expected = os.path.join(install.HOME, ".local")
        args = argparse.Namespace(user=True, prefix=install.PREFIX)
        self.assertEqual(install.prefix_dir(args), expected)

    def test_with_custom_path(self):
        expected = os.path.join(install.HOME, "apps")
        args = argparse.Namespace(user=False, prefix=expected)
        self.assertEqual(install.prefix_dir(args), expected)


class TestRun(unittest.TestCase):
    def test_run_command(self):
        expected = "test\n"
        command = ("python", "-c", "print('test')")
        self.assertEqual(install.run(*command), expected)

    def test_exit_program_on_errors(self):
        command = ("python", "-c", "print 'test'")
        with self.assertRaises(SystemExit):
            install.run(*command)


class TestPkgSrc(unittest.TestCase):
    def test_input_combinations(self):
        params = (
            (
                argparse.Namespace(package="test", version="0.1.0", url=None, path=None),
                "test==0.1.0",
            ),
            (
                argparse.Namespace(package="test", version=None, url=None, path=None),
                "test",
            ),
            (
                argparse.Namespace(package="test", version=None, url="http://host/repo", path=None),
                "http://host/repo",
            ),
            (
                argparse.Namespace(package="test", version=None, url="/home/user/pkg", path=None),
                "/home/user/pkg",
            ),
        )
        for args, src in params:
            with self.subTest(args=args, src=src):
                self.assertEqual(install.pkg_src(args), src)


@contextlib.contextmanager
def temp_dirs():
    with tempfile.TemporaryDirectory() as path:
        user_bin = pathlib.Path(path).resolve() / "bin"
        user_bin.mkdir()

        venv_dir = pathlib.Path(path).resolve() / "venv"
        venv_bin = venv_dir / "bin"
        venv_bin.mkdir(parents=True)

        yield user_bin, venv_bin


class TestPkgScripts(unittest.TestCase):
    def test_scripts_lookup(self):
        with temp_dirs() as (_, venv_bin):
            files = (
                "activate",
                "activate.csh",
                "Activate.ps1",
                "deactivate",
                "easy_install",
                "easy_install-3.7",
                "pip",
                "pip3",
                "py.test",
                "pytest",
                "python",
                "python3",
            )

            for file in files:
                f = venv_bin / file
                f.touch()

            expected = {"py.test", "pytest"}
            self.assertEqual(install.pkg_scripts(venv_bin), expected)


class TestLink(unittest.TestCase):
    def test_creates_link(self):
        with temp_dirs() as (user_bin, venv_bin):
            shouldnt_exist = venv_bin / "shouldnt_exist"
            shouldnt_exist_link = user_bin / shouldnt_exist.name

            should_exist = venv_bin / "should_exist"
            should_exist.touch()
            should_exist_link = user_bin / should_exist.name
            should_exist_link.symlink_to(should_exist)

            should_create = venv_bin / "should_create"
            should_create.touch()
            should_create_link = user_bin / should_create.name

            bins = (shouldnt_exist.name, should_exist.name, should_create.name)
            install.link(venv_bin, user_bin, bins)

            self.assertFalse(shouldnt_exist_link.is_symlink())
            self.assertTrue(should_exist_link.is_symlink())
            self.assertTrue(should_create_link.is_symlink())


class TestUnlink(unittest.TestCase):
    def test_removes_link(self):
        with temp_dirs() as (user_bin, venv_bin):
            script = venv_bin / "script"
            script.touch()

            script_link = user_bin / script.name
            script_link.symlink_to(script)

            bins = (script.name,)
            install.unlink(venv_bin, user_bin, bins)

            self.assertFalse(script_link.is_symlink())
