---
name: db-migration-safety
description: Reviews and writes database migrations for safety — lock contention, blocking DDL on large tables, data-loss/destructive operations, missing indexes, and rollback plans. Use before running any schema change against a real or production database.
when_to_use: เขียน/รัน migration; เปลี่ยน schema; เพิ่ม/ลบ column/index/constraint บนตารางจริง
---

## When to Use

Trigger this skill before writing or running ANY of these against a real/production DB:

- New migration file, or editing an existing one
- `ALTER TABLE`, `CREATE INDEX`, `DROP`, `ADD CONSTRAINT`, type changes, `SET NOT NULL`
- Backfilling / updating data across a large table (≥ ~100k rows, or unknown size)
- Renaming a column/table, or changing a column's type
- Any change reviewed by another engineer touching schema

Skip only for: brand-new empty tables, dev-only throwaway DBs, or pure read/query work with no DDL.

## Steps

1. **Classify every statement** as `additive` (safe), `lock-risky`, or `destructive`:
   - additive: `ADD COLUMN` (nullable, no default OR constant default on PG11+), `CREATE INDEX CONCURRENTLY`, new table, add nullable FK without validation
   - lock-risky: `CREATE INDEX` (non-concurrent), `ADD COLUMN ... NOT NULL` with volatile default, `ALTER COLUMN TYPE`, `ADD CONSTRAINT` (validating), `SET NOT NULL` on existing column
   - destructive: `DROP TABLE/COLUMN`, `TRUNCATE`, type narrowing (e.g. `bigint`→`int`, `text`→`varchar(n)`), `DROP CONSTRAINT` relied on by app
   Print this classification before doing anything else.

2. **Get the row count** before judging lock risk: `SELECT reltuples::bigint FROM pg_class WHERE relname = '<table>';` (fast estimate). Treat "unknown" as large. Lock duration scales with rows.

3. **Kill blocking index builds** — replace `CREATE INDEX` with `CREATE INDEX CONCURRENTLY` (Postgres) / `ALGORITHM=INPLACE, LOCK=NONE` (MySQL 8). CONCURRENTLY cannot run inside a transaction block, so it must be its own migration file with transaction wrapping disabled (e.g. `disable_ddl_transaction!` / no `BEGIN`).

4. **Batch every backfill** — never one `UPDATE` over the whole table (holds row locks + bloats WAL). Loop in chunks (1k–10k rows) keyed on PK, commit per batch, optional sleep between. Run the backfill as a SEPARATE step from the DDL that depends on it.

5. **Apply expand–contract for rename / type change** (3 deploys, never rename in place):
   - Expand: add the new column/type. Deploy app that writes BOTH old + new.
   - Migrate: backfill new column in batches; switch reads to new column.
   - Contract: drop the old column in a LATER migration, after the new code is fully deployed and stable.

6. **Make NOT NULL safe** — don't `SET NOT NULL` directly on a big table (full scan under lock). Instead: `ADD CONSTRAINT ... CHECK (col IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT` (lighter lock), then optionally promote.

7. **Write the rollback** — every migration needs a working `down` / inverse. If the op is irreversible (dropped column = lost data), say so explicitly and require an explicit confirmation + backup before running.

8. **Dry-run on a copy** — run the migration against a clone/staging snapshot of prod data (real volume), time it, and check it completes without long locks. Report measured duration.

## Common Errors / Gotchas

- **`CREATE INDEX CONCURRENTLY` inside a transaction** → fails or silently degrades to a normal locking build. Each CONCURRENTLY index needs its own non-transactional migration. A failed CONCURRENTLY build leaves an `INVALID` index — drop it before retrying.
- **`ADD COLUMN ... DEFAULT <volatile>` rewrites the whole table** under an `ACCESS EXCLUSIVE` lock. Constant defaults are metadata-only on PG11+/MySQL8 and are safe; `now()`, `gen_random_uuid()`, sequences are NOT.
- **`ALTER TABLE` takes `ACCESS EXCLUSIVE`** which queues behind AND blocks all reads/writes — even a fast `ALTER` blocks the table while waiting for a slow query to finish (lock queue pile-up). Set a short `lock_timeout` (e.g. `SET lock_timeout = '3s'`) and retry, so the migration fails fast instead of freezing the table.
- **Adding a foreign key validates the whole referencing table** under lock. Use `ADD CONSTRAINT ... NOT VALID` then `VALIDATE CONSTRAINT` in a second step.
- **Type narrowing = silent data loss / errors** (`bigint`→`int` overflows, `varchar(n)` truncates, `timestamp`→`date` drops time). Block these unless data is proven to fit and a backup exists.
- **Dropping a column the running app still references** → errors until the new deploy lands. Drop only AFTER the code that stopped using it is fully deployed (contract phase).
- **Renaming a column in one shot** breaks the currently-running app version during deploy. Always expand–contract.
- **Long single-statement backfill** holds locks + inflates replication lag; replicas fall behind and reads time out.

## Verify

A migration is safe to run only when ALL hold:

- [ ] Every statement classified; no `destructive` op runs without explicit confirmation + a backup taken
- [ ] No non-concurrent index build on a non-trivial table; CONCURRENTLY indexes are in their own non-transactional file
- [ ] All backfills are batched with per-batch commits, separate from dependent DDL
- [ ] Rename/type-change uses expand–contract across separate deploys
- [ ] A working `down`/rollback exists, or irreversibility is flagged and confirmed
- [ ] `lock_timeout` set so the migration fails fast instead of hanging the table
- [ ] Dry-run on prod-sized copy completed; measured duration and lock impact reported

If you cannot verify lock duration on real data volume, do NOT run against production — escalate for a maintenance window or a tested staging run first.
