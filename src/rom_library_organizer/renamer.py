from __future__ import annotations

"""Filename sanitisation utilities.

These helpers strip characters that are problematic on common file systems
and normalise whitespace, producing tidy, portable file names.
"""

import re

# Characters disallowed on Windows filesystems. Using a conservative set keeps
# the resulting names portable across platforms.
_INVALID_CHARS_RE = re.compile(r"[\\/:*?\"<>|]")


def sanitize_filename(name: str) -> str:
    """Return a filesystem-safe version of ``name``.

    The function replaces disallowed characters with a single space,
    collapses consecutive whitespace and trims leading/trailing spaces.
    """

    # Replace invalid characters with a space to keep word boundaries.
    cleaned = _INVALID_CHARS_RE.sub(" ", name)
    # Collapse any run of whitespace into a single space and strip edges.
    cleaned = re.sub(r"\s+", " ", cleaned).strip()
    # Avoid stray spaces before file extensions (e.g. "name .ext").
    cleaned = cleaned.replace(" .", ".")
    return cleaned
