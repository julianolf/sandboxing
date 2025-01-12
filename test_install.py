import os

import pytest

import install


@pytest.fixture(scope="session")
def home():
    return os.path.expanduser("~")


def test_data_dir_on_darwin(home, monkeypatch):
    expected = os.path.join(home, "Library", "Application Support")
    monkeypatch.setattr(install.sys, "platform", "darwin")
    assert install.data_dir() == expected


def test_data_dir_on_linux_with_xdg_data_home(home, monkeypatch):
    expected = os.path.join(home, ".shared-data")
    monkeypatch.setenv("XDG_DATA_HOME", expected)
    monkeypatch.setattr(install.sys, "platform", "linux")
    assert install.data_dir() == expected


def test_data_dir_on_linux_without_xdg_data_home(home, monkeypatch):
    expected = os.path.join(home, ".local", "share")
    monkeypatch.delenv("XDG_DATA_HOME", raising=False)
    monkeypatch.setattr(install.sys, "platform", "linux")
    assert install.data_dir() == expected
