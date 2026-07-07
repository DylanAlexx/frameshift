from dataclasses import dataclass
from enum import StrEnum


class MediaType(StrEnum):
    MOVIE = "movie"
    TV_EPISODE = "tv_episode"
    UNKNOWN = "unknown"


@dataclass(slots=True, frozen=True)
class ParsedMedia:
    media_type: MediaType
    title: str | None = None
    year: int | None = None
    season: int | None = None
    episode: int | None = None
