import re

from frameshift.models.parsed_media import MediaType, ParsedMedia

_TV_PATTERN = re.compile(
    r"(?P<title>.+?)[.\s]+(?:S(?P<season>\d{1,2})E(?P<episode>\d{1,2})|(?P<season2>\d{1,2})x(?P<episode2>\d{1,2}))",
    re.IGNORECASE,
)

_MOVIE_PATTERN = re.compile(r"^(?P<title>.+?)[.\s\(]+(?P<year>19\d{2}|20\d{2})")

_RESOLUTION_PATTERN = re.compile(
    r"\b(480p|720p|1080p|2160p)\b",
    re.IGNORECASE,
)


def parse_filename(filename: str) -> ParsedMedia:
    tv_match = _TV_PATTERN.search(filename)
    resolution_match = _RESOLUTION_PATTERN.search(filename)

    resolution = None
    if resolution_match:
        resolution = resolution_match.group(1).lower()

    if tv_match:
        season = tv_match.group("season") or tv_match.group("season2")
        episode = tv_match.group("episode") or tv_match.group("episode2")

        return ParsedMedia(
            media_type=MediaType.TV_EPISODE,
            title=tv_match.group("title").replace(".", " ").strip(),
            season=int(season),
            episode=int(episode),
            resolution=resolution,
        )

    movie_match = _MOVIE_PATTERN.search(filename)

    if movie_match:
        return ParsedMedia(
            media_type=MediaType.MOVIE,
            title=movie_match.group("title").replace(".", " ").strip(),
            year=int(movie_match.group("year")),
            resolution=resolution,
        )

    return ParsedMedia(media_type=MediaType.UNKNOWN, resolution=resolution)
