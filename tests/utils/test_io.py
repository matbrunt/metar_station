import pytest
from pathlib import Path

from metar_station.utils import io


def test_get_data_dir_envvar_exists(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("DATA_DIR", "/foo/bar")
    assert io.get_data_dir() == Path("/foo/bar")


def test_get_data_dir_envvar_exists_relative(monkeypatch: pytest.MonkeyPatch):
    base_path = Path(__file__).parent

    expected_path = base_path.parent.joinpath("foo")

    monkeypatch.chdir(base_path)
    monkeypatch.setenv("DATA_DIR", "../foo")
    assert io.get_data_dir() == expected_path


def test_get_data_dir_no_envvar(monkeypatch: pytest.MonkeyPatch, mocker):
    monkeypatch.delenv("DATA_DIR", raising=False)

    mock = mocker.patch(
        "metar_station.utils.io.get_root_dir",
        return_value=Path("/foo/bar"),
    )
    assert io.get_data_dir() == Path("/foo/bar/data")
    mock.assert_called_once()
