from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from frameshift.models.library import Library

console = Console()

console.rule("[bold cyan]FrameShift[/]")


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
        f"📼 Episodes: {episode_count}\n"
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
        movie_size = sum(movie.size for movie in library.movies)

        console.print()

        console.print(
            Panel(
                (
                    "[bold]🎬 Movies[/]\n\n"
                    f"[cyan]Count:[/] {len(library.movies)}\n"
                    f"[cyan]Size :[/] {format_size(movie_size)}"
                ),
                expand=False,
                border_style="cyan",
            )
        )

        table = Table(show_header=True)

        table.add_column("Title")
        table.add_column("Year", justify="center")
        table.add_column("Video", justify="center")
        table.add_column("Size", justify="right")

        for movie in sorted(
            library.movies,
            key=lambda movie: (
                movie.parsed.title or "",
                movie.parsed.year or 0,
            ),
        ):
            parsed = movie.parsed

            table.add_row(
                parsed.title or movie.path.stem,
                str(parsed.year or "-"),
                parsed.resolution or "[dim]-[/]",
                format_size(movie.size),
            )

        console.print(table)

    #
    # TV Series
    #
    for series in library.series:
        console.print()

        episode_count = len(series.episodes)

        season_count = len(
            {
                episode.parsed.season
                for episode in series.episodes
                if episode.parsed.season is not None
            }
        )

        total_size = sum(episode.size for episode in series.episodes)

        console.print(
            Panel(
                (
                    f"[bold]📺 {series.title}[/]\n\n"
                    f"[cyan]Seasons :[/] {season_count}\n"
                    f"[cyan]Episodes:[/] {episode_count}\n"
                    f"[cyan]Size     :[/] {format_size(total_size)}"
                ),
                expand=False,
                border_style="cyan",
            )
        )

        seasons = sorted(
            {
                episode.parsed.season
                for episode in series.episodes
                if episode.parsed.season is not None
            }
        )

        for season_number in seasons:
            console.print(f"\n[bold]Season {season_number}[/]")

            table = Table(show_header=True)

            table.add_column("Episode", justify="center")
            table.add_column("Video", justify="center")
            table.add_column("Size", justify="right")

            season_episodes = sorted(
                (episode for episode in series.episodes if episode.parsed.season == season_number),
                key=lambda episode: episode.parsed.episode or 0,
            )

            for episode in season_episodes:
                parsed = episode.parsed

                table.add_row(
                    f"E{parsed.episode:02}",
                    parsed.resolution or "-",
                    format_size(episode.size),
                )

            console.print(table)

    #
    # Unknown
    #
    if library.unknown:
        unknown_size = sum(file.size for file in library.unknown)

        console.print()

        console.print(
            Panel(
                (
                    "[bold]❓ Unknown Files[/]\n\n"
                    f"[cyan]Count:[/] {len(library.unknown)}\n"
                    f"[cyan]Size :[/] {format_size(unknown_size)}"
                ),
                expand=False,
                border_style="yellow",
            )
        )

        table = Table(show_header=True)

        table.add_column("Filename")
        table.add_column("Size", justify="right")

        for media_file in sorted(
            library.unknown,
            key=lambda file: file.path.name.lower(),
        ):
            table.add_row(
                media_file.path.name,
                format_size(media_file.size),
            )

        console.print(table)
