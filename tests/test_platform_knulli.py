from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from rom_library_organizer.platforms.knulli import KnulliPlatformOrganizer


def test_is_supported(tmp_path: Path) -> None:
    organizer = KnulliPlatformOrganizer()
    rom = tmp_path / "game.nes"
    rom.write_bytes(b"rom")
    assert organizer.is_supported(rom)
    not_rom = tmp_path / "readme.txt"
    not_rom.write_text("hi")
    assert not organizer.is_supported(not_rom)


def test_rename_bios(tmp_path: Path) -> None:
    organizer = KnulliPlatformOrganizer()
    bios_file = tmp_path / "scph1001.bin"
    bios_file.write_bytes(b"bios")
    metadata = {
        "name": "scph1001",
        "extension": ".bin",
        "is_bios": True,
    }
    rel_path = organizer.rename(metadata)
    dest = tmp_path / rel_path
    dest.parent.mkdir(parents=True)
    bios_file.rename(dest)

    assert dest.exists()
    assert dest.parent.name == "bios"
    assert dest.name == "scph1001.bin"


def test_rename_multidisc(tmp_path: Path) -> None:
    organizer = KnulliPlatformOrganizer()
    rom = tmp_path / "ff7_disc2.cue"
    rom.write_bytes(b"data")
    metadata = {
        "platform": "Sony Playstation",
        "name": "Final Fantasy VII",
        "region": "USA",
        "disc": 2,
        "extension": ".cue",
    }
    rel_path = organizer.rename(metadata)
    dest = tmp_path / rel_path
    dest.parent.mkdir(parents=True)
    rom.rename(dest)

    assert dest.exists()
    assert dest.parent.name == "psx"
    assert dest.parent.parent.name == "roms"
    assert dest.name == "Final Fantasy VII (USA) (Disc 2).cue"
