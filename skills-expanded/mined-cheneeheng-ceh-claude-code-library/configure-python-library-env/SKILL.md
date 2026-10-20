---
name: configure-python-library-env
description: >-
  Load this skill when setting up a Python library's environment or code style: uv dependencies,
  pyproject.toml, type hints, docstrings, naming, ruff/mypy. Auto-load when pyproject.toml is edited
  or a uv command runs.
disable-model-invocation: false
user-invocable: false
compatibility: >-
  Requires Python 3.12+ and the `uv` package manager on PATH, plus network access to PyPI for `uv
  sync` / `uv add`. `ruff`, `mypy`, and `pytest` are not assumed to be installed globally - `uv`
  installs them into the project environment and every command runs via `uv run`.
license: Apache-2.0
---

# Configure the Python Library Environment

Keep a library's environment on uv, with a minimal runtime dependency set and one lint and type
config. Done when `ruff` and `mypy` pass and `pyproject.toml` matches the config below.

## Procedure

1. Run every command through `uv run`, and change dependencies only with `uv add` / `uv sync`, so
   every run uses the one environment `uv.lock` pins and a stray `pip install` cannot drift it.
2. Before adding a runtime dependency, check that every consumer should inherit it. If not, make it
   a dev dependency or an optional extra.
3. Write code to the coding style below.
4. Before every PR, run the three checks under Linting and type checking.
5. Install the pre-commit hook once per clone, per Pre-commit hooks below.

## Rules

### Environment

- Python: **3.12** | Package manager: **uv** | Virtual env: `.venv/` (managed by uv)
- Project manifest: `pyproject.toml` | Lockfile: `uv.lock` (never edit manually)

| Action                      | Command                  |
| --------------------------- | ------------------------ |
| Install all dependencies    | `uv sync`                |
| Add a production dependency | `uv add <package>`       |
| Add a dev dependency        | `uv add --dev <package>` |
| Run any command             | `uv run <command>`       |
| Run tests                   | `uv run pytest`          |
| Lint                        | `uv run ruff check .`    |
| Format                      | `uv run ruff format .`   |
| Type check                  | `uv run mypy .`          |

**Never edit `uv.lock` manually. Never commit `.env`.**

Keep the runtime dependency set minimal — a library inherits onto every consumer. Do not add web-service
dependencies (`fastapi`, `uvicorn`, `asyncpg`); those belong to applications, not libraries.

`pyproject.toml` configuration:

```toml
[project]
name = "your-library"
version = "0.1.0"
requires-python = ">=3.12"
dependencies = []  # keep minimal; every dependency is imposed on consumers

[tool.ruff]
line-length = 88

[tool.ruff.lint]
select = ["E", "F", "I", "UP", "N", "B"]

[tool.ruff.lint.isort]
known-first-party = ["your_library"]

[tool.mypy]
strict = true
python_version = "3.12"
ignore_missing_imports = false

[tool.pytest.ini_options]
asyncio_mode = "auto"
```

### Coding style

- Line length: **88 characters** — ruff/Black default, set in `pyproject.toml`
- Type hints required on all function signatures and class attributes
- Use `Any` only with a comment explaining why

**Docstrings** (Google style, required on all public symbols):

```python
def parse_duration(text: str) -> timedelta:
    """Parses a human duration string into a timedelta.

    Args:
        text: Duration like "1h30m" or "45s".
    Returns:
        The parsed timedelta.
    Raises:
        ValueError: If the string cannot be parsed.
    """
```

One-line summary, then `Args` / `Returns` / `Raises` sections as needed. Omit sections that don't apply.

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
