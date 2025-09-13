from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from .base import PlatformOrganizer


class BatoceraPlatformOrganizer(PlatformOrganizer):
    """Organize ROMs according to Batocera's folder structure.

    Batocera expects one directory per system inside the global ``roms``
    folder and a top-level ``bios`` directory for firmware files. Game names
    may include region and disc information in parentheses.
    """

    # Batocera supports a wide array of ROM extensions. For the purposes of
    # the organiser we keep this intentionally small and focused on the common
    # formats shared with the rest of this project. BIOS files often use the
    # same extensions as ROMs (e.g. ``.bin``) so they are included here as
    # well.
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

    #: Mapping of human readable platform names to Batocera folder names.
    #: Only a handful are required for the tests but the mapping can easily be
    #: extended in the future.
    PLATFORM_MAP = {
        "nintendo 64": "n64",
        "sony playstation": "psx",
        "playstation": "psx",
        "snes": "snes",
        "super nintendo": "snes",
    }

    @classmethod
    def is_supported(cls, file: Path) -> bool:
        """Return ``True`` if ``file`` has a recognised extension."""

        return file.suffix.lower() in cls.SUPPORTED_EXTENSIONS

    @staticmethod
    def _sanitize(value: str) -> str:
        """Return a filesystem-safe version of ``value``."""

        value = re.sub(r"[<>:\"/\\|?*]", " ", value)
        value = re.sub(r"\s+", " ", value)
        return value.strip()

    def _platform_folder(self, platform: str) -> str:
        """Return the Batocera folder name for ``platform``."""

        key = platform.lower()
        return self.PLATFORM_MAP.get(key, self._sanitize(platform).lower().replace(" ", ""))

    def rename(self, file_metadata: Mapping[str, Any]) -> str:
        """Return destination path for ``file_metadata``.

        If ``is_bios`` is set in ``file_metadata`` the file is placed in the
        ``bios`` directory, otherwise it is placed in the appropriate system
        folder under ``roms`` with region and disc information appended to the
        filename when available.
        """

        name = self._sanitize(str(file_metadata.get("name", "Unknown")))
        extension = str(file_metadata.get("extension", ""))

        # Handle BIOS files which reside in a dedicated top level directory.
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

        return f"{platform_dir}/{base_name}{extension}"
