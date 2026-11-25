# Python

## Environment and Tooling
- Use `uv` for package management (`uv add`, `uv run`, `uv sync`) not raw pip
- Use `ruff` for linting and formatting, not black or flake8
- Use `pytest` for testing with `pytest-cov` for coverage
- Minimum Python version: 3.11 unless the project specifies otherwise

## Code Style
- Type hints on every function signature, parameters and return type
- Use `|` union syntax (`str | None`) not `Optional[str]`
- Prefer `dataclasses` or `pydantic` models over raw dicts for structured data
- Use `pathlib.Path` everywhere, never `os.path`
- f-strings for all string formatting, no `.format()` or `%`
- `match` statements over long `if/elif` chains where applicable
- Keep functions small and single-purpose

## Imports
- Standard library first, third-party second, local last, separated by blank lines
- Never use wildcard imports (`from x import *`)
- Prefer explicit imports (`from pathlib import Path`) over module imports

## Error Handling
- Never silently swallow exceptions, always log or re-raise
- Use specific exception types, not bare `except:`
- Use `contextlib.suppress` only for truly ignorable errors, and comment why
- Custom exceptions should inherit from a project base exception class

## Async
- Use `asyncio` for I/O-bound concurrency, never `threading` for new code
- Always `await` coroutines, never fire-and-forget unless explicitly intentional
- Use `asyncio.TaskGroup` (Python 3.11+) over `asyncio.gather`

## Testing
- One test file per module: `tests/test_<module>.py`
- Test names: `test_<what>_<condition>_<expected_result>`
- Use `pytest.fixture` for shared setup
- Parametrize repeated logic with `@pytest.mark.parametrize`
- Mock external I/O with `pytest-mock`, never make real network calls in tests

## Documentation
- Google style docstrings on all public functions and classes
- No docstrings on private functions (`_name`) unless logic is non-obvious
- A wrong docstring is worse than none

## Common Patterns

Reading files:
    from pathlib import Path
    content = Path("file.txt").read_text(encoding="utf-8")

Dataclass:
    from dataclasses import dataclass, field

    @dataclass
    class Config:
        host: str
        port: int = 8080
        tags: list[str] = field(default_factory=list)

Context manager:
    from contextlib import contextmanager

    @contextmanager
    def managed_resource():
        resource = acquire()
        try:
            yield resource
        finally:
            release(resource)

Pattern matching:
    match command:
        case "quit":  sys.exit(0)
        case "help":  print_help()
        case _:       print(f"Unknown: {command}")
