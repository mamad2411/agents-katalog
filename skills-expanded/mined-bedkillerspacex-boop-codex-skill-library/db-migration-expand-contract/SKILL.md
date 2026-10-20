---
name: db-migration-expand-contract
description: >
  Apply expand/contract (parallel change) schema migrations for owned services:
  dual-write/dual-read phases, backfill, feature flags, and safe removal of old
  columns. Use for zero/near-zero downtime renames, splits, and type changes
  under rolling deploys — companion to database-migration-safety.
---

# DB Migration Expand/Contract

## Scope And Authorization

- **In scope:** Schema evolution on databases you operate with multi-instance app deploys.
- **Out of scope:** Irreversible prod data experiments without rollback/forward plans.
- Prefer feature flags and metrics per phase.
- Pair with `database-migration-safety` for DDL lock practice and `code-quality-standards`.

## When To Use

- Renaming columns/tables without downtime.
- Splitting columns, changing types, or moving data between tables.
- Rolling deploys where old and new app versions coexist.
- Avoiding lock-heavy one-shot rewrites.

## Do Not Use As Primary

| Need | Skill instead |
| --- | --- |
| General migration safety / locks | `database-migration-safety` |
| Failover | `db-failover-checklist` |
| Retention purges | `data-retention-job-design` |
| API versioning only | API design skills |
| Implementation quality baseline | `code-quality-standards` |

## Pattern overview

```text
EXPAND → MIGRATE/BACKFILL → CONTRACT
(with app deploy steps interleaved)
```

| Phase | Schema | App |
| --- | --- | --- |
| 0 Start | Old shape | Old code |
| 1 Expand | Add new structures (nullable/new table) | Still old |
| 2 Dual write | New+old | Code writes both |
| 3 Backfill | Fill new from old | Dual write continues |
| 4 Dual read / switch | Prefer new | Feature flag to read new |
| 5 Contract | Drop old | Code only new |

## Workflow

### 1. Design the target model

1. Example: rename `users.name` → `users.display_name`.
2. Map every reader/writer in code and jobs.
3. Success: no dual-write forever; contract completed; data parity proven.

### 2. Expand

```sql
ALTER TABLE users ADD COLUMN display_name text;  -- nullable first
-- optional: CHECK/constraints deferred
```

Deploy migration **before** code that requires the column to be non-null.

### 3. Dual-write deploy

```python
def save_user(u: User) -> None:
    u.display_name = u.display_name or u.name
    # persist both columns during transition
    repo.upsert(name=u.name, display_name=u.display_name)
```

1. Ship dual-write while still reading old if needed.
2. Keep dual-write **idempotent**.

### 4. Backfill

```sql
-- Batched
UPDATE users
SET display_name = name
WHERE display_name IS NULL
  AND id > $last
ORDER BY id
LIMIT 1000;
```

1. Throttle; monitor replication lag.
2. Verify counts: `WHERE display_name IS NULL` → 0 (except intentional).
3. For large tables, run as job not blocking migration txn.

### 5. Switch reads

```python
def get_display(u: User) -> str:
    if feature_enabled("read_display_name"):
        return u.display_name or u.name
    return u.name
```

1. Canary flag; compare metrics/errors.
2. Fix straggling writers (jobs, admin scripts).

### 6. Enforce and contract

```sql
-- After all writers populate new column
ALTER TABLE users ALTER COLUMN display_name SET NOT NULL;
-- Bake time...
-- Contract only when no code references name
ALTER TABLE users DROP COLUMN name;
```

Contract **only** after:

1. Code search clean (`rg '\.name'` carefully).
2. Old app versions no longer running.
3. Bake period without dual-write issues.

### 7. Type change variant

```text
Add new_col (new type) → dual-write convert → backfill convert →
read new_col → drop old_col → optional rename new_col
```

Avoid in-place type change on huge tables when rewrite locks exceed budget.

## Verification matrix

| Check | Phase |
| --- | --- |
| Old app works with expanded schema | After expand |
| Dual-write parity sample | During dual-write |
| Null backlog ~0 | After backfill |
| Read flag 100% | Before NOT NULL |
| No references to old column | Before drop |

```bash
rg -n 'display_name|\.name' --glob '!migrations/**'  # careful review
```

## Good / Bad

| Topic | Good | Bad |
| --- | --- | --- |
| Rename | Expand + dual + drop | `RENAME COLUMN` mid traffic without plan |
| Dual-write | Temporary with ticket | Permanent dual forever |
| Backfill | Batched + observed | One huge UPDATE |
| Contract | After version drain | Drop while canaries on old code |
| Flags | Controlled read switch | Big bang read cutover unmonitored |

## Output Checklist

- [ ] Target schema and all consumers listed
- [ ] Expand migration shipped
- [ ] Dual-write deployed
- [ ] Backfill complete with evidence
- [ ] Read switch canaried
- [ ] Constraints tightened
- [ ] Code references removed
- [ ] Contract migration shipped after bake
- [ ] Dual-write removed
- [ ] Residual jobs/scripts audited

## Rules

- Expand/contract trades speed of schema purity for deploy safety — finish the contract phase.
- Do not drop under dual-version uncertainty.
- Focus on **expand/contract migration sequencing**.
