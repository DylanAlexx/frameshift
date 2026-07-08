import sqlite3

from frameshift.config import APP_DIR, DATABASE_PATH


def connect() -> sqlite3.Connection:
    """Open (or create) the FrameShift database."""

    APP_DIR.mkdir(parents=True, exist_ok=True)

    connection = sqlite3.connect(DATABASE_PATH)
    connection.row_factory = sqlite3.Row

    return connection


def initialize(connection: sqlite3.Connection) -> None:
    """Create the database schema if it does not already exist."""

    connection.execute(
        """
        CREATE TABLE IF NOT EXISTS media_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            path TEXT NOT NULL UNIQUE,
            size INTEGER NOT NULL,
            extension TEXT NOT NULL,
            media_type TEXT NOT NULL,
            title TEXT,
            year INTEGER,
            season INTEGER,
            episode INTEGER,
            resolution TEXT
        )
        """
    )

    connection.commit()
