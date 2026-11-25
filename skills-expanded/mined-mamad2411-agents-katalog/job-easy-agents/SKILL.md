# AGENTS.md — Job-Easy

## Purpose

This file orients agentic coding assistants working in this repository.
It summarizes build/lint/test commands and local coding conventions.

## Quick Context

- Python project targeting `>=3.12` with `hatchling` build backend.
- Entry point: `job-easy` (from `src.__main__:main`).
- Core packages: `browser-use`, `pydantic`, `litellm`.
- Source code lives in `src/`; tests live under `tests/`.
- Pytest defaults: `-v --tb=short` (see `pyproject.toml`).

## Setup & Environment

- Always use the repository `.venv` for running commands (activate it or call `.venv/bin/python`, `.venv/bin/pytest`, etc.).
- Install dev dependencies: `pip install -e ".[dev]"`
- Environment variables live in `.env` (see `.env.example`).
- Fit scoring uses a profile YAML (see `profiles/profile.example.yaml`).

## Build & Run

- Build wheel/sdist (requires `build`): `python -m build`
- Run the CLI entrypoint: `job-easy <args>`
- Run module directly: `python -m src single <job_url>`

## Lint & Format

- Lint (ruff): `ruff check .`
- Format (ruff): `ruff format .`
- Check formatting only: `ruff format --check .`
- Ruff config: `pyproject.toml` (line length 88, target py312, double quotes).
- Lint rules: `E`, `W`, `F`, `I`, `B`, `C4`, `UP`, `ARG`, `SIM`.

## Tests

- Run all tests: `pytest`
- Run tests in a folder: `pytest tests/unit/tracker/`
- Run a single file: `pytest tests/unit/tracker/test_fingerprint.py`
- Run a single test function: `pytest tests/unit/tracker/test_fingerprint.py::test_fingerprint_with_job_id_returns_stable_hash`
- Run by keyword: `pytest -k fingerprint`
- Run integration tests only (targeted): `pytest tests/integration/test_specific.py -m integration`
- Avoid running all integration tests at once; scope to a file or test.
- Run slow tests only: `pytest -m slow`
- Run with coverage: `pytest --cov=src --cov-report=term-missing`
- Async tests use `pytest-asyncio` with `asyncio_mode=auto`.

## TDD Expectations (from `conductor/workflow.md`)

- Use TDD for core modules (tracker, extractor, tailoring, config).
- Write the failing test first, then implement, then refactor.
- Add tests for edge cases and critical paths.

## Test Naming

- Use `test_<unit>_<scenario>_<expected>()` naming.
- Example: `test_tracker_insert_duplicate_raises_error()`.

## Code Style Guidelines

### Imports

- Use `from __future__ import annotations` at the top of modules.
- Group imports: standard library, third-party, first-party (`src.*`).
- Ruff enforces import sorting (isort behavior).
- Avoid unused imports; ruff checks this.

### Formatting

- Follow ruff formatting (similar to Black, 88-char lines).
- Use double quotes for strings (`tool.ruff.format`).
- Prefer trailing commas in multi-line literals.

### Typing & Pydantic

- Use type hints on public interfaces and return types.
- Prefer `list[str]`/`dict[str, Any]` over `List`/`Dict`.
- Use `str | None` union syntax instead of `Optional[str]`.
- Pydantic models use `BaseModel` and `Field` metadata.
- Favor `model_validate` / `model_dump` for serialization.

### Naming

- Modules: snake_case filenames.
- Functions/variables: `snake_case`.
- Classes: `PascalCase`.
- Constants: `UPPER_SNAKE_CASE`.
- Enums/choices: use `Literal` or enum types as appropriate.

### Error Handling

- Prefer early returns for invalid states.
- Avoid bare `except`; catch specific exceptions.
- When suppressing errors, use `contextlib.suppress` with narrow scope.
- Return structured error info (e.g., `errors=["..."]`) when applicable.

### Logging

- Use module-level loggers: `logger = logging.getLogger(__name__)`.
- Log summaries for decisions (fit scoring, overrides, blockers).
- Avoid logging secrets or user credentials.

### I/O & Paths

- Use `pathlib.Path` for filesystem operations.
- Create directories with `mkdir(parents=True, exist_ok=True)`.
- Avoid hard-coded paths; prefer settings/config values.

### Async

- Use `async def` for I/O-bound operations.
- Await service calls rather than blocking.

## Architecture Notes

- `tracker` handles duplicate detection and persistence.
- `extractor` pulls structured job descriptions.
- `scoring` evaluates fit against a profile.
- `tailoring` generates resumes/cover letters.
- `runner` coordinates browser automation flows.
- `hitl` contains human-in-the-loop prompts.

## Safety Requirements (Non-Negotiable)

- No auto-submit without explicit user confirmation.
- Prompt on duplicate detection; log override reasons.
- Never automate CAPTCHA/2FA bypass.
- Never fabricate experience or claims in documents.

## Conventional Commits (from `conductor/workflow.md`)

- Format: `<type>(<scope>): <description>`
- Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`.
- Example: `feat(tracker): add fingerprint-based duplicate detection`.

## Cursor/Copilot Rules

- No `.cursor/rules/`, `.cursorrules`, or `.github/copilot-instructions.md` found.

## Tips for Agents

- Respect existing module boundaries (tracker/extractor/tailoring/etc.).
- Keep changes minimal and consistent with existing patterns.
- Update tests when behavior changes.
- Use ruff + pytest before finishing work.
- Avoid adding secrets to config or commits.
