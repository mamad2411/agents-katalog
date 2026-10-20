---
name: configure-python-service-env
description: >-
  Load this skill when setting up a Python service's environment, code style, or secrets: uv,
  pyproject.toml, type hints, ruff/mypy, settings from environment variables and .env. Auto-load
  when pyproject.toml is edited, a uv command runs, or a secret or BaseSettings class is added.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI for `uv
  sync` / `uv add`. `ruff`, `mypy`, `pytest`, `uvicorn`, `alembic`, `pydantic-settings`, and
  `pip-audit` are not assumed to be installed globally - `uv` installs them into the project
  environment and commands run via `uv run`; `pip-audit` also fetches the vulnerability database
  over the network. Running the service also needs a reachable PostgreSQL instance.
license: Apache-2.0
---

# Configure the Python Service Environment

Keep a service's environment on uv, with secrets loaded from the environment and one lint and type
config. Done when `ruff` and `mypy` pass and `pyproject.toml` matches the config below.

## Procedure

1. Run every command through `uv run`, and change dependencies only with `uv add` / `uv sync`, so
   every run uses the one environment `uv.lock` pins and a stray `pip install` cannot drift it.
2. Load every secret through `pydantic-settings` from the environment, and keep `.env.example` current.
3. Write code to the coding style below.
4. Before every PR, run the three checks under Linting and type checking.
5. Install the pre-commit hook once per clone, per Pre-commit hooks below.

## Rules

### Environment

- Python: **3.12** | Package manager: **uv** | Virtual env: `.venv/` (managed by uv)
- Project manifest: `pyproject.toml` | Lockfile: `uv.lock` (never edit manually)

| Action                      | Command                                |
| --------------------------- | -------------------------------------- |
| Install all dependencies    | `uv sync`                              |
| Add a production dependency | `uv add <package>`                     |
| Add a dev dependency        | `uv add --dev <package>`               |
| Run any command             | `uv run <command>`                     |
| Start development server    | `uv run uvicorn app.main:app --reload` |
| Run tests                   | `uv run pytest`                        |
| Lint                        | `uv run ruff check .`                  |
| Format                      | `uv run ruff format .`                 |
| Type check                  | `uv run mypy .`                        |

**Never edit `uv.lock` manually. Never commit `.env`.**

`pyproject.toml` configuration:

```toml
[project]
name = "your-app"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = ["fastapi", "uvicorn[standard]", "pydantic-settings", "asyncpg", "alembic", "structlog"]

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "N", "B"]

[tool.ruff.lint.isort]
known-first-party = ["app"]

[tool.mypy]
strict = true
python_version = "3.12"
ignore_missing_imports = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Secrets management

- Never hard-code secrets, API keys, or passwords in source code
- Load secrets via `pydantic-settings` (`BaseSettings`) from environment variables / `.env`
- Never commit `.env`; always maintain `.env.example` with placeholder values
- Generate cryptographic secrets: `python -c "import secrets; print(secrets.token_hex(32))"`
- Run `uv run pip-audit` before every release
- Session tokens: `secrets.token_urlsafe(32)`, never logged, never in URLs

### Coding style

- Line length: **88 characters** — ruff/Black default, set in `pyproject.toml`
- Type hints required on all function signatures and class attributes
- Use `Any` only with a comment explaining why
- All `async def` route handlers; all I/O calls use `await`
- Blocking calls stall the event loop: use `await asyncio.sleep()`, never `time.sleep()`

**Docstrings** (Google style, required on all public symbols):

```python
def reserve_stock(order: Order, qty: int) -> ReservationResult:
    """Reserves stock for an order.

    Args:
        order: The order requesting stock.
        qty: Units to reserve.
    Returns:
        ReservationResult with success or failure reason.
    Raises:
        InsufficientStockError: If qty exceeds available stock.
    """
```

One-line summary, then `Args` / `Returns` / `Raises` sections as needed. Omit sections that don't apply.

**Naming:**

| Kind                 | Convention            | Example                        |
| -------------------- | --------------------- | ------------------------------ |
| Variables, functions | `snake_case`          | `session_id`, `validate_event` |
| Classes              | `PascalCase`          | `SessionState`                 |
| Constants            | `UPPER_SNAKE_CASE`    | `MAX_CHALLENGES`               |
| Private members      | `_leading_underscore` | `_apply_event`                 |

**Imports** (three groups, separated by blank lines):

```python
# 1. Standard library
import asyncio

# 2. Third-party
from fastapi import HTTPException
from pydantic import BaseModel

# 3. Local application
from app.models.session import SessionState
```

**Pydantic v2:** Use `BaseModel` for all API request/response types and domain entities.

### Linting and type checking

**ruff** for linting and formatting (do not add flake8, pylint, isort, or Black: one tool and one config cannot disagree with itself). **mypy** for type checking.

Required before every PR:

```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy .
```

Give every `# type: ignore` a comment. Keep `strict = true` when errors appear.

### Pre-commit hooks

Run ruff on every commit, so lint and format errors never reach a PR. Install once per clone with
`uv add --dev pre-commit` and `uv run pre-commit install`. The hooks call ruff through `uv run`, so
they use the version `uv.lock` pins rather than a second copy pinned in the hook config:

```yaml
# .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: ruff-check
        name: ruff check
        entry: uv run ruff check --fix
        language: system
        types: [python]
      - id: ruff-format
        name: ruff format
        entry: uv run ruff format
        language: system
        types: [python]
```

mypy stays out of the hook: it checks the whole program, which is too slow for every commit, so it
runs before the PR. A hook that rewrites a file aborts the commit: re-stage and commit again. Never
commit with `--no-verify` to get past a hook.
