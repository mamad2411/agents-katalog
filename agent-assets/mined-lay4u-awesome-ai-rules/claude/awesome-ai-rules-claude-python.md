# Python 3.12+ Project Rules

## Scope
- Applies to Python services, libraries, and CLI tools in this repository.
- Emphasize explicit typing, reproducible environments, and clean architecture.

## Runtime and Tooling Baseline
- Python version: 3.12+.
- Package and environment management must use `uv`.
- Do not use raw `pip` workflows for install, sync, or lock operations.
- Commit lockfiles for deterministic CI and production builds.

## Type Hints
- Type hints are required for:
  - function parameters
  - return types
  - class attributes
  - public module-level constants where non-obvious
- Avoid untyped `dict`/`list` in public interfaces; use typed structures.
- Use `typing` and `collections.abc` generics consistently.

## Linting and Formatting
- Linting tool: Ruff.
- Formatting tool: `ruff format`.
- CI must fail on lint or format violations.
- Keep rule ignores narrow and documented inline when necessary.

## Testing Standards
- Test framework: `pytest`.
- Coverage is required for changed code paths.
- Recommended command: `pytest --cov --cov-report=term-missing`.
- Test naming:
  - files: `test_*.py`
  - functions: `test_<behavior>`

## Web and Async Conventions
- Web services should use FastAPI.
- CLI async workflows should use `asyncio`.
- Avoid blocking I/O inside async code; use async clients/drivers.
- Keep framework code thin and push domain logic into testable services.

## Data Validation
- Use Pydantic v2 for request/response and settings validation.
- Use explicit models for external boundaries (API, queue, file input).
- Prefer strict field constraints over ad hoc manual checks.

## ORM and Persistence
- ORM choices: SQLAlchemy 2.0 or SQLModel.
- Use SQLAlchemy 2.x style APIs (`select()`, `Session` patterns).
- Keep models, repositories, and migrations separated by responsibility.
- Wrap transaction boundaries explicitly in service-layer code.

## Project Structure Guidance
- `src/<package>/api/` FastAPI routers and schemas
- `src/<package>/domain/` business logic and entities
- `src/<package>/infra/` DB, external clients, adapters
- `tests/` unit and integration tests mirroring source layout

## Error Handling and Logging
- Raise specific exception types; avoid broad `except Exception` without re-raise.
- Convert internal exceptions to user-safe messages at boundaries.
- Use structured logging with stable event names and context fields.

## Definition of Done
- `uv sync` and lockfile are up to date.
- Ruff lint and `ruff format --check` pass.
- Pytest suite passes with coverage for changed behavior.
- Added code is fully type-annotated and validated at boundaries.
