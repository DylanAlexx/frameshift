from pathlib import Path

import typer

from frameshift.discovery.scanner import scan as scan_media
from frameshift.library.builder import build_library
from frameshift.persistence.database import connect
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
    connection.close()

    files = list(scan_media(path))
    library = build_library(files)

    render_scan_summary(str(path), library)
    render_scan_results(library)

    console.print(f"\n[bold green]Found {len(files)} media file(s).[/]")


@app.command()
def version() -> None:
    """Show version information."""

    console.print("[bold]FrameShift[/] v0.1.0")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
