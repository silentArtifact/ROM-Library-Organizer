from rom_library_organizer.renamer import sanitize_filename


def test_sanitize_filename_removes_invalid_characters() -> None:
    original = " Super:Mario 64?.n64 "
    assert sanitize_filename(original) == "Super Mario 64.n64"


def test_sanitize_filename_collapses_whitespace() -> None:
    original = "Foo   Bar\tBaz\n"
    assert sanitize_filename(original) == "Foo Bar Baz"
