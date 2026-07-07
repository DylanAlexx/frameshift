from sqlite3 import Connection

from frameshift.models.library import Library


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
            episode
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(path)
        DO UPDATE SET
            size = excluded.size,
            extension = excluded.extension,
            media_type = excluded.media_type,
            title = excluded.title,
            year = excluded.year,
            season = excluded.season,
            episode = excluded.episode
        """,
        rows,
    )

    connection.commit()
