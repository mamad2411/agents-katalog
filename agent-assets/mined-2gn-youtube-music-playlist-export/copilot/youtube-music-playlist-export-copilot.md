# Copilot Instructions

## Project Overview

This is a Python project that exports YouTube Music playlists to M3U playlist files.

## Package Management

Always use **[uv](https://docs.astral.sh/uv/)** for all Python package management tasks. Do not use `pip`, `pip-tools`, `poetry`, or `conda`.

- Add dependencies: `uv add <package>`
- Remove dependencies: `uv remove <package>`
- Install project: `uv sync`
- Run scripts: `uv run <script>`
- Run tools: `uvx <tool>`

Project metadata and dependencies are declared in `pyproject.toml`.

## Development Conventions

- Target Python 3.11+
- Use type hints throughout
- Prefer `pathlib.Path` over `os.path` for file operations
- Output files use the `.m3u` extension (UTF-8 encoded)
