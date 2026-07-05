import re
from enum import Enum


class MediaType(Enum):
    MOVIE = "movie"
    TV_EPISODE = "tv_episode"
    UNKNOWN = "unknown"


# Matches:
# S01E01
# s01e01
# S1E1
# s1e1
# 1x01
# 01x01
_TV_PATTERN = re.compile(
    r"(s\d{1,2}e\d{1,2})|(\d{1,2}x\d{1,2})",
    re.IGNORECASE,
)


def classify_filename(filename: str) -> MediaType:
    """
    Classify a media filename as a movie, TV episode, or unknown.
    """

    if _TV_PATTERN.search(filename):
        return MediaType.TV_EPISODE

    return MediaType.MOVIE
