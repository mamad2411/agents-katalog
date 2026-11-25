---
name: mariadb-check-autoincrement-trigger-fallback
description: Documents the MariaDB error 1901 pitfall and ships a BEFORE INSERT and BEFORE UPDATE trigger fallback for CHECK constraints on AUTO_INCREMENT columns.
category: Database
---

# MariaDB CHECK on AUTO_INCREMENT — Trigger Fallback Skill

> **Skill ID:** `mariadb-check-autoincrement-trigger-fallback`<br>
> **Version:** 1.0.0<br>
> **Type:** Atomic + script

## Description

Document the **MariaDB error 1901 misleading-attribution pitfall** and ship
the BEFORE INSERT + BEFORE UPDATE trigger fallback that replaces a
forbidden CHECK constraint on an AUTO_INCREMENT primary key.

## The Pitfall (Error 1901)

When you try to add a CHECK constraint that **references an
AUTO_INCREMENT column** — directly or transitively (e.g. comparing it
to another column) — MariaDB / MySQL refuses with:

```
ERROR 1901 (HY000): Function or expression '<other_col>'
cannot be used in the CHECK clause of <constraint_name>
```

**The error message names the OTHER column, not the AUTO_INCREMENT
column.** This is the trap: the column actually responsible (the
AUTO_INCREMENT PK) is never mentioned. Engineers spend hours trying to
"fix" the named column before discovering the real cause.

### Reproducer

```sql
CREATE TABLE accounts (
  account_id        INT AUTO_INCREMENT PRIMARY KEY,
  parent_account_id INT NULL
);

ALTER TABLE accounts
  ADD CONSTRAINT chk_no_self_parent
  CHECK (parent_account_id IS NULL OR parent_account_id <> account_id);
-- ERROR 1901: Function or expression 'parent_account_id'
--             cannot be used in the CHECK clause of chk_no_self_parent
```

The error names `parent_account_id`. The actual offender is
`account_id` (the AUTO_INCREMENT PK).

### Confirmed scope

- MariaDB 10.2 through at least **12.2.2** (current as of authoring).
- MySQL 8.0+ has the same constraint.
- CHECK constraints in general WORK on both engines (since MariaDB 10.2
  / MySQL 8.0.16) — the restriction is **specifically** on referencing
  AUTO_INCREMENT columns.

## The Fallback: BEFORE Triggers

A `BEFORE INSERT` + `BEFORE UPDATE` trigger pair using `SIGNAL SQLSTATE
'45000'` reproduces CHECK semantics:

```sql
DELIMITER //
CREATE TRIGGER trg_accounts_no_self_parent_ins
BEFORE INSERT ON accounts
FOR EACH ROW
BEGIN
  IF NEW.parent_account_id IS NOT NULL
     AND NEW.parent_account_id = NEW.account_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'parent_account_id must not equal account_id';
  END IF;
END//

CREATE TRIGGER trg_accounts_no_self_parent_upd
BEFORE UPDATE ON accounts
FOR EACH ROW
BEGIN
  IF NEW.parent_account_id IS NOT NULL
     AND NEW.parent_account_id = NEW.account_id THEN
    SIGNAL SQLSTATE '45000'
      SET MESSAGE_TEXT = 'parent_account_id must not equal account_id';
  END IF;
END//
DELIMITER ;
```

**Both** triggers are required: a CHECK fires on INSERT + UPDATE, so
the trigger pair must too. A single BEFORE INSERT misses the UPDATE
attack vector.

### Why not a single trigger?

MariaDB does not support `BEFORE INSERT OR UPDATE` (PostgreSQL does).
You MUST author both.

## Idempotent Installation

Use [`scripts/install-no-self-fk-trigger.py`](scripts/install-no-self-fk-trigger.py):

```bash
python3 .agents/skills/mariadb-check-autoincrement-trigger-fallback/scripts/install-no-self-fk-trigger.py \
    --secrets /path/to/db.secrets \
    --table accounts \
    --pk-col account_id \
    --parent-col parent_account_id
```

The script DROPs any pre-existing same-named trigger before CREATE, so
re-running is safe.

## Smoke Test

```sql
-- Should fail with SQLSTATE 45000:
UPDATE accounts SET parent_account_id = account_id WHERE account_id = 1;
-- ERROR 1644: parent_account_id must not equal account_id

-- Should succeed:
UPDATE accounts SET parent_account_id = 2 WHERE account_id = 1;
```

## Performance Cost

- Per-row trigger overhead: **~5–20 µs** on modern InnoDB.
- At 100 writes/day (chart-of-accounts workload): unmeasurable.
- At 10k writes/second: ~50–200 ms/sec aggregate CPU — consider
  dropping the trigger and relying on app-layer guard only.

## Defense-in-Depth Pairing

This DB trigger is the **last line of defense**. Pair it with an
app-layer guard (see
[`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md)
§Decision: Constraint Placement Matrix) so the request fails fast at
the application boundary, with the trigger catching only direct-DB or
buggy-client writes.

## Related Skills

- [`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md) — composer that invokes this skill in Phase 6.
- [`mysql-capability-probe-pymysql`](../mysql-capability-probe-pymysql/SKILL.md) — primitive probes; use `SHOW TRIGGERS` to verify install.

## Scripts

| Script | Tier | Purpose |
|---|---|---|
| [`scripts/install-no-self-fk-trigger.py`](scripts/install-no-self-fk-trigger.py) | Deterministic | Idempotent BEFORE INSERT + BEFORE UPDATE trigger installer for any `(table, parent_col, pk_col)`. |
