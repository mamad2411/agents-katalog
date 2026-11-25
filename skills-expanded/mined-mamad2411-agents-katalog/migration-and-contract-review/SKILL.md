---
name: migration-and-contract-review
category: quality
description: Use when a diff or design adds or changes a DB migration, an endpoint or DTO, an event payload, or a shared type with consumers
source: sbdchd/squawk docs (Apache-2.0), ankane/strong_migrations (MIT), Google AIP-180 (CC BY 4.0), adapted
---
# Migration & Contract Review

## Why It Matters Here

A production rollback reverts the merge commit — it does **not** undo the schema. The old code has to keep running against the new schema until a human decides otherwise, and the system already flags a schema-touching task for a mandatory stage deploy. A migration or contract reviewed only for "does it run" and not "does the PREVIOUS release's code still work against it" is an outage waiting for the next rollback.

Pair with migration-safety (backend-developer, same rules from the authoring side) and spec-authoring's Security & data / Decision record sections for the design-time version of this.

## Blocking Checks (Important or Critical)

**Editing an applied migration.** A migration already run on any environment is immutable; a fix is a new migration.
- ❌ editing `0042_add_status.sql` after it merged.
- ✅ `0051_fix_status_default.sql` that corrects it.

**A stub or empty down/rollback migration.** If it can't really be undone, say so and give the operational alternative instead of a down migration that lies.

**Drop, rename or retype of a column or table still read by deployed code.**
- ❌ `ALTER TABLE tasks DROP COLUMN legacy_status;` in the same task that stops writing it.
- ✅ stop writing it (task N), deploy, confirm no reads remain (`grep_code`/consumer check), THEN drop it (task N+1, `deploy_depends_on: ["N"]`).

**`ADD COLUMN … NOT NULL` with no default**, or a **volatile default** (rewrites the whole table).
- ❌ `ALTER TABLE tasks ADD COLUMN priority int NOT NULL;`
- ✅ `ALTER TABLE tasks ADD COLUMN priority int NOT NULL DEFAULT 0;` — a constant default on PG11+ does not rewrite the table.

**`CREATE INDEX` without `CONCURRENTLY`** on a table already carrying rows, or `CONCURRENTLY` used inside a transaction / a multi-statement file the repo's migration runner wraps in one (check how the runner executes a file before assuming `CONCURRENTLY` is safe there).
- ❌ `CREATE INDEX idx_tasks_status ON tasks(status);` on a live table — takes a write lock for the build.
- ✅ `CREATE INDEX CONCURRENTLY idx_tasks_status ON tasks(status);`, run outside a transaction.

**A FK or CHECK added without `NOT VALID` + a later `VALIDATE`.**
- ❌ `ALTER TABLE tasks ADD CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id);` — locks and scans the whole table.
- ✅ `ADD CONSTRAINT … NOT VALID;` then, in a later step/migration, `VALIDATE CONSTRAINT fk_project;`.

**`SET NOT NULL` on an existing column** with no prior validated `CHECK (col IS NOT NULL)` (PG12+ lets the planner skip the full scan once that check is validated).

**A data backfill inside the schema migration**, unbatched. Backfill in application code or a batched script, not a single blocking UPDATE in the DDL migration.

**A new query path added with no supporting index** — works in dev on a handful of rows, locks up in production.

## Contract Checks

- **Additive is safe:** a new optional response field, a new endpoint, a new optional request field with a default.
- **Breaking needs every consumer updated and ordered:** a renamed/removed field, a changed type or status code, a new REQUIRED request field, a changed default page size, a changed enum's meaning.
  - AIP-180: *"Old clients must be able to work against newer servers"* — source, wire and semantic compatibility all have to hold, not just "it compiles."
- **Mobile clients cannot be force-updated.** Anything an already-installed app reads stays readable until a later, separate contract task ships and enough time has passed — never break it in the same task that adds the new shape.
- **Find consumers** with `list_links(component, direction:"in")`, then `grep_code` in the cloned consumer repo (technical-analysis-workflow's cross-repo clone procedure) for the exact field/endpoint.
- **Error shape and status codes are part of the contract** — changing a 404 to a 200-with-null, or a flat error body to a nested one, breaks a consumer's error handling exactly like a renamed field.

## Design-Side Application (spec-authoring)

Any schema or contract change in the design gets: the expand step and the contract (breaking) step as SEPARATE tasks in the `split`, a `before_deploy` entry on the expand task ("migration N applied on stage"), and a `rollback_plan` that states plainly that the schema stays and names what still reads it. The contract-breaking task carries `deploy_depends_on` on every consumer-update task.

## Common Mistakes

- Treating "the migration ran in the task's dev DB" as proof it's safe in production — a live table with real row counts behaves differently under a table rewrite or a non-concurrent index build.
- Reviewing the SQL in isolation from the code that reads the table — a column drop is safe only once nothing reads it, which is a code fact, not a SQL fact.
- Accepting "the mobile team will update eventually" as cover for a breaking contract change shipped now.

## Red Flags

- A single migration file both drops a column and the diff still has a reader for it (`grep_code` the old field name).
- `NOT NULL` added to an existing column with no earlier `CHECK` step.
- A renamed REST field with no corresponding `blocked_by`/`deploy_depends_on` on the consuming repositories' tasks.
- `before_deploy`/`rollback_plan` left empty on a task that `HasMigration`.
