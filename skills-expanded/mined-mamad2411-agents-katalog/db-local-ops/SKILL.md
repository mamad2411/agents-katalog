---
name: db-local-ops
description: Wipe or seed the local development database via wipe.sh and seed.sh. Use when resetting dev data, applying demo seed records, or recovering from a bad local DB state.
disable-model-invocation: true
---

# Database Local Ops

## When to use

Use this skill when the user wants to reset local dev data, re-seed demo records, or recover after schema changes on a local database.

## Workflow

1. Confirm `ENV_PROFILE=local` and [`config/profiles/local.toml`](../../../config/profiles/local.toml) target the intended **local** database.
2. Wipe (full volume reset):
   - `./.cursor/skills/db-local-ops/scripts/run.sh wipe`
   - Re-apply schema with `alembic-migrate`; optionally seed afterward.
3. Seed demo data:
   - `./.cursor/skills/db-local-ops/scripts/run.sh seed`
   - Only when seeding is allowed (`APP_ENV=local`; see `docs/database.md`).

## Constraints

- **Wipe and seed are destructive** — local development only.
- Use `./.cursor/skills/db-local-ops/scripts/run.sh` as the canonical wrapper (`wipe` or `seed` subcommand).
- Same scripts for host-app and full-stack workflows (both run via the app container except wipe, which is `compose down -v`).
- Do not run wipe/seed against production or shared databases.
- Tests use a PostgreSQL test database from `tests/conftest.py` (Alembic upgrade); these scripts affect **dev** databases only.
