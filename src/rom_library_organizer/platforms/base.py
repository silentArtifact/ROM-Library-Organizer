from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Mapping


class PlatformOrganizer(ABC):
    """Abstract base class for platform-specific ROM organization."""

    @classmethod
    @abstractmethod
    def is_supported(cls, file: Path) -> bool:
        """Return ``True`` if the given file is handled by this platform."""

    @abstractmethod
    def rename(self, file_metadata: Mapping[str, Any]) -> str:
        """Return the new filename for ``file_metadata``."""
