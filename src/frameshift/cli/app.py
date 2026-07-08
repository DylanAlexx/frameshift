from pathlib import Path

import typer

from frameshift.discovery.scanner import scan as scan_media
from frameshift.library.builder import build_library
from frameshift.persistence.database import connect, initialize
from frameshift.persistence.media_repository import load_library, save_library
from frameshift.ui.console import console, render_scan_results, render_scan_summary

app = typer.Typer(
    help="Analyze and understand local media libraries.",
    no_args_is_help=True,
)


@app.command()
def scan(path: Path) -> None:
    """Scan a media directory and list all media files."""

    path = path.expanduser().resolve()

    connection = connect()

    try:
        initialize(connection)

        files = list(scan_media(path))
        library = build_library(files)

        save_library(connection, library)

        render_scan_summary(str(path), library)
        render_scan_results(library)

        console.print(f"\n[bold green]Found {len(files)} media file(s).[/]")

    finally:
        connection.close()


@app.command()
def library() -> None:
    """Display the saved media library."""

    connection = connect()

    try:
        library = load_library(connection)

        render_scan_summary("Database", library)
        render_scan_results(library)

        total = (
            len(library.movies)
            + sum(len(series.episodes) for series in library.series)
            + len(library.unknown)
        )

        console.print(f"\n[bold green]Found {total} media file(s).[/]")

    finally:
        connection.close()


@app.command()
def version() -> None:
    """Show version information."""

    console.print("[bold]FrameShift[/] v0.1.0")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
