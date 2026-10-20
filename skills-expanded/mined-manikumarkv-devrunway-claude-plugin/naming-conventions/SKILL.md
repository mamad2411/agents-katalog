---
name: naming-conventions
description: Naming standards for the layers code style guides miss — database tables, columns, indexes and constraints, migration files, JSON payload keys, custom headers, environment variables, and test names. Load always.
user-invocable: false
paths:
  - "**/*"
---

Full standards in [naming-conventions.md](naming-conventions.md).

**This skill covers naming at system boundaries — the names that become contracts.** For code identifiers (functions, variables, booleans, files) see `standards`. For route paths and query params see `api-conventions`. For commit and branch names see `standards` and `conventional-commit`.

**Database — the expensive ones:**
- Tables: `snake_case`, plural — `order_items`. Unquoted identifiers fold to lowercase in Postgres, so `orderItems` silently becomes `orderitems`
- Columns: `snake_case`; primary key `id`; foreign key `<singular>_id` matching the referenced table
- Timestamps: `created_at`, `updated_at`, `deleted_at` — always `_at`, always timezone-aware
- Booleans: `is_active`, `has_verified_email` — question form, never a bare adjective
- Indexes: `idx_<table>_<columns>` · Unique: `uq_<table>_<columns>` · Foreign key: `fk_<table>_<referenced>` · Check: `ck_<table>_<rule>`
- Migrations: `<timestamp>_<verb>_<subject>.sql` — `20260902103000_add_email_index_to_users.sql`

**JSON payloads:**
- Pick one casing for keys and hold it at every boundary; convert in a mapping layer, never mid-payload
- Never expose internal column names that leak schema detail you may want to change

**Environment variables:**
- `SCREAMING_SNAKE_CASE`, prefixed by service: `STRIPE_SECRET_KEY`, not `SECRET_KEY`
- Suffix by kind: `_URL`, `_TOKEN`, `_SECRET`, `_KEY`, `_TIMEOUT_MS`
- Anything suffixed `_SECRET`, `_TOKEN`, `_KEY`, or `_PASSWORD` must never be logged or echoed

**Custom headers:** `X-` prefix is deprecated (RFC 6648) — use `<Org>-<Purpose>`, e.g. `Acme-Request-Id`.

**Tests:** name the behaviour and the condition, not the function — `returns 404 when the order does not exist`, not `test getOrder`.

**Severity when reviewing:** naming in application code is a WARNING — renames are cheap. Naming in a **new migration, table, column, or public payload key is a BLOCKER** — those become contracts on merge and cost a migration plus a client release to change.
