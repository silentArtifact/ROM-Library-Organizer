# Contributing

Thank you for your interest in contributing to ROM Library Organizer! This document outlines the process and standards for contributing.

## Coding Standards

- Follow [PEP 8](https://peps.python.org/pep-0008/) style guidelines.
- Use type hints for new code and prefer explicit imports.
- Keep functions small and focused; add docstrings for public methods and classes.

## Testing

- Install development dependencies: `pip install -e .`
- Run the test suite with `pytest` and ensure all tests pass before submitting a pull request.
- Add tests for any new features or bug fixes.

## Adding Support for a New Platform

1. Create a new module in `src/rom_library_organizer/platforms/` that subclasses `PlatformOrganizer`.
2. Implement the required `is_supported` and `rename` methods.
3. Add tests under `tests/` covering the new platform logic.
4. Document the platform in the README and include a CLI example.

## Submitting Changes

- Fork the repository and create your feature branch from `main`.
- Commit your changes with clear, descriptive messages.
- Open a pull request and describe the motivation and approach.

We appreciate your help in improving ROM Library Organizer!
