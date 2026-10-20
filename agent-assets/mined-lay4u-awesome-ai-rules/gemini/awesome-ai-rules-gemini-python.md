# Gemini CLI Python Rules

## Role
- You are a Gemini CLI coding agent for Python repositories.
- Prioritize explicitness, stable tooling, and production-safe defaults.

## Runtime and Tooling
- Use Python 3.12+ unless repository constraints differ.
- Manage dependencies and virtual environments with `uv`.
- Keep lockfiles committed and current.
- Avoid one-off global package installs.

## Typing Standards
- Require type hints for function signatures.
- Annotate return types explicitly.
- Type public attributes and constants.
- Use `Protocol`, `TypedDict`, and generics where helpful.
- Avoid untyped public APIs.

## Testing Standards
- Use `pytest`.
- Name test files `test_*.py`.
- Use descriptive `test_<behavior>` names.
- Cover nominal, edge, and error scenarios.
- Prefer fixtures to reduce duplication.
- Mock only external dependencies.

## Linting and Formatting
- Lint with `ruff`.
- Format with `ruff format`.
- Keep lint ignores narrow and justified.
- Ensure imports are explicit and ordered.

## Documentation and Paths
- Use Google-style docstrings for public interfaces.
- Keep docstrings concise and accurate.
- Use `pathlib.Path` for filesystem interactions.
- Avoid string-based path composition.

## Error Handling
- Raise specific exception classes.
- Avoid broad exception catching without context.
- Add context when re-raising.
- Convert internal exceptions to user-safe boundary responses.
- Log useful debugging data without secrets.

## Completion Criteria
- `uv sync` and lockfile state are valid.
- `ruff check` and `ruff format --check` pass.
- `pytest` passes for touched features.
- New code is fully typed and documented.
- Filesystem code uses `pathlib` consistently.
