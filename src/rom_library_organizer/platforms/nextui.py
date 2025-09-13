from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from .base import PlatformOrganizer


class NextUIPlatformOrganizer(PlatformOrganizer):
    """Organize ROMs according to NextUI's folder structure.

    NextUI groups games first by platform and then by region. The final
    filename includes the disc number when provided. All components are
    sanitised to ensure filesystem compatibility.
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

    def rename(self, file_metadata: Mapping[str, Any]) -> str:
        """Return destination path for ``file_metadata``.

        The path follows NextUI's convention of
        ``<platform>/<region>/<game>[- Disc #]<extension>``. ``region`` is
        required by NextUI to separate releases geographically. ``disc`` (or
        ``disc_number``) is appended to the filename when present.
        """

        platform = self._sanitize(str(file_metadata.get("platform", "Unknown Platform")))
        region = self._sanitize(str(file_metadata.get("region", "Unknown Region")))
        name = self._sanitize(str(file_metadata.get("name", "Unknown Game")))
        extension = str(file_metadata.get("extension", ""))
        disc = file_metadata.get("disc") or file_metadata.get("disc_number")

        base_name = name
        if disc:
            base_name += f" - Disc {disc}"
        base_name = self._sanitize(base_name)

        return f"{platform}/{region}/{base_name}{extension}"
