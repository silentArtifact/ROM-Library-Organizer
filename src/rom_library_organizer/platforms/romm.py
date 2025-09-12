from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Mapping

from .base import PlatformOrganizer


class ROMMPlatformOrganizer(PlatformOrganizer):
    """Organize ROMs following ROMM's folder structure."""

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

        The path follows ROMM's convention of
        ``<platform>/<game>/<game><extension>``. ``game`` includes the region
        in parentheses when provided.
        """

        platform = self._sanitize(str(file_metadata.get("platform", "Unknown Platform")))
        name = self._sanitize(str(file_metadata.get("name", "Unknown Game")))
        region = file_metadata.get("region")
        extension = str(file_metadata.get("extension", ""))

        base_name = f"{name} ({region})" if region else name
        base_name = self._sanitize(base_name)

        return f"{platform}/{base_name}/{base_name}{extension}"
