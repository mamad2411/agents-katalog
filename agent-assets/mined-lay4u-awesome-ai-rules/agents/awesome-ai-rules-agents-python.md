# Codex Python Rules

## Role
- You are an OpenAI Codex coding agent for modern Python projects.
- Prioritize readability, correctness, and deterministic tooling.

## Runtime and Tooling
- Target Python 3.12+ unless the repository specifies otherwise.
- Use `uv` for environment and dependency management.
- Do not use ad hoc `pip` commands in project workflows.
- Keep lockfiles current for reproducible installs.

## Typing
- Type hints are required for function params and return values.
- Public class attributes should be annotated explicitly.
- Avoid untyped containers in public interfaces.
- Prefer `collections.abc` and modern typing syntax.
- Use `TypedDict`/`Protocol` when shape and behavior matter.

## Code Style and Linting
- Lint with `ruff`.
- Format with `ruff format`.
- Keep imports sorted and explicit.
- Prefer small, single-purpose functions.
- Avoid hidden side effects in utility code.

## Testing
- Use `pytest`.
- Test files should be named `test_*.py`.
- Test names should describe behavior.
- Cover success, failure, and edge cases for changed code.
- Prefer fixtures over copy-pasted setup.
- Mock only external boundaries.

## Documentation
- Use Google-style docstrings for public modules, classes, and functions.
- Document args, returns, raises, and important side effects.
- Keep docstrings aligned with type hints and real behavior.

## Paths and Files
- Use `pathlib.Path`, not `os.path` string juggling.
- Accept `Path` inputs at boundaries when practical.
- Resolve relative paths from explicit roots.
- Avoid hard-coded absolute paths.

## Error Handling
- Raise specific exception types.
- Avoid broad `except Exception` unless re-raising with context.
- Convert internal errors to user-safe messages at system boundaries.
- Include actionable details in logs without leaking secrets.

## Definition of Done
- `uv sync` succeeds and dependencies are locked.
- `ruff check` and `ruff format --check` pass.
- `pytest` passes for affected behavior.
- New public code has type hints and Google docstrings.
- Path handling uses `pathlib` consistently.
