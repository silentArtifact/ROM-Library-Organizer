from pathlib import Path

from rom_library_organizer.platforms.romm import ROMMPlatformOrganizer


def test_is_supported(tmp_path: Path) -> None:
    organizer = ROMMPlatformOrganizer()
    rom = tmp_path / "game.nes"
    rom.write_bytes(b"rom")
    assert organizer.is_supported(rom)
    not_rom = tmp_path / "readme.txt"
    not_rom.write_text("hi")
    assert not organizer.is_supported(not_rom)


def test_rename_and_place(tmp_path: Path) -> None:
    organizer = ROMMPlatformOrganizer()
    rom = tmp_path / "oot.z64"
    rom.write_bytes(b"data")
    metadata = {
        "platform": "Nintendo 64",
        "name": "Legend of Zelda: Ocarina of Time",
        "region": "USA",
        "extension": ".z64",
    }
    rel_path = organizer.rename(metadata)
    dest = tmp_path / rel_path
    dest.parent.mkdir(parents=True)
    rom.rename(dest)

    assert dest.exists()
    assert dest.name == "Legend of Zelda Ocarina of Time (USA).z64"
    assert dest.parent.name == "Legend of Zelda Ocarina of Time (USA)"
    assert dest.parent.parent.name == "Nintendo 64"
