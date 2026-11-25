---
name: add-store
description: How to add a data-access repository (a JsonStore subclass) under backend/db/. Use when introducing a new persisted JSON file or new query methods over an existing one.
---

# Add a store (db layer)

All persistent state goes through a **repository** in `backend/db/` — never raw `json.load`/`json.dump` in routes, services, or tools. A store is the only place that knows the storage format. This keeps a future DB migration a drop-in concrete implementation.

## The base class

`JsonStore` (`backend/db/json_store.py`) is stateless — it reads disk on every call. It gives you:
`all()`, `find_by_id(id)`, `query(**filters)`, `count(**filters)`, `insert(item)`, `bulk_insert(items)`, `upsert(item)`, `update_by_id(id, changes)`, `delete(id)`, `replace_all(items)`. It supports two file shapes: a flat list (`root_key=None`) or a keyed dict (`root_key="items"`).

> `_save_raw` is the single write choke point — it fires the checkpoint pre-write hook (RFC `.Codex/rfcs/phase1/a4-inversion.md`) and does atomic writes. Always go through the base store's mutators so writes are checkpointed and crash-safe. Do not write the file yourself.

## Steps

1. **Register the path** in `backend/paths.py` (re-exported from `backend/core/config.py`) as a `*_JSON` constant pointing under `DATA_DIR`. Add it to `__all__`. Never hardcode a path in the store.
2. **Subclass `JsonStore`:**

   ```python
   from backend.paths import WIDGETS_JSON
   from .json_store import JsonStore

   class WidgetStore(JsonStore):
       def __init__(self):
           super().__init__(WIDGETS_JSON, id_field="id", root_key=None)

       # Domain query/normalize methods only — no HTTP, no financial math.
       def query_widgets(self, kind: str | None = None) -> list[dict]:
           items = self._load_items()
           if kind is not None:
               items = [w for w in items if w.get("kind") == kind]
           return items
   ```

3. **Normalize on create.** Follow `CommitmentsStore.create` / `_make_*` helpers: generate ids, coerce types, validate enums against a module-level set, drop unknown keys. Nested-array edits get dedicated methods (`set_*`, `update_*`) — the base only patches top-level fields.
4. **Dependency rule.** `db/` depends only on `core/`. **`db/` must NOT import `ai.*`** (import-linter Contract 2 — the checkpoint hook is inverted via `core.write_hooks`) and must not import `services/` or `api/`. No domain/business rules in a store — those live in `services/`.
5. **No backward-compat shims.** If a schema changes, migrate the data file (script under `backend/scripts/`); never read old + new shapes at once.
6. **Gitignore runtime state.** Caches and runtime-only files (poll state, pending queues) go in `.gitignore`; never stage `backend/data/*`.

## Tests (required)

Every store gets a CRUD/query test, isolated to `tmp_path`. Pattern: `tests/test_positions_stores.py` / `tests/test_commitments_store.py`. Monkeypatch the path constant so the test never touches live `backend/data/*`. See the `write-test` skill.

## Docs

Add the store to the "Data access layer" list in `AGENTS.md`. If it backs a new data file, document the schema in the "Data model" section.

## Verify

`make test` + backend import smoke (see `run-app` skill).
