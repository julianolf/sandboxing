import argparse
import os

import pytest

import install

Args = argparse.Namespace


def test_data_dir_on_darwin(monkeypatch):
    expected = os.path.join(install.HOME, "Library", "Application Support")
    monkeypatch.setattr(install.sys, "platform", "darwin")
    assert install.data_dir() == expected


def test_data_dir_on_linux_with_xdg_data_home(monkeypatch):
    expected = os.path.join(install.HOME, ".shared-data")
    monkeypatch.setenv("XDG_DATA_HOME", expected)
    monkeypatch.setattr(install.sys, "platform", "linux")
    assert install.data_dir() == expected


def test_data_dir_on_linux_without_xdg_data_home(monkeypatch):
    expected = os.path.join(install.HOME, ".local", "share")
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    monkeypatch.setattr(install.sys, "platform", "linux")
    assert install.data_dir() == expected


def test_bin_dir():
    expected = os.path.join(install.HOME, ".local", "bin")
    assert install.bin_dir() == expected


def test_run():
    expected = "test\n"
    command = ("python", "-c", "print('test')")
    assert install.run(*command) == expected


def test_run_exit_program_on_errors():
    command = ("python", "-c", "print 'test'")
    with pytest.raises(SystemExit):
        install.run(*command)


@pytest.mark.parametrize(
    "args,src",
    [
        (Args(package="test", version="0.1.0", url=None, path=None), "test==0.1.0"),
        (Args(package="test", version=None, url=None, path=None), "test"),
        (Args(package="test", version=None, url="http://host/repo", path=None), "http://host/repo"),
        (Args(package="test", version=None, url="/home/user/pkg", path=None), "/home/user/pkg"),
    ],
)
def test_pkg_src(args, src):
    assert install.pkg_src(args) == src


def test_pkg_scripts(tmp_path):
    venv_bin = tmp_path / "bin"
    venv_bin.mkdir()

    files = (
        "activate",
        "activate.csh",
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
    assert install.pkg_scripts(venv_bin) == expected
