from dataclasses import dataclass

from frameshift.models.media_file import MediaFile


@dataclass(slots=True, frozen=True)
class Series:
    title: str
    episodes: list[MediaFile]
