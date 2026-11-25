---
name: database-migrations
description: "Sequences a relational schema change so it deploys without downtime: expand/contract, lock-safe DDL, reversibility, deploy order. Use when writing or reviewing a migration or splitting a schema change across releases. Not for RDS instance changes in Terraform (use terraform-aws:terraform-review)."
license: MIT
---

# Database Migrations

Engine-agnostic. The examples use SQL that most relational engines accept; the
concurrency and locking notes are flagged where they are engine-specific, because the
difference between "this locks the table" and "this does not" is the whole subject.

Without a checkout (web), work from the migration file or DDL the user pastes.

## The one rule

**Every schema state must work with both the code before it and the code after it.**

Everything else on this page follows from that sentence. It is true because a deploy is not
atomic: for some window — seconds if you are lucky, minutes if a rollout is gradual, longer
if something goes wrong midway — *both* the old code and the new code are running against
*one* database. Any schema state that only one of them can tolerate produces errors for
real users during that window.

So every schema change is split across deploys, and each individual deploy is compatible
with the code on both sides of it. When the pipeline reliably runs migrations before the
application (see Deploy ordering), an additive expand can ship with the code that uses it;
without that guarantee, keep them in separate deploys.

## Expand / migrate / contract

| Phase | Deploy | What ships | Why it is safe |
| --- | --- | --- | --- |
| **Expand** | N | Additive DDL only: new nullable columns, new tables, new indexes. No code change required. | Old code does not know the new column exists and is unaffected. |
| **Migrate** | N+1 | Code that writes and reads the new shape. Backfill existing rows. | The schema has existed since the previous deploy, so the code cannot outrun it. |
| **Contract** | N+2 | Remove what is now unused: drop old columns, add `NOT NULL`, delete compatibility branches. | No deployed code references the removed thing. |

Contract is a separate release, not the tail of the migrate release. Between N+1 and N+2
you need enough time to be confident the new code is staying — at least one full release
cycle, and longer if your rollback window is longer. **If you might roll back to the
previous version, you cannot have contracted yet**, because that version still reads the
old column.

The cost of this is that a single logical change takes three releases. That is the price of
being able to deploy at any hour without a maintenance window, and it is a good trade.

## Patterns

| Change | How to do it safely |
| --- | --- |
| **Add a column** | N: `ADD COLUMN c TEXT NULL` (with a `DEFAULT` if the app needs one). N+1: code writes and reads it. N+2 (optional): `SET NOT NULL`. |
| **Drop a column** | N: remove every code reference and deploy. N+1: `DROP COLUMN`. Never the other order. |
| **Rename a column** | Never rename in place. N: add the new column. N+1: dual-write both, backfill, read the new one. N+2: drop the old one. |
| **Change a column's type** | Same as a rename — a new column of the new type, dual-write, backfill, drop. In-place type changes rewrite the table under a lock. |
| **Add `NOT NULL`** | N: add nullable, backfill in batches. N+1: code always writes a value. N+2: add the constraint. On PostgreSQL, `SET NOT NULL` scans the table under an `ACCESS EXCLUSIVE` lock; from version 12, first add `CHECK (c IS NOT NULL) NOT VALID`, then `VALIDATE CONSTRAINT` (weaker lock), then `SET NOT NULL` (skips the scan because the check proves it), then drop the check. |
| **Add an index** | Use the engine's non-blocking form (`CREATE INDEX CONCURRENTLY` on PostgreSQL; `ALGORITHM=INPLACE, LOCK=NONE` on MySQL/InnoDB). Safe in a single deploy. The concurrent form cannot run inside a transaction, which some migration tools wrap by default. A failed concurrent build leaves an `INVALID` index behind; drop it before retrying. |
| **Add a foreign key** | Add it unvalidated (`NOT VALID` on PostgreSQL), then validate as a separate step during low traffic. Validating takes a weaker lock than adding-and-validating in one statement. |
| **Backfill a large table** | Batched, with a bound and a sleep, outside the schema migration. A single `UPDATE` over millions of rows holds one transaction open for the duration and blocks vacuum/cleanup behind it. |

## Prohibited

| Pattern | What goes wrong |
| --- | --- |
| `ADD COLUMN ... NOT NULL` with no default, in the same deploy as the code that populates it | Old code inserts without the column and the insert fails; and if the migration has not run yet, new code fails on a missing column. Broken in both directions. |
| `DROP COLUMN` while any deployed code still selects it | Immediate errors on in-flight requests. Rollback does not fix it — the data is gone. |
| `RENAME COLUMN` | Not backward compatible with anything. There is no window in which both versions work. |
| Destructive DDL in the same change as the code that depends on it | Couples two things that deploy at different times; any ordering hiccup is an outage. |
| A blocking `CREATE INDEX` on a production table | On PostgreSQL it takes a `SHARE` lock: reads continue, every write blocks for the whole build — which on a large table is not seconds. |
| Unbounded `lock_timeout` (or a long one) on a migration touching a hot table | The migration queues behind a long-running query, then everything queues behind the migration, then the connection pool is exhausted. Fail fast instead: set a short timeout and retry. |
| Gating the migration job on "did migration files change?" | Migration tools are designed to be idempotent and to reconcile state. Skipping the run when files are unchanged breaks tools that need to run to discover there is nothing to do. |

## Migration file conventions

- **Idempotent.** `IF NOT EXISTS` / `IF EXISTS`, or the framework's own guard. A migration
  that is re-run — after a partial failure, on a restored replica, by a retrying job —
  must not error. Exception: `CREATE INDEX CONCURRENTLY IF NOT EXISTS` sees the `INVALID`
  index a failed build left and skips, so the re-run "succeeds" with an unusable index.
  Guard that case with `DROP INDEX CONCURRENTLY IF EXISTS` first, or check `pg_index.indisvalid`.
- **One concern per file.** Do not mix DDL and a bulk data change. DDL takes locks; bulk
  DML holds a long transaction. Together they hold locks for the length of the data change.
- **A short `lock_timeout` at the top** of any migration touching a large table.
- **Reviewable.** A migration is a production change. It gets the same review as code, and
  the review reads it as "what locks does this take, and for how long".
- **A down migration, or an explicit statement that there is none.** See below.

## Reversibility

A migration is reversible when running its down step restores the **state**, not just the
**schema**. That distinction is where teams get caught.

| Change | Reversible? | Why |
| --- | --- | --- |
| Add a nullable column | Yes, trivially | Dropping it loses only data that only the new code wrote |
| Add a table | Yes | Same |
| Add an index | Yes | Dropping it costs performance, not data |
| Add a constraint | Yes | Dropping it widens what is accepted |
| **Drop a column** | **No** | The down migration can recreate the column. It cannot recreate the values. |
| **Drop a table** | **No** | Same, larger |
| **Change a type with a lossy cast** | **No** | Truncated precision does not come back |
| **A backfill that overwrites** | **No**, unless you saved the old values | The down migration has nothing to restore from |

So: **the expand and migrate phases are reversible, and the contract phase is not.** That
is not an accident of the pattern, it is the reason the pattern is ordered that way — it
concentrates all the irreversibility into the one deploy that ships last, after the new
behaviour has already proven itself in production.

Write the down migration for the reversible ones. For the irreversible ones, say so in the
file, in a comment, at the top — "no down migration: this drops `<column>`; recovery is
restore-from-backup" — so that the person reading it at 3am is not searching for one.

## When a migration cannot be rolled back

At some point a contract-phase migration will land and something will break. The rollback
button does not help: reverting the application does not put the column back, and the
previous version is the one that needs it.

What is actually available:

1. **Forward-fix.** Write and ship a new migration that restores the shape the running code
   needs. This is usually the fastest correct path, and it is the reason your pipeline's
   time-to-deploy matters as an incident metric rather than a productivity one. Practise it
   when nothing is on fire.
2. **Restore from backup** — correct, and expensive. It costs whatever writes happened
   since the snapshot, so it is a last resort for data loss, not a routine rollback.
3. **Shim in the application.** Ship a version that tolerates the new schema, buying time
   for a considered fix rather than a panicked one.

The preparation that makes all three cheaper:

- **Snapshot before any production migration**, automatically, as a pipeline step rather
  than a checklist item. The snapshot you did not take is only ever discovered at the worst
  moment.
- **Keep contract migrations small and alone.** One `DROP COLUMN` per release, in its own
  change, so that when it is wrong the blast radius is one column.
- **Know your restore time before you need it.** "We have backups" is not a recovery plan
  if nobody has measured how long a restore takes.

## Deploy ordering

When schema and code ship in the same pipeline, the order is:

```
deploy the migration runner → run migrations → deploy the application → shift traffic → verify
```

- **Migration runner first**, so it is executing the migration files from the commit being
  deployed rather than the previous one.
- **Migrations run unconditionally**, not gated on a file-change filter.
- **Application after migrations**, so the schema is never behind the code. Expand/contract
  already guarantees safety if this ordering slips; this is defence in depth, not the
  primary control.
- **Traffic shift last, and atomic**, where the platform allows it — a version alias, a
  weighted rollout, a swap. Deploying the new version behind a held-back alias and then
  cutting over gives you an instant reversal of *code* while the database stays valid for
  both versions, which is exactly the property expand/contract was built to provide.

## Review checklist

Every change containing migration files:

- [ ] Every new column is nullable or has a default
- [ ] No column is dropped that currently-deployed code still references
- [ ] No in-place renames or lossy type changes
- [ ] The schema after this deploy works with the **previous** release's code
- [ ] If this is a contract change, the matching expand shipped at least one release ago
- [ ] Index creation uses the engine's non-blocking form
- [ ] Foreign keys are added unvalidated, then validated separately
- [ ] `lock_timeout` is set on anything touching a large table
- [ ] A down migration exists, or the file states why it cannot
- [ ] A backup or snapshot is taken by the pipeline before the production run

## Verify

Before approving, show evidence rather than assertion:

- Run the migration against a copy of production-sized data (or a restored snapshot) and
  record how long each statement held its lock.
- On PostgreSQL, confirm no index is left invalid:
  `SELECT indexrelid::regclass FROM pg_index WHERE NOT indisvalid;` returns no rows.
- Run the previous release's test suite against the migrated schema. If it fails, the
  change is not expand-compatible.

If none of that is possible (no database access, pasted DDL only), say which checklist items
you could not confirm instead of marking them done.
