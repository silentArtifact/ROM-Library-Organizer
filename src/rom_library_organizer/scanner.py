from __future__ import annotations

"""Utilities for scanning directories for ROM files.

The :func:`scan_roms` generator walks a directory tree and yields
information about each ROM file that it finds. Files with unrecognised
extensions are ignored.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Generator

# Common ROM file extensions. This list is intentionally conservative and can
# be expanded in the future as new formats are supported.
ROM_EXTENSIONS: set[str] = {
    ".nes",
    ".sfc",
    ".smc",
    ".gba",
    ".gb",
    ".gbc",
    ".n64",
    ".z64",
    ".v64",
    ".nds",
    ".iso",
    ".bin",
}


@dataclass
class RomInfo:
    """Metadata about a ROM file discovered during scanning."""

    path: Path
    extension: str
    size: int
    name: str


def scan_roms(root_path: str | Path) -> Generator[RomInfo, None, None]:
    """Yield information for ROM files under ``root_path``.

    Parameters
    ----------
    root_path:
        Directory to search for ROM files. Subdirectories are traversed
        recursively.

    Yields
    ------
    RomInfo
        Metadata for each recognised ROM file. Files with extensions not in
        :data:`ROM_EXTENSIONS` are skipped silently.
    """

    root = Path(root_path)
    if not root.exists():
        return

    for path in root.rglob("*"):
        if not path.is_file():
            continue
        ext = path.suffix.lower()
        if ext not in ROM_EXTENSIONS:
            continue
        stat = path.stat()
        yield RomInfo(path=path, extension=ext, size=stat.st_size, name=path.name)
