from dataclasses import dataclass

from frameshift.models.media_file import MediaFile
from frameshift.models.series import Series


@dataclass(slots=True, frozen=True)
class Library:
    movies: list[MediaFile]
    series: list[Series]
    unknown: list[MediaFile]
