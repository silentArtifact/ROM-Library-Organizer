"""Command-line interface for rom_library_organizer."""

from __future__ import annotations

import argparse
from typing import Sequence


def main(argv: Sequence[str] | None = None) -> None:
    """Parse command-line arguments and execute the organizer."""
    parser = argparse.ArgumentParser(
        description="Organize a ROM library for selected platforms"
    )
    parser.add_argument(
        "target_directory",
        help="Directory containing the ROM files to organize",
    )
    parser.add_argument(
        "platforms",
        nargs="*",
        help="Names of the platforms to process",
    )
    args = parser.parse_args(argv)

    print(f"Target directory: {args.target_directory}")
    if args.platforms:
        print(f"Selected platforms: {', '.join(args.platforms)}")
    else:
        print("No platforms selected.")


if __name__ == "__main__":
    main()
