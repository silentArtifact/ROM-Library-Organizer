from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from rom_library_organizer.platforms.nextui import NextUIPlatformOrganizer


def test_is_supported(tmp_path: Path) -> None:
    organizer = NextUIPlatformOrganizer()
    rom = tmp_path / "game.nes"
    rom.write_bytes(b"rom")
    assert organizer.is_supported(rom)
    not_rom = tmp_path / "readme.txt"
    not_rom.write_text("hi")
    assert not organizer.is_supported(not_rom)


def test_rename(tmp_path: Path) -> None:
    organizer = NextUIPlatformOrganizer()
    rom = tmp_path / "ff7_disc2.bin"
    rom.write_bytes(b"data")
    metadata = {
        "platform": "Sony Playstation",
        "name": "Final Fantasy VII",
        "region": "USA",
        "disc": 2,
        "extension": ".bin",
    }
    rel_path = organizer.rename(metadata)
    dest = tmp_path / rel_path
    dest.parent.mkdir(parents=True)
    rom.rename(dest)

    assert dest.exists()
    assert dest.parent.name == "USA"
    assert dest.parent.parent.name == "Sony Playstation"
    assert dest.name == "Final Fantasy VII - Disc 2.bin"
