from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from frameshift.models.library import Library

console = Console()


def format_size(size: int) -> str:
    """Convert bytes into a human-readable size."""

    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:
        if value < 1024 or unit == units[-1]:
            return f"{value:.1f} {unit}"
        value /= 1024

    return f"{value:.1f} TB"


def render_scan_summary(path: str, library: Library) -> None:
    """Render a summary panel for a scan."""

    movie_count = len(library.movies)
    series_count = len(library.series)
    episode_count = sum(len(series.episodes) for series in library.series)
    unknown_count = len(library.unknown)

    total_size = (
        sum(movie.size for movie in library.movies)
        + sum(episode.size for series in library.series for episode in series.episodes)
        + sum(file.size for file in library.unknown)
    )

    summary = (
        f"[bold]📂 Directory:[/] {path}\n"
        f"🎬 Movies: {movie_count}\n"
        f"📺 TV Series: {series_count}\n"
        f"📼 TV Episodes: {episode_count}\n"
        f"❓ Unknown: {unknown_count}\n"
        f"💾 Total Size: {format_size(total_size)}"
    )

    console.print(
        Panel(
            summary,
            title="[bold cyan]FrameShift Scan[/]",
            expand=False,
        )
    )


def render_scan_results(library: Library) -> None:
    """Display scan results."""

    #
    # Movies
    #
    if library.movies:
        table = Table(title="🎬 Movies")

        table.add_column("Title")
        table.add_column("Year", justify="center")
        table.add_column("Size", justify="right")

        for movie in library.movies:
            parsed = movie.parsed

            table.add_row(
                parsed.title or movie.path.stem,
                str(parsed.year or "-"),
                format_size(movie.size),
            )

        console.print(table)

    #
    # TV Series
    #
    for series in library.series:
        table = Table(title=f"📺 {series.title}")

        table.add_column("Season", justify="center")
        table.add_column("Episode", justify="center")
        table.add_column("Size", justify="right")

        for episode in series.episodes:
            parsed = episode.parsed

            table.add_row(
                str(parsed.season or "-"),
                str(parsed.episode or "-"),
                format_size(episode.size),
            )

        console.print(table)

    #
    # Unknown
    #
    if library.unknown:
        table = Table(title="❓ Unknown")

        table.add_column("Filename")
        table.add_column("Size", justify="right")

        for media_file in library.unknown:
            table.add_row(
                media_file.path.name,
                format_size(media_file.size),
            )

        console.print(table)
