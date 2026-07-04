from pathlib import Path

import pytest

from frameshift.discovery.scanner import scan


def test_scan_empty_directory(tmp_path: Path) -> None:
    files = list(scan(tmp_path))

    assert files == []


def test_scan_finds_media_files(tmp_path: Path) -> None:
    (tmp_path / "movie.mkv").touch()
    (tmp_path / "episode.mp4").touch()

    files = list(scan(tmp_path))

    assert len(files) == 2
    assert tmp_path / "movie.mkv" in files
    assert tmp_path / "episode.mp4" in files


def test_scan_ignores_non_media_files(tmp_path: Path) -> None:
    (tmp_path / "poster.jpg").touch()
    (tmp_path / "notes.txt").touch()
    (tmp_path / "tvshow.nfo").touch()
    (tmp_path / "episode.mkv").touch()

    files = list(scan(tmp_path))

    assert files == [tmp_path / "episode.mkv"]


def test_scan_searches_subdirectories(tmp_path: Path) -> None:
    season = tmp_path / "Season 1"
    season.mkdir()

    episode = season / "S01E01.mkv"
    episode.touch()

    files = list(scan(tmp_path))

    assert files == [episode]


def test_scan_raises_for_missing_directory() -> None:
    with pytest.raises(FileNotFoundError):
        list(scan(Path("this-directory-does-not-exist")))


def test_scan_raises_for_file(tmp_path: Path) -> None:
    file = tmp_path / "movie.mkv"
    file.touch()

    with pytest.raises(NotADirectoryError):
        list(scan(file))
