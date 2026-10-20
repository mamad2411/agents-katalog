---
name: safe-migration
description: Write a database migration the zero-downtime, review-safe way — additive-first (add nullable → backfill → tighten), never edit a shipped migration, and ship RLS + allow/deny test in the same PR for any new sensitive table. Use whenever adding/changing a table, column, index, or constraint. Trigger words — migration, schema change, DDL, ALTER TABLE, add column, backfill, index, constraint, Prisma migrate.
---
# Safe migration (additive, RLS + test in same PR)

**Use when:** any schema change — new table/column/index/constraint, or altering an existing one.
**Owners:** database-architect (security-engineer co-reviews any sensitive table). On the default profile
migrations live in `supabase/migrations/*.sql` (raw SQL) or Prisma (`prisma/migrations/`) — adapt to the
project's actual stack per `CLAUDE.md`.

## Inputs
The data-model change requested, the table's ownership/tenancy edge if sensitive, current
`docs/specs/data-model.md`, and whether this table holds user/tenant/PII/payment/health data.

## Procedure
1. **Never edit a shipped migration.** If it is applied/merged, add a NEW migration. Confirm nothing
   already in `supabase/migrations/` (or `prisma/migrations/`) touches this object destructively.
2. **Additive-first for zero-downtime** — split any tightening across steps, deployed in order:
   a. **Add** the column as `NULL`able (or add the new table) — never `NOT NULL` with app traffic live.
   b. **Backfill** existing rows in a separate statement/migration (batched if large).
   c. **Tighten**: add `NOT NULL` / `CHECK` / `UNIQUE` / drop the old column only after backfill lands.
3. **New sensitive table → delegate to the `rls-policy` skill** in the SAME PR: `ENABLE`+`FORCE` RLS,
   policies per the permission matrix, and a pgTAP allow/deny test. A sensitive table without RLS fails review.
4. **Index** every foreign key and every hot query predicate/sort. Use `CREATE INDEX CONCURRENTLY` for
   large live tables (raw SQL); on Prisma add `@@index` and review the generated SQL.
5. **Constrain** at the DB: `CHECK` for enums/ranges, `UNIQUE` for natural keys, FK `ON DELETE` intent.
   Money is integer minor units — no floats.
6. **Standard columns**: `id UUID DEFAULT gen_random_uuid()`, `created_at`/`updated_at TIMESTAMPTZ`, and
   an `updated_at` trigger (`before update` bumping `now()`) — Prisma uses `@updatedAt`.
7. **VERIFY** locally: apply the migration on a fresh DB, run the backfill, run the pgTAP/allow-deny +
   unit tests green. Then apply the *down*/rollback path (or a compensating migration) to confirm reversibility.
8. **Update `docs/specs/data-model.md`** (and `rls-policies.md` if the pattern is new) in the same PR.
9. **Verify:** run `scripts/verify.sh` with the migration applied, then **exercise the app against the migrated
   schema** (the flows that read/write the changed object) and confirm the rollback path runs clean. Record with
   `scripts/verify.sh --observe "<expected>" "<observed>"` the flow you drove and the rollback result.

## Guardrails
- ❌ Editing a merged migration; ❌ `NOT NULL`/`UNIQUE` added in one shot on a live populated table.
- ❌ New sensitive table without RLS + allow/deny test in the same PR — block it.
- ❌ FK or hot-path column without an index; ❌ floats for currency; ❌ destructive drop without a backfill/rollback plan.
- No privileged/`service_role` connection used to work around a missing policy — fix the policy.
- A migration touching user/tenant/PII/payment/health data lands in `vantry.yml` `sensitive_paths`: the PR
  cannot merge without a committed `.vantry/reviews/<branch-slug>.security.json` with `verdict: pass`.

## The vendored Postgres reference, and where it is wrong
**`vendor/skills/supabase-postgres/`** carries good material on indexes and locking — and two examples that
contradict this playbook directly: `ADD CONSTRAINT … UNIQUE/CHECK/FOREIGN KEY` in a single statement, and 27
bare `CREATE INDEX` statements with no `CONCURRENTLY`.

`vendor/skills/supabase-postgres/CONFLICTS.md` records both with the safe two-step forms. **Read that file
before following any DDL example in the vendored corpus.** This playbook wins.

## Done when
Migration is new (not an edit), backfill verified, indexes + constraints + `updated_at` trigger present, any
sensitive table has RLS + a **named** passing allow/deny test, `docs/specs/data-model.md` is updated, and a
**fresh passing receipt** for this branch whose observation names the app flow you drove against the migrated
schema and states the **rollback applied cleanly**; `scripts/verify.sh` passes and CI re-runs the same contract.

## Stack notes — PostgreSQL / Supabase + Prisma (illustration, not contract)
If `vantry.yml` `stack:` names something else, this section is void and the Procedure above still applies.

- `ALTER TABLE … ADD COLUMN … NULL` is safe on modern Postgres; adding a NOT NULL column with no default
  rewrites the table and locks it.
- `CREATE INDEX CONCURRENTLY` outside a transaction; a plain `CREATE INDEX` blocks writes for its duration.
- Row-level security: `ENABLE` **and** `FORCE`, in the same migration as the table, with its pgTAP allow and
  deny test in the same PR.
- Prisma: `migrate dev` locally, `migrate deploy` in CI. Never edit a migration in `prisma/migrations/` that
  has been applied anywhere — add a new one.
- Money as `bigint` minor units, never `float` or `numeric` used casually.

On a store with no row-level security (MySQL, Mongo, DynamoDB, SQLite), the contract above is unchanged: the
authorization predicate moves to the repository layer or the policy engine, and it still ships with an
EXECUTED allow test and an EXECUTED deny test in the same change.
