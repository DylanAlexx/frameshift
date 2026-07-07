from collections import defaultdict

from frameshift.models.library import Library
from frameshift.models.media_file import MediaFile
from frameshift.models.parsed_media import MediaType
from frameshift.models.series import Series


def build_library(files: list[MediaFile]) -> Library:
    """Build an organized media library."""

    movies: list[MediaFile] = []
    unknown: list[MediaFile] = []

    series_lookup: dict[str, list[MediaFile]] = defaultdict(list)

    for media_file in files:
        parsed = media_file.parsed

        match parsed.media_type:
            case MediaType.MOVIE:
                movies.append(media_file)

            case MediaType.TV_EPISODE:
                title = parsed.title or "Unknown Series"
                series_lookup[title].append(media_file)

            case _:
                unknown.append(media_file)

    movies.sort(key=lambda movie: (movie.parsed.title or "", movie.parsed.year or 0))

    series = [
        Series(
            title=title,
            episodes=sorted(
                episodes,
                key=lambda episode: (
                    episode.parsed.season or 0,
                    episode.parsed.episode or 0,
                ),
            ),
        )
        for title, episodes in sorted(series_lookup.items())
    ]

    unknown.sort(key=lambda media: media.path.name)

    return Library(
        movies=movies,
        series=series,
        unknown=unknown,
    )
