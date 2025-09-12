from pathlib import Path
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from rom_library_organizer.scanner import scan_roms


def test_scan_roms_filters_and_reports(tmp_path: Path) -> None:
    rom = tmp_path / "game.nes"
    rom.write_bytes(b"abc")
    ignored = tmp_path / "notes.txt"
    ignored.write_text("not a rom")

    results = list(scan_roms(tmp_path))
    assert len(results) == 1
    info = results[0]
    assert info.path == rom
    assert info.extension == ".nes"
    assert info.size == 3
    assert info.name == "game.nes"
    # ensure unknown file is not included
    assert all(res.path != ignored for res in results)
