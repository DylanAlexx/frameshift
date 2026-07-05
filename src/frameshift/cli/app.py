from pathlib import Path

import typer

from frameshift.discovery.scanner import scan as scan_media

app = typer.Typer(
    help="Analyze and understand local media libraries.",
    no_args_is_help=True,
)


@app.command()
def scan(path: Path) -> None:
    """Scan a media directory and list all media files."""

    path = path.expanduser().resolve()

    typer.echo(f"Scanning: {path}")

    count = 0

    for media_file in scan_media(path):
        typer.echo(media_file.path)
        count += 1

    typer.echo(f"\nFound {count} media file(s).")


@app.command()
def version() -> None:
    """Show version information."""
    typer.echo("frameshift 0.1.0")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
