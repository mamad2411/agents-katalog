# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Portman** is a CLI tool for managing port allocations across multiple git worktrees and development contexts. It prevents port conflicts when running Docker services by automatically allocating unique ports per context and integrating with direnv for seamless environment variable management.

## Development Commands

### Setup
```bash
# Install in editable mode (development)
uv pip install -e .

# Install with dev dependencies
uv sync --all-groups
```

### Testing
```bash
# Run all tests with coverage
uv run pytest

# Run specific test file
uv run pytest tests/test_discovery.py

# Run specific test function
uv run pytest tests/test_discovery.py::test_discover_services_with_custom_compose_file

# Run tests without coverage report
uv run pytest --no-cov
```

### Linting
```bash
# Run all linting (required before commits)
uv run ruff check .
uv run ruff format --check src tests
uv run mypy src

# Auto-fix ruff issues
uv run ruff check --fix .

# Format code
uv run ruff format src tests
```

### Running the CLI in Development
```bash
# Use the venv binary for testing local changes
.venv/bin/portman --help

# Or install and use globally
uv pip install -e .
portman --help
```

### Debugging
```bash
# Enable debug logging
PORTMAN_DEBUG=1 portman discover -f docker-compose.yml
```

## Architecture

### Core Components

**Context System** (`context.py`):
- Generates unique hashes for project paths + git worktrees
- Context hash = `sha256(absolute_path + git_branch_or_worktree)`
- Enables per-worktree port isolation on the same machine

**Port Allocation** (`allocator.py`):
- Service-type-aware port ranges (e.g., Postgres: 5432-5532)
- System port scanning to avoid conflicts
- Preferred port support with fallback to range allocation

**Database Layer** (`db.py`):
- SQLite database at `~/.local/share/portman/allocations.db`
- Stores: context_hash, service_name, allocated_port, timestamps
- Enforces uniqueness constraints on ports and context+service pairs

**Service Discovery** (`discovery.py`):
- Parses `docker-compose.yml` files for port definitions
- Handles bash parameter expansion syntax: `${VAR:-default}`
- Supports both short format (`"${PORT}:5432"`) and long format (`{published: "${PORT}", target: 5432}`)
- Infers service types from names/images for intelligent port range selection

**CLI Structure** (`cli.py` + `commands/`):
- Modular command structure: one file per command in `src/portman/commands/`
- Each command is a standalone module imported and registered in `cli.py`
- Shared utilities in `commands/common.py`

**Console Utilities** (`console.py`):
- Centralized output formatting with Rich
- Debug mode controlled by `PORTMAN_DEBUG` environment variable
- Functions: `debug()`, `info()`, `success()`, `warning()`, `error()`

### Key Data Flow

1. **Port Booking**: Command → Context detection → Check DB → Allocator → System port scan → DB insert
2. **Port Export**: Context detection → DB query → Format env vars → Output for direnv
3. **Auto-discovery**: Parse compose file → Extract services → Book each service → Store in DB

## Important Implementation Details

### Docker Compose Port Parsing

The discovery system handles multiple port definition formats:
- Bare ports: `"5432"` → auto-generate env var `SERVICE_PORT`
- Env vars: `"${PG_PORT}:5432"` or `"$PG_PORT:5432"` → extract `PG_PORT`
- Bash defaults: `"${PG_PORT:-5432}:5432"` → extract `PG_PORT`, ignore default
- Explicit mappings: `"8080:80"` → skip (no dynamic allocation needed)

**Regex pattern** (in `discovery.py:152`): `r"^\$\{?(\w+)(?::-[^}]+)?\}?:(\d+)(?:/\w+)?$"`

### Version Management

Version is defined in two places and must stay in sync:
- `pyproject.toml` - line 3: `version = "X.Y.Z"`
- `src/portman/__init__.py` - line 3: `__version__ = "X.Y.Z"`

### Command Registration Pattern

New commands should follow this pattern:
1. Create file in `src/portman/commands/your_command.py`
2. Import shared utilities from `.common` (console, get_db)
3. Define function with Typer decorators
4. Add import in `src/portman/commands/__init__.py`
5. Register in `src/portman/cli.py` with `app.command()(your_command)`

## Commit Guidelines

- Do NOT mention AI assistance in commit messages
- Use conventional commits format: `type: description`
- Types: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`
- Keep subject line under 72 characters
- Use imperative mood ("add feature" not "added feature")

## Testing Philosophy

- Unit tests for core logic (allocator, discovery, context, db)
- Integration tests use temporary directories and databases
- Mock filesystem operations where appropriate
- All new features require corresponding tests
- Test coverage target: >80% for core modules
