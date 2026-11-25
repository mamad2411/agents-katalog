---
name: drizzle-migrations
description: How to safely add, edit, and verify Drizzle migrations in the skills-observability backend (PostgreSQL + Drizzle ORM). Covers the schema-first generation flow, the strict monotonicity invariant of `_journal.json` `when` timestamps (whose violation has silently skipped migrations in production), idempotent SQL patterns, and how to verify on a fresh DB before merging. Use this skill whenever the user edits `backend/src/db/schema.ts`, runs `bun run migrate:generate` or `bun run migrate:run`, hand-edits anything under `backend/src/db/migrations/` (including `meta/_journal.json`), asks about adding or altering a database column / table / index / constraint, debugs a migration that "didn't apply" or "ran in dev but not prod", or resolves a merge conflict in the migration journal. Trigger this even if the user only mentions a small schema tweak — the journal pitfall is the kind of bug where everything looks fine until production silently diverges, and the right time to apply this guidance is before the schema edit, not after.
---

# Drizzle Migrations — skills-observability backend

This skill exists because we lost meaningful production time to a class of migration bug that produces no error, no warning, and no test failure — until prod and dev silently disagree about what tables exist. The rules below are designed to keep that from happening again. Where a rule looks heavy-handed, the **Why** explains the real failure it prevents, so you can apply judgment at the edges.

## The Golden Path (schema-first)

When a database change is needed, follow this exact sequence. Do not deviate without reading the rest of this document first.

```
1. Edit backend/src/db/schema.ts        (the source of truth)
2. cd backend && bun run migrate:generate   (Drizzle writes the SQL + journal entry)
3. Open the generated *.sql and review it    (catch destructive ops, missing IF NOT EXISTS)
4. Optionally tighten the SQL for idempotency (see "SQL idempotency" below)
5. Commit BOTH the .sql file AND the updated meta/_journal.json + meta/*.json snapshot
6. Verify against a fresh DB before merging  (see "Verification" below)
```

If you find yourself hand-writing a `.sql` file under `backend/src/db/migrations/` from scratch, stop and ask whether the change can be expressed in `schema.ts` instead. Hand-authored migrations are valid in special cases (data backfills, raw SQL Drizzle can't generate), but they are off the golden path and need extra care — see "Hand-authored migrations" below.

## The invariant that bit us: journal monotonicity

The `meta/_journal.json` file is a list of entries with an `idx`, a `tag`, and a `when` (a Unix-epoch milliseconds timestamp). At runtime, `drizzle-orm/postgres-js/migrator` decides whether to apply a given migration like this:

> Walk the journal entries in `idx` order. For each entry, apply it only if its `when` is **strictly greater** than the **maximum `created_at`** currently recorded in the `__drizzle_migrations` table. Otherwise, skip it.

Read that sentence twice. The consequence is non-obvious and catastrophic: **if you add a new entry whose `when` is `<=` any already-applied entry's `when`, that entry will be silently skipped forever.** No error. No warning. No log line. The migration just doesn't run, and the production DB diverges from the schema your code expects.

This actually happened to us. Three migrations carried May-2025 `when` values in a journal whose head was already in March 2026. They never ran in production. The schema looked fine in dev (where the DB had been re-created) and the test suite passed (against a fresh DB), but every prod request that touched those tables 500'd. We only noticed via on-call.

**The invariant**: in `_journal.json`, `entries[i].when > entries[j].when` for every `i > j`. Strictly greater, no equality, no going backward.

### Practical rules that keep the invariant true

1. **Never hand-edit `meta/_journal.json` to "fix dates" or resolve a merge conflict.** Re-run `bun run migrate:generate` or carefully merge by re-issuing the entries with new `when` values that are strictly greater than the current max. The journal is an append-only log in disguise.

2. **When `migrate:generate` produces an entry, leave its `when` alone.** Drizzle stamps it with `Date.now()` at generation time, which is by construction greater than every previous entry (assuming the clock isn't broken).

3. **When two branches each add a migration and you merge, the resulting journal must still be monotonic.** Two branches can each generate `0007_*` legitimately. Resolve by:
   - Pick a winning idx ordering (typically: keep both, the later-merged one becomes `idx N+1`, rename its file).
   - Re-stamp the later entry's `when` to `Date.now()` so it is strictly greater than the prior max.
   - If you can't be sure, re-run `migrate:generate` on a clean tree and let Drizzle re-emit the entry.

4. **If you ever truly must hand-author a journal entry**, set `when: Date.now()` *at the moment you author it*, and verify it is strictly greater than `Math.max(...entries.map(e => e.when))` in the existing journal. Don't copy `when` values from other entries, don't pick "round" timestamps, don't reuse a value because "it looks similar."

5. **Audit the journal whenever you touch it.** A quick check in `node`:
   ```js
   const j = require("./backend/src/db/migrations/meta/_journal.json");
   j.entries.reduce((p, e) => { if (e.when <= p) throw new Error(`non-monotonic at ${e.tag}`); return e.when; }, 0);
   ```
   If this throws, the journal is broken and you have a latent silent-skip bug.

### Why this design exists (briefly)

Drizzle uses `when` as a totally-ordered cursor instead of relying on `idx` because the cursor must survive parallel branches and out-of-order merges in the source repo. The bug is not in Drizzle — it's that the contract is unintuitive and the failure is silent. Your job is to keep the contract.

## SQL idempotency

A migration may run on a DB that's already partially applied (a previous run was interrupted, a rollback got partially rolled back, etc.). Make the SQL safe to re-run:

| Operation       | Use this                                          | Not this                  |
| --------------- | ------------------------------------------------- | ------------------------- |
| Create a table  | `CREATE TABLE IF NOT EXISTS ...`                  | `CREATE TABLE ...`        |
| Add a column    | `ALTER TABLE x ADD COLUMN IF NOT EXISTS y ...`    | `ALTER TABLE x ADD COLUMN y ...` |
| Drop a column   | `ALTER TABLE x DROP COLUMN IF EXISTS y`           | `ALTER TABLE x DROP COLUMN y` |
| Create an index | `CREATE INDEX IF NOT EXISTS ix ON ...`            | `CREATE INDEX ix ON ...`  |
| Insert seed data| `INSERT ... ON CONFLICT DO NOTHING`               | plain `INSERT`            |

Drizzle's generator does not always emit the `IF NOT EXISTS` form. Tighten the SQL by hand after generation when it's an obvious win — this costs you ten seconds and prevents a 3am incident if a migration retry is needed.

**Why this matters**: idempotent SQL turns "the migration half-applied and now everything is broken" into "re-run the migrate command, it picks up where it left off." On the golden path it never matters; in degraded states it's the difference between a five-minute fix and a restore from backup.

## Hand-authored migrations

Sometimes `migrate:generate` can't express what you need (data backfill, custom function, raw DDL Drizzle doesn't model). In that case:

1. **Generate a placeholder first** with `bun run migrate:generate` even if the schema diff is empty — this gives you a correctly-stamped journal entry and the right filename pattern.
2. **Replace the SQL contents** with your hand-written DDL/DML. Keep it idempotent.
3. **Do not edit the journal `when` value.** Leave the timestamp Drizzle stamped.
4. **Document why** at the top of the SQL file in a one-line comment so the next reader doesn't think it was a botched generation.

For pure data backfills that don't change schema, prefer a one-shot script invoked manually rather than a migration — backfills in the migration system are hard to retry, slow on large tables, and tangle data movement with schema evolution.

## Verification before merge

Before pushing a migration-bearing PR, verify the migrations apply cleanly **against a fresh DB**, not just your existing dev DB. Your dev DB has accumulated state across many branches; it can mask both ordering bugs and missing migrations.

```bash
# from repo root
docker compose -f docker-compose.dev.yml down -v   # destroys the volume
docker compose -f docker-compose.dev.yml up -d     # fresh PG
cd backend && bun run migrate:run                   # apply from scratch
```

After this runs cleanly, also confirm:

- The schema in the fresh DB matches `schema.ts`. A quick `\dt` and `\d <table>` in `psql` against the new tables is enough.
- The number of rows in `__drizzle_migrations` equals the number of journal entries. If it's lower, a migration was silently skipped — start by auditing the journal monotonicity.

**Why this matters**: the migration runner is the only thing standing between your schema and prod. The fresh-DB run is the only test that exercises it the way prod will exercise it on next deploy (assuming prod isn't fresh — but prod will, on every new env, every disaster-recovery rebuild, every test environment provisioned by CI).

## Reviewing a migration PR

When reviewing someone else's migration changes, check in this order:

1. **`meta/_journal.json` is monotonic.** Walk the `when` values; flag any non-strict-increase.
2. **Each new `.sql` file is idempotent** where the operation supports it.
3. **The SQL matches the schema diff.** If `schema.ts` adds a column `notNull` with a default, the SQL should reflect that — Drizzle is usually right, but it's the easiest place for a subtle mistake to slip in (e.g., forgetting that adding NOT NULL to a populated table requires a default or a backfill step).
4. **For destructive changes** (drop column, drop table, type narrowing) — confirm the data isn't needed, and whether a two-phase rollout (deploy code that ignores the column, then drop it later) is safer.
5. **No edits to existing migration `.sql` files** unless the migration is brand-new and unmerged. Editing a migration that has already run in any environment will not re-apply the change — the runner will see the entry as already applied. If you need to change something already shipped, write a new migration.

## Common mistakes and what they look like

- *"My migration ran in dev but the table doesn't exist in prod."* → Almost always journal monotonicity. Audit `_journal.json`.
- *"I edited the SQL in `0005_*.sql` and re-deployed but the change didn't take."* → Already-applied migrations are not re-run. Add a new migration.
- *"I got a merge conflict in `_journal.json` and resolved it by hand."* → High risk of breaking monotonicity. Re-audit, or re-generate.
- *"`migrate:generate` produced a weird empty migration."* → Often means your schema.ts change didn't actually change anything Drizzle can see (e.g., a comment-only edit, or a TS type without a runtime difference). Delete the empty migration before committing.
- *"The migration runs but takes forever on prod."* → You're probably backfilling or adding a non-concurrent index on a large table. For large tables, prefer `CREATE INDEX CONCURRENTLY` (which Drizzle won't generate — hand-author) and split data backfills out of the migration system.

## Emergency: a migration was silently skipped in production

If you discover a journal entry was skipped (rows missing from `__drizzle_migrations`, or schema doesn't match), the fix is:

1. **Don't try to "re-stamp" the old `when` value** — that just hides the problem and doesn't trigger a re-run because the runner only looks forward.
2. **Generate a new migration** that does what the skipped one was supposed to do. Make it idempotent so it's safe even on environments where the original *did* run.
3. **Audit every other environment** (staging, dev databases, ephemeral CI envs) to figure out where the divergence exists.
4. **Then fix the journal** so future fresh-DB runs don't repeat the skip — strictly monotonic `when` values, no exceptions.

The reason to fix forward (new migration) rather than backward (edit old `when`) is that production schemas are built by running migrations in order; the only way to change one is to add another. Editing history doesn't propagate.
