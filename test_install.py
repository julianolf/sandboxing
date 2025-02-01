import argparse
import os
import pathlib
import sys
import tempfile
import unittest
from unittest.mock import patch

import install

DARWIN = sys.platform == "darwin"
LINUX = sys.platform == "linux"


class InstallTestCase(unittest.TestCase):
    @unittest.skipIf(not DARWIN, "requires darwin")
    def test_data_dir_on_darwin(self):
        expected = os.path.join(install.HOME, "Library", "Application Support")
        self.assertEqual(install.data_dir(), expected)

    @unittest.skipIf(not LINUX, "requires linux")
    def test_data_dir_on_linux_with_xdg_data_home(self):
        expected = os.path.join(install.HOME, ".shared-data")
        with patch.dict("os.environ", {"XDG_DATA_HOME": expected}):
            self.assertEqual(install.data_dir(), expected)

    @unittest.skipIf(not LINUX, "requires linux")
    def test_data_dir_on_linux_without_xdg_data_home(self):
        expected = os.path.join(install.HOME, ".local", "share")
        environ = dict(os.environ)
        environ.pop("XDG_DATA_HOME", None)
        with patch.dict("os.environ", environ, clear=True):
            self.assertEqual(install.data_dir(), expected)

    def test_bin_dir(self):
        expected = os.path.join(install.HOME, ".local", "bin")
        self.assertEqual(install.bin_dir(), expected)

    def test_run(self):
        expected = "test\n"
        command = ("python", "-c", "print('test')")
        self.assertEqual(install.run(*command), expected)

    def test_run_exit_program_on_errors(self):
        command = ("python", "-c", "print 'test'")
        with self.assertRaises(SystemExit):
            install.run(*command)

    def test_pkg_src(self):
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

    def test_pkg_scripts(self):
        with tempfile.TemporaryDirectory() as path:
            venv_bin = pathlib.Path(path) / "bin"
            venv_bin.mkdir()

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
