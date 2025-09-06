# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Platform_utils is a cross-platform Python library that provides utilities for:
- Path manipulation (application data paths, frozen app detection, cross-platform paths)
- Clipboard operations (get/set text)
- User idle time detection (Windows)
- Process management (killing processes)
- Shell integration (Windows context menu)
- Output suppression for py2exe

## Build System and Package Management

This project uses **uv** as the package manager and build tool with hatchling as the build backend.

### Common Commands

**Building the package:**
```bash
uv build
```

**Running tests:**
```bash
uv run python -m unittest discover -s tests
```

**Running a specific test:**
```bash
uv run python -m unittest tests.test_paths
uv run python -m unittest tests.test_paths.TestModulePath.test_module_path
```

**Installing in development mode:**
```bash
uv sync
```

**Publishing (for releases):**
```bash
uv publish
```

## Architecture

The library is organized into focused modules:

- **`paths.py`** - Core path utilities using platformdirs library with Windows-specific extensions via `_winpaths.py`
- **`clipboard.py`** - Cross-platform clipboard operations with Windows (pywin32) and Unix (subprocess) implementations  
- **`idle.py`** - Windows user idle time detection using win32api
- **`process.py`** - Process management utilities
- **`blackhole.py`** - stdout/stderr suppression for py2exe
- **`shell_integration/`** - Windows shell context menu integration

Platform detection is handled centrally in `paths.py` with `is_windows`, `is_mac`, `is_linux` flags and `is_frozen()` for detecting packaged applications.

## Dependencies

- **platformdirs** - Cross-platform directory utilities
- **pywin32** - Windows-specific APIs (Windows only)

## Testing

Tests use Python's built-in unittest framework and are located in the `tests/` directory. Currently only `test_paths.py` exists with cross-platform path testing.

## Release Process

Releases are automated via GitHub Actions when tags are pushed. The workflow uses uv to build and publish to PyPI.