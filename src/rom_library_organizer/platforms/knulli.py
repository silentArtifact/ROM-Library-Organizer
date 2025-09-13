from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from .base import PlatformOrganizer


class KnulliPlatformOrganizer(PlatformOrganizer):
    """Organize ROMs according to Knulli's folder structure.

    Knulli is a custom firmware that stores user data inside a top level
    ``/userdata`` directory. Games reside in ``/userdata/roms/<system>`` while
    BIOS files are kept in ``/userdata/bios``. Filenames may include region and
    disc information in parentheses. This organiser returns paths relative to
    ``/userdata`` so the caller can place the file in the appropriate location.
    """

    SUPPORTED_EXTENSIONS = {
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
        ".cue",
    }

    PLATFORM_MAP = {
        "nintendo 64": "n64",
        "sony playstation": "psx",
        "playstation": "psx",
        "snes": "snes",
        "super nintendo": "snes",
    }

    @classmethod
    def is_supported(cls, file: Path) -> bool:
        """Return ``True`` if ``file`` has a recognised ROM extension."""

        return file.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    @staticmethod
    def _sanitize(value: str) -> str:
        """Return a filesystem-safe version of ``value``."""

        value = re.sub(r"[<>:\"/\\|?*]", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def _platform_folder(self, platform: str) -> str:
        """Return the Knulli folder name for ``platform``."""

        key = platform.lower()
        return self.PLATFORM_MAP.get(key, self._sanitize(platform).lower().replace(" ", ""))

    def rename(self, file_metadata: Mapping[str, Any]) -> str:
        """Return destination path for ``file_metadata``.

        BIOS files are placed in ``bios``. All other files are placed in
        ``roms/<platform>`` with region and disc information appended to the
        filename when available.
        """

        name = self._sanitize(str(file_metadata.get("name", "Unknown")))
        extension = str(file_metadata.get("extension", ""))

        if file_metadata.get("is_bios"):
            return f"bios/{name}{extension}"

        platform = str(file_metadata.get("platform", "unknown"))
        platform_dir = self._platform_folder(platform)
        region = file_metadata.get("region")
        disc = file_metadata.get("disc") or file_metadata.get("disc_number")

        base_name = name
        if region:
            base_name += f" ({region})"
        if disc:
            base_name += f" (Disc {disc})"
        base_name = self._sanitize(base_name)

        return f"roms/{platform_dir}/{base_name}{extension}"
