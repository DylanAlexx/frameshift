from dataclasses import dataclass
from pathlib import Path

from frameshift.models.parsed_media import ParsedMedia


@dataclass(slots=True, frozen=True)
class MediaFile:
    path: Path
    size: int
    extension: str
    parsed: ParsedMedia
