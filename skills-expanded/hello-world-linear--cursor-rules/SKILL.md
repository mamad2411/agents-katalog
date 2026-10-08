# Cursor Rules for Linear Hello World

## Project Context

This is an AI-native Python project demonstrating the Linear + Cursor + GitHub workflow.

**Tagline:** Linear plans it. Cursor builds it. GitHub controls it. Python runs it.

## Code Style

- Follow PEP 8 and use type hints for all functions
- Use `ruff` for linting and formatting
- Use `mypy` for type checking
- Write docstrings in Google style for all public functions and classes

## Project Structure

```
linear-hello-world/
├─ .cursor/           # Cursor configuration
├─ .linear/           # Linear integration config
├─ src/hello_world/   # Main source code
├─ tests/             # Test suite
├─ main.py            # CLI entry point
├─ pyproject.toml     # Project configuration
└─ Makefile           # Common tasks
```

## Key Commands

- `make install-dev` - Install development dependencies
- `make test` - Run tests
- `make lint` - Run linter
- `make format` - Format code
- `make run` - Run CLI
- `make api` - Start API server

## Dependencies

- **FastAPI** - REST API framework
- **Typer** - CLI framework
- **Rich** - Terminal formatting
- **Pydantic** - Data validation
- **pytest** - Testing framework

## Testing

- All code should have corresponding tests in `tests/`
- Run `make test` before committing
- Maintain test coverage above 80%

## API Design

- REST endpoints follow standard conventions
- Use Pydantic models for request/response validation
- Include OpenAPI documentation

## CLI Design

- Use Typer for CLI commands
- Support both long (`--name`) and short (`-n`) flags
- Include helpful descriptions for all options
