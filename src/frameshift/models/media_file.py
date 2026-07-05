from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class MediaFile:
    path: Path
    size: int
    extension: str
