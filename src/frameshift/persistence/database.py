import sqlite3
from pathlib import Path

DEFAULT_DATABASE = Path("frameshift.db")


def connect(database: Path = DEFAULT_DATABASE) -> sqlite3.Connection:
    """Open (or create) the FrameShift database."""

    database.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(database) 