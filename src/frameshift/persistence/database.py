import sqlite3
from pathlib import Path

DEFAULT_DATABASE = Path("frameshift.db")


def connect(database: Path = DEFAULT_DATABASE) -> sqlite3.Connection:
    """Open (or create) the FrameShift database."""

    database.parent.mkdir(parents=True, exist_ok=True)

    return sqlite3.connect(database) 

def initialize(connection: sqlite3.Connection) -> None:
    """Create the database schema if it does not already exist."""

    connection.execute("""
        CREATE TABLE IF NOT EXISTS media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            size INTEGER NOT NULL,
            extension TEXT NOT NULL,
            media_type TEXT NOT NULL,
            title TEXT,
            year INTEGER,
            season INTEGER,
            episode INTEGER
        )
    """)

    connection.commit()