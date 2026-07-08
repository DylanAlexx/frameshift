import sqlite3
from pathlib import Path
from sqlite3 import Connection

from frameshift.library.builder import build_library
from frameshift.models.library import Library
from frameshift.models.media_file import MediaFile
from frameshift.models.parsed_media import MediaType, ParsedMedia


def save_library(connection: Connection, library: Library) -> None:
    """Persist a scanned library."""

    rows = []

    # Movies
    for media_file in library.movies:
        parsed = media_file.parsed

        rows.append(
            (
                str(media_file.path),
                media_file.size,
                media_file.extension,
                parsed.media_type.value,
                parsed.title,
                parsed.year,
                None,
                None,
                parsed.resolution,
            )
        )

    # TV Episodes
    for series in library.series:
        for media_file in series.episodes:
            parsed = media_file.parsed

            rows.append(
                (
                    str(media_file.path),
                    media_file.size,
                    media_file.extension,
                    parsed.media_type.value,
                    parsed.title,
                    parsed.year,
                    parsed.season,
                    parsed.episode,
                    parsed.resolution,
                )
            )

    # Unknown
    for media_file in library.unknown:
        parsed = media_file.parsed

        rows.append(
            (
                str(media_file.path),
                media_file.size,
                media_file.extension,
                parsed.media_type.value,
                parsed.title,
                parsed.year,
                parsed.season,
                parsed.episode,
                parsed.resolution,
            )
        )

    connection.executemany(
        """
        INSERT INTO media_files (
            path,
            size,
            extension,
            media_type,
            title,
            year,
            season,
            episode,
            resolution
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(path)
        DO UPDATE SET
            size = excluded.size,
            extension = excluded.extension,
            media_type = excluded.media_type,
            title = excluded.title,
            year = excluded.year,
            season = excluded.season,
            episode = excluded.episode,
            resolution = excluded.resolution
        """,
        rows,
    )

    connection.commit()


def load_library(connection: sqlite3.Connection) -> Library:
    """Load the media library from the database."""

    rows = connection.execute(
        """
        SELECT
            path,
            size,
            extension,
            media_type,
            title,
            year,
            season,
            episode,
            resolution
        FROM media_files
        ORDER BY title
        """
    ).fetchall()

    media_files: list[MediaFile] = []

    for row in rows:
        parsed = ParsedMedia(
            media_type=MediaType(row["media_type"]),
            title=row["title"],
            year=row["year"],
            season=row["season"],
            episode=row["episode"],
            resolution=row["resolution"],
        )

        media_files.append(
            MediaFile(
                path=Path(row["path"]),
                size=row["size"],
                extension=row["extension"],
                parsed=parsed,
            )
        )

    return build_library(media_files)
