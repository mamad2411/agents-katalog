# Python Skill

You are working on a Python project. Apply these best practices.

## Project Setup

- Use `pyproject.toml` for all project metadata and tool configuration — avoid legacy `setup.py` / `setup.cfg`.
- Use `uv` or `poetry` for dependency management; commit the lockfile.
- Use Python 3.12+ features: type parameter syntax (`type Point = tuple[int, int]`), `tomllib`, `match` statements.

## Type Hints

- Annotate all function signatures and class attributes.
- Use built-in generics directly: `list[str]`, `dict[str, int]`, `tuple[int, ...]` (no need to import from `typing` in 3.9+).
- Use `X | Y` union syntax instead of `Union[X, Y]` (Python 3.10+).
- Use `TypedDict` for dict shapes; use `dataclasses.dataclass` or Pydantic models for structured data.
- Run `mypy --strict` or `pyright` in CI.

## Code Style

- Follow PEP 8; use `ruff` for linting and formatting (replaces `flake8` + `black` + `isort`).
- Use f-strings for interpolation — not `%` formatting or `.format()`.
- Use `pathlib.Path` instead of `os.path` for file system operations.
- Use context managers (`with` statements) for resources (files, DB connections, locks).

## Async

- Use `asyncio` with `async def` / `await` for I/O-bound concurrency.
- Use `asyncio.gather()` for concurrent coroutines.
- Use `anyio` or `trio` for more structured concurrency when needed.
- Add `from __future__ import annotations` to defer evaluation of annotations in async code (Python 3.9).

## Testing

- Use `pytest` with `pytest-asyncio` for async tests.
- Use `tmp_path` fixture for temporary files — never use hardcoded paths in tests.
- Use `monkeypatch` to override environment variables and module attributes.
- Use `pytest.raises(ValueError, match="…")` for expected exception messages.

## Security

- Never use `eval()` or `exec()` with user input.
- Use `secrets` module for cryptographic random values — not `random`.
- Validate and sanitize all external inputs; use Pydantic for structured validation.
- Pin dependencies in `requirements.txt` or the lockfile; run `pip-audit` or `safety` in CI.
