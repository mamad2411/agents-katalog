# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Run tests
uv run pytest tests/ -v

# Run a single test
uv run pytest tests/test_e2e.py::test_name -v

# Coverage (CI requires ≥80%)
uv run coverage run -m pytest && uv run coverage report -i --fail-under=80

# Lint/format (ruff via pre-commit)
uv run pre-commit run --all-files

# Install dev dependencies
uv sync --group dev
```

## Architecture

`entropic` is a minimal run-cache for Python simulations. It hashes input parameters to detect duplicate runs and skips redundant computation. The user provides a `runner` callable; entropic manages persistence on top of SQLite/SQLAlchemy.

### Core components

**`store.py` — `Store[ModelT]`**: The main generic class. Constructor requires `runner`, `result_cls` (a user-defined SQLAlchemy model), `results_dir`, and optionally `file_suffix` and `db_url` (default `sqlite:///db.sqlite3`). Uses `NullPool` on every session to avoid connection leaks.

Run flow: params → `hash_dict()` → hash-keyed sidecar JSON in `results_dir` → ingest to SQLite via `_ingest_to_db()` (deletes sidecar on success).

Primary API surface:
- `run_or_retrieve(params)` — cache-hit or run
- `run(params)` — force run even if cached
- `retrieve(params)` — lookup by params hash
- `sweep(params)` — batch run/retrieve over an iterable of param dicts
- `register(params, file_path)` — index an externally produced file
- `delete(params, remove_file)` — delete a record

Module-level `expand_grid(grid)` expands a `{key: [values]}` grid into the full Cartesian product (list of param dicts) for feeding to `sweep`. It is the only product-expansion helper; non-product sweeps are built directly as iterables of dicts.

**`db.py` — `Base`**: SQLAlchemy `DeclarativeBase` with four reserved columns: `id` (str PK, the hash), `result_file` (str), `created_at` (datetime), `custom_data` (JSON/MutableDict). Users subclass `Base` and add their own simulation parameter columns. `apply_patch()` and `_apply_custom_data_patch()` allow partial updates.

**`hashing.py` — `hash_dict(params)`**: Returns the first 16 hex chars of SHA-256 of a canonically normalized JSON payload. `_normalize()` handles: dicts sorted by key, floats rounded to 12 significant figures, enums via `.value`, tuples flattened to lists.

### User-defined model pattern

```python
from entropic import Base, Mapped, mapped_column

class SimResult(Base):
    __tablename__ = "results"
    alpha: Mapped[float] = mapped_column()
    beta: Mapped[float] = mapped_column()

store = Store(runner=my_runner, result_cls=SimResult, results_dir=Path("./results"))
```

The four reserved column names (`id`, `result_file`, `created_at`, `custom_data`) cannot be used as user-defined columns — `Store` validates this at construction time.

### Testing approach

Tests use a real in-memory SQLite DB and `tmp_path` (no mocking of the DB layer). `test_e2e.py` is the primary coverage vehicle — it exercises the full workflow end-to-end with a logistic growth ODE runner writing CSV files.
