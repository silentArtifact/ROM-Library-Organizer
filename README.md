# ROM Library Organizer

ROM Library Organizer is a tool designed to help manage and organize collections of video game ROMs.

## Installation

```bash
pip install rom-library-organizer
```

### Manual installation (no PyPI access)

1. Download the source code (clone this repository or grab a release archive) and move into the project directory.
2. (Optional) Create and activate a virtual environment.
3. Build a wheel locally so you can install without hitting PyPI:
   ```bash
   python -m pip install --upgrade build
   python -m build
   ```
   The wheel is written to `dist/`.
4. Install from the wheel directly:
   ```bash
   python -m pip install dist/rom_library_organizer-*.whl
   ```

This keeps the entire installation process offline after fetching the source.

For development installation from source:

```bash
pip install -e .
```

## Basic Usage

After installation, run:

```bash
rom-library-organizer
```

This command currently displays a placeholder message.

## CLI Examples

The tool accepts a directory of ROM files and one or more platform names. The
examples below show how to invoke the organizer for each supported platform.

### Batocera

```bash
rom-library-organizer /path/to/roms batocera
```

### Knulli

```bash
rom-library-organizer /path/to/roms knulli
```

### NextUI

```bash
rom-library-organizer /path/to/roms nextui
```

### ROMM

```bash
rom-library-organizer /path/to/roms romm
```

## Goals

- Provide a command-line interface for organizing ROM files.
- Support metadata scraping and library management.
- Offer extensible plugin architecture for various console platforms.

## NextUI Metadata

When organizing ROMs for the hypothetical *NextUI* frontend, the
``NextUIPlatformOrganizer`` expects a couple of extra metadata fields:

- ``region`` – used to group games inside platform folders. When missing,
  files fall back to ``Unknown Region``.
- ``disc`` / ``disc_number`` – optional number appended to the filename as
  ``- Disc X`` for multi-disc titles.

The resulting structure follows ``<platform>/<region>/<game>[- Disc #]<ext>``.
