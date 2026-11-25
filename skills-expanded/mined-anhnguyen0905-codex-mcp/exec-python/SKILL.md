---
name: exec-python
description: Python execution idioms to embed into Codex prompts when the target project is Python — PEP 8, type hints, error handling, and packaging conventions.
---

# Python Idioms (embed when project is Python)

```
Python standards:
- PEP 8 naming: snake_case functions/vars, PascalCase classes, UPPER_SNAKE constants.
- Type hints on all public functions (params + return); use modern syntax the project's Python
  version supports (e.g. `list[str]`, `X | None`).
- Errors: raise specific exceptions, never bare `except:`; catch the narrowest type that you can
  actually handle; chain with `raise ... from err` to preserve context.
- No mutable default arguments (def f(x=[]) bug) — use None + assignment.
- Prefer comprehensions/generators over manual loops when clearer; pathlib over os.path;
  f-strings over % or .format; dataclasses (or the project's model library, e.g. pydantic) over
  bare dicts for structured data.
- Context managers (with) for files, locks, connections — never rely on GC for cleanup.
- Respect the project's tooling: existing linter/formatter config (ruff/black), import order,
  and dependency manager (uv/poetry/pip) — add deps only via its manifest.
- Tests: pytest style if the project uses it — plain asserts, fixtures over setUp, parametrize
  for case tables.
```
