"""Command-line interface for rom_library_organizer."""

from __future__ import annotations

import argparse
from importlib import import_module
from typing import Sequence, Type

from .platforms import PlatformOrganizer


def load_platform_class(name: str) -> Type[PlatformOrganizer]:
    """Dynamically import a platform organizer class by name."""
    module_name = f"rom_library_organizer.platforms.{name}"
    module = import_module(module_name)
    for obj in module.__dict__.values():
        if (
            isinstance(obj, type)
            and issubclass(obj, PlatformOrganizer)
            and obj is not PlatformOrganizer
        ):
            return obj
    raise ValueError(f"No PlatformOrganizer subclass found in {module_name}")


def main(argv: Sequence[str] | None = None) -> None:
    """Parse command-line arguments and execute the organizer."""
    parser = argparse.ArgumentParser(
        description="Organize a ROM library for selected platforms",
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
    organizers: list[PlatformOrganizer] = []
    for name in args.platforms:
        try:
            cls = load_platform_class(name)
            organizers.append(cls())
            print(f"Loaded platform organizer: {name}")
        except ModuleNotFoundError:
            print(f"Unknown platform: {name}")
        except ValueError as exc:
            print(str(exc))
    if not organizers:
        print("No platforms selected.")


if __name__ == "__main__":
    main()
