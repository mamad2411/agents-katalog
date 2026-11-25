---
name: mysql-fk-hardening-workflow
description: End-to-end orchestrator for adding a foreign-key constraint to an existing MySQL or MariaDB column on a production table.
category: Database
---

# MySQL Foreign-Key Hardening Workflow Skill

> **Skill ID:** `mysql-fk-hardening-workflow`<br>
> **Version:** 1.0.0<br>
> **Type:** Composer

## Description

End-to-end orchestrator for adding a foreign-key constraint to an existing
MySQL / MariaDB column on a production table. Composes the
[`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md)
probes through a judgement-gated pipeline:

1. **Probe** — engine, orphan rows, sentinel-0 rows, FK readiness.
2. **Decide** — sentinel-NULL migration scope, constraint placement
   (FK only / app guard / DB trigger / both — see §Decision below).
3. **Migrate** — sentinel rows to NULL via the dry-run → authorize →
   commit harness (`scripts/dry-run-update.py` + `scripts/commit-update.py`).
4. **Bracket** — dispatch a DB backup workflow BEFORE and AFTER each
   destructive step via
   [`db-backup-bracketing-protocol`](../db-backup-bracketing-protocol/SKILL.md).
5. **ALTER** — add the FK with `ON DELETE` / `ON UPDATE` chosen per
   §Decision: Referential Action below.
6. **Install app + DB guards** for rules the FK cannot express (e.g.
   self-reference prohibition; see
   [`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md)).
7. **Verify** — re-probe and confirm zero orphans, FK present, app guard fires.

## When to Apply

- A legacy table has a logical FK relationship not yet enforced by the engine.
- A column historically used `0` as a "no-parent" sentinel and needs migration
  to `NULL` before the FK can be added.
- A self-referencing parent column needs both FK enforcement AND a
  non-self-reference rule that CHECK cannot express on AUTO_INCREMENT PKs.

Do NOT apply when:
- The constraint is a simple non-NULL FK on a greenfield table — write the
  FK directly in `CREATE TABLE`.
- The table is not InnoDB — invoke
  [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md)
  `apply-engine.py` first.

## Composition Map

| Step | Delegated to |
|---|---|
| Engine / orphan / null / FK-readiness probes | [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) |
| Sentinel → NULL migration harness | `scripts/dry-run-update.py` + `scripts/commit-update.py` (this skill) |
| Backup bracketing each destructive step | [`db-backup-bracketing-protocol`](../db-backup-bracketing-protocol/SKILL.md) |
| Self-reference rule on AUTO_INCREMENT PK | [`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md) |
| App-layer guard examples | [`php-mysqli-prepared-statement-modernization`](../php-mysqli-prepared-statement-modernization/SKILL.md) §Self-Parent Guard |
| Atomic commit of schema migration scripts | [`git-atomic-commit-construction`](../git-atomic-commit-construction/SKILL.md) |

## Procedure

### Phase 1 — Probe

```bash
SECRETS=/path/to/db.secrets

# Engine
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-server-flavor.py --secrets "$SECRETS"
# Orphans against intended parent
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-orphan-rows.py \
    --secrets "$SECRETS" --check 'child.fk_col->parent.pk_col' --list-orphans
# Sentinel-0 enumeration
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-null-rows.py \
    --secrets "$SECRETS" --check 'child.fk_col'
# FK readiness (orphans + index + engine in one shot)
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-fk-readiness.py \
    --secrets "$SECRETS" --fk 'child.fk_col->parent.pk_col'
```

### Phase 2 — Decision Gates

#### Decision: Sentinel Migration Scope

Present `probe-null-rows.py` output to user. Common scopes:

- **Narrow** — single column only (preferred for risk minimization).
- **Broad** — all sentinel-0 columns at once.

Default to narrow unless user explicitly authorizes broad.

#### Decision: Constraint Placement Matrix (W6 / K1)

| Strategy | Self-parent prevented? | Cross-row FK enforced? | Write perf cost | Read perf cost | Industry norm? |
|---|---|---|---|---|---|
| FK only | No (FK alone permits self-ref) | Yes | ~0 (engine) | 0 | Yes |
| App-layer guard | Yes | No (orphans still possible) | ~1 ns Kotlin / ~50 ns PHP | 0 | **YES — primary** |
| DB trigger | Yes | No | ~5–20 µs per row | 0 | Niche / legacy |
| **Both (FK + app + trigger)** | Yes | Yes | ~5–20 µs + 1–50 ns | 0 | Defense-in-depth |

**Recommendation**: at chart-of-accounts write volumes (~100/day), the
trigger overhead is unmeasurable; prefer **both** for defense-in-depth.
At >10k writes/second, drop the trigger and lean on the app guard.

#### Decision: Referential Action

| Parent action | Recommended `ON DELETE` | Rationale |
|---|---|---|
| Account / Master entity | `RESTRICT` | Prevent silent cascading loss; force explicit child cleanup first. |
| Soft-deletable parent | `RESTRICT` + app cascades soft-delete | Same. |
| Pure metadata join | `SET NULL` | Acceptable when child can stand alone. |
| Owned audit row | `CASCADE` | Child has no meaning without parent. |

Default `ON UPDATE CASCADE` is always safe — PKs rarely change, but
when they do (re-keying), CASCADE prevents orphans.

### Phase 3 — Sentinel → NULL Migration (dry-run gated)

```bash
# Dry run — proves intent, ALWAYS rolls back
python3 .agents/skills/mysql-fk-hardening-workflow/scripts/dry-run-update.py \
    --secrets "$SECRETS" \
    --update "UPDATE child SET fk_col = NULL WHERE fk_col = 0" \
    --verify "SELECT id FROM child WHERE fk_col = 0" \
    --expect-rows 72
# Outputs: ... --- DRY_RUN_SHA: a1b2c3d4e5f60718 ---

# User authorizes -> commit
python3 .agents/skills/mysql-fk-hardening-workflow/scripts/commit-update.py \
    --secrets "$SECRETS" \
    --update "UPDATE child SET fk_col = NULL WHERE fk_col = 0" \
    --verify "SELECT id FROM child WHERE fk_col = 0" \
    --require-dry-run-sha a1b2c3d4e5f60718
```

The `--require-dry-run-sha` drift guard refuses to commit unless the
exact `(update, verify)` pair was dry-run-attested. This blocks the
"I ran the dry-run yesterday, let me commit today" mistake.

### Phase 4 — Backup Bracketing

Before AND after each destructive op (Phase 3 UPDATE, Phase 5 ALTER,
Phase 6 trigger install), invoke
[`db-backup-bracketing-protocol`](../db-backup-bracketing-protocol/SKILL.md).

### Phase 5 — ALTER TABLE ADD CONSTRAINT

```sql
ALTER TABLE child
  ADD CONSTRAINT fk_child_parent
  FOREIGN KEY (fk_col) REFERENCES parent (pk_col)
  ON DELETE RESTRICT ON UPDATE CASCADE;
```

Verify with `SHOW CREATE TABLE child` post-ALTER.

### Phase 6 — Self-Reference Guard (if applicable)

Delegate to
[`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md).

### Phase 7 — Verify

Re-run `probe-fk-readiness.py` post-ALTER and confirm:
- `engine = InnoDB`
- `orphan_count = 0`
- `fk_present = True`
- Trigger smoke-test: `INSERT ... SET fk_col = pk_col` raises SQLSTATE 45000.

## Pitfalls

| Pitfall | Mitigation |
|---|---|
| Sentinel `0` rows present at ALTER time → ALTER fails 1452 | Run Phase 3 first. |
| Self-referencing column + AUTO_INCREMENT PK + CHECK → error 1901 | Use trigger fallback skill (Phase 6). |
| ALTER on InnoDB ~10M-row table takes minutes / table lock | Coordinate maintenance window; consider `pt-online-schema-change`. |
| FK added but app still inserts sentinel `0` | Audit app code post-migration; install guard at Phase 6. |
| Dry-run authorized → days later commit drift | `--require-dry-run-sha` blocks this. |

## Related Skills

- [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) — primitive probes
- [`mariadb-check-autoincrement-trigger-fallback`](../mariadb-check-autoincrement-trigger-fallback/SKILL.md) — self-ref rule
- [`db-backup-bracketing-protocol`](../db-backup-bracketing-protocol/SKILL.md) — safety bracketing
- [`php-mysqli-prepared-statement-modernization`](../php-mysqli-prepared-statement-modernization/SKILL.md) — app-guard idiom in PHP
- [`remote-mysql-roundtrip-minimization`](../remote-mysql-roundtrip-minimization/SKILL.md) — probe efficiency

## Scripts

| Script | Tier | Purpose |
|---|---|---|
| [`scripts/dry-run-update.py`](scripts/dry-run-update.py) | Deterministic | START TXN → UPDATE → verify → ROLLBACK; emits sha for commit step. |
| [`scripts/commit-update.py`](scripts/commit-update.py) | Deterministic | Re-verifies + COMMITs; refuses without matching `--require-dry-run-sha`. |
