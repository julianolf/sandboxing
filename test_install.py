import os

import install


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
