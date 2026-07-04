from collections.abc import Iterator
from pathlib import Path

_SUPPORTED_EXTENSIONS = {
    ".avi",
    ".flv",
    ".m4v",
    ".mkv",
    ".mov",
    ".mp4",
    ".ts",
    ".webm",
    ".wmv",
}


def is_media_file(path: Path) -> bool:
    """Return True if the path is a supported media file."""
    return path.is_file() and path.suffix.lower() in _SUPPORTED_EXTENSIONS


def scan(path: Path) -> Iterator[Path]:
    """Yield all supported media files under the given directory."""

    if not path.exists():
        raise FileNotFoundError(f"Directory does not exist: {path}")

    if not path.is_dir():
        raise NotADirectoryError(f"Expected a directory, got: {path}")

    for item in path.rglob("*"):
        if is_media_file(item):
            yield item
