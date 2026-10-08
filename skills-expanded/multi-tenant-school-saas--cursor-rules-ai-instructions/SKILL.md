# Cursor AI Instructions Bridge

This repository uses `AGENTS.md` as the single source of AI instructions.

Cursor should load this file only to discover and follow the Codex-compatible instruction hierarchy.

## Required Reading

Read `AGENTS.md` first.

Then read the nearest nested `AGENTS.md` file for the area being changed:

* `app/AGENTS.md` for Laravel application code
* `database/AGENTS.md` for migrations, seeders, and factories
* `tests/AGENTS.md` for tests
* `docs/AGENTS.md` for documentation
* `resources/AGENTS.md` for Blade and frontend assets

## Working Rules

* Do not invent architecture.
* Do not add packages or frameworks unless explicitly approved.
* Do not bypass tenant isolation.
* Do not duplicate long documentation sections inside Cursor rules.
* Keep Cursor behavior aligned with `AGENTS.md`.

When uncertain, consult the authoritative documents listed in `AGENTS.md`.
