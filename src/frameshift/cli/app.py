from pathlib import Path

import typer

app = typer.Typer(
    name="frameshift",
    help="Analyze and understand local media libraries.",
)


@app.command()
def scan(
    path: Path = typer.Argument(
        ...,
        help="Path to the media library to scan.",
        exists=True,
        file_okay=False,
        dir_okay=True,
        readable=True,
        resolve_path=True,
    ),
) -> None:
    """Run a scan of the configured media library."""
    typer.echo(f"Scanning: {path}")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
