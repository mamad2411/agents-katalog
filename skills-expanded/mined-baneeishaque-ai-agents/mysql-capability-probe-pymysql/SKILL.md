---
name: mysql-capability-probe-pymysql
description: Probe a live MySQL server for capability flags such as `CLIENT_MULTI_STATEMENTS` using a tiny Python + PyMySQL script, before adopting the capability in production code. Avoids both Homebrew `mysql` 9.x (which dropped `mysql_native_password`) and a full MariaDB server install.
category: Database
---

# MySQL Capability Probe (PyMySQL) Skill (v1)

> **Skill ID:** `mysql-capability-probe-pymysql`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)

## 1. When to Apply

Apply this skill whenever production code is about to depend on a MySQL server capability
whose presence is NOT guaranteed across MySQL/MariaDB/managed-host vintages — for example:

- `CLIENT_MULTI_STATEMENTS` (the only capability fully implemented in v1).
- Specific authentication plugin (`mysql_native_password`, `caching_sha2_password`).
- Storage-engine availability (`InnoDB`, `Aria`).
- Server SQL mode flags (`ONLY_FULL_GROUP_BY`, `STRICT_TRANS_TABLES`).
- JSON / window-function / CTE support across legacy hosts.

**Anti-trigger:** Do NOT use for routine `SELECT VERSION()` reads — those go through the
application's normal DB layer.

## 2. Why PyMySQL (not `mysql` CLI, not full MariaDB)

| Option | Verdict | Reason |
| --- | --- | --- |
| Homebrew `mysql` 9.x CLI | ❌ Rejected | MySQL 9.x dropped `mysql_native_password` — cannot connect to legacy managed-host DBs (e.g., Helio, many shared-hosting providers). |
| Full MariaDB server install | ❌ Rejected | Multi-GB, runs a local daemon you don't need; overkill to issue one probe query. |
| `mariadb-connector-c` (Homebrew, headers only) | ❌ Rejected | Provides C library only, no CLI binary. |
| **PyMySQL** | ✅ Adopted | Pure-Python (~100 KB), zero native deps, speaks `mysql_native_password` natively, exposes `client_flag` directly. |

## 3. Required Inputs

- A KEY=VALUE secrets file with at minimum:

    ```text
    DB_HOST=...
    DB_USER=...
    DB_PASSWORD=...
    DB_NAME=...
    DB_PORT=3306   # optional
    ```

  This matches the existing `act.secrets` convention used by Account-Ledger and similar projects.
  If your project uses a different layout (`.env`, JSON), convert via a one-liner first.

- A Python interpreter — sourced from **mise global python** (NEVER the system `/usr/bin/python3`
  on macOS, which is Apple Xcode 3.9 and ignores `mise ls` globals). The shipped runner resolves
  this via the DIRECT install path to avoid the `mise exec` cascade pitfall — see
  [`mise-tool-management` Layer 5](../mise-tool-management/SKILL.md).

## 4. Operational Logic

### 4.1 Inputs and Secrets

If the secrets file is a broken symlink (common in cross-machine workspaces), repair it via
[`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md) BEFORE running the
probe — the script gives an opaque `OSError` if it cannot read the file.

### 4.2 One-Shot Probe

```bash
python3 .agents/skills/mysql-capability-probe-pymysql/scripts/probe-runner.py \
    --probe   .agents/skills/mysql-capability-probe-pymysql/scripts/probe-multi-statement.py \
    --secrets /path/to/act.secrets \
    --name    probe-multi
```

The runner:

1. Resolves python via `python3` on PATH (via `mise` if workspace-configured).
2. Idempotently installs `pymysql` via that python's `pip --user` if missing.
3. Ensures `<repo-root>/scratch/` exists and is gitignored
   (delegates to [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)).
4. Runs the probe, redirecting stdout → `scratch/<name>.out`, stderr → `scratch/<name>.err`.
5. Forwards the probe's exit code.

### 4.3 Verdict Schema

Probe scripts MUST emit ONE deterministic verdict line on stdout:

```text
MULTI_STATEMENT_SUPPORTED: True   [((2,),), ((4,),)]
MULTI_STATEMENT_SUPPORTED: False  OperationalError  (1064, 'You have an error...')
```

Exit codes:

- `0` — capability supported.
- `1` — capability not supported (probe ran cleanly, server rejected).
- `2` — configuration error (missing secrets, missing pymysql, no mise python).

### 4.4 Adding a New Capability Probe

1. Copy `probe-multi-statement.py` to `scripts/probe-<capability>.py`.
2. Replace the `cur.execute(...)` block with the capability-specific query.
3. Emit a single verdict line: `<CAPABILITY>: True|False  <evidence>`.
4. Invoke via the same `probe-runner.py` with `--probe scripts/probe-<capability>.py`.

### 4.5 Probe Catalogue (shipped scripts)

| Script | Purpose | Verdict line(s) | Exit codes |
| --- | --- | --- | --- |
| [`scripts/probe-multi-statement.py`](scripts/probe-multi-statement.py) | Probe `CLIENT_MULTI_STATEMENTS` support. | `MULTI_STATEMENT_SUPPORTED: True\|False` | 0 supported / 1 not / 2 config |
| [`scripts/probe-server-flavor.py`](scripts/probe-server-flavor.py) | Identify server flavor (MySQL vs MariaDB — wire-compatible but with diverging system variables), version, default storage engine, per-engine txn/FK/savepoint support, and optionally one table's row count + data/index byte size. Run BEFORE any DDL or flavor-specific docs lookup. | `SERVER_FLAVOR: <flavor>  VERSION: <v>  DEFAULT_ENGINE: <eng>` | 0 ran / 1 connect/query fail / 2 config |
| [`scripts/probe-required-indexes.py`](scripts/probe-required-indexes.py) | Verify that each given `table.column` has an index whose first key part is that column (`SEQ_IN_INDEX=1`). Used as the prerequisite check before relying on single-column index seeks (see [`remote-mysql-roundtrip-minimization` §5.4](../remote-mysql-roundtrip-minimization/SKILL.md)). | `INDEX_PRESENT:` / `INDEX_MISSING:` + summary line | 0 all present / 1 some missing / 2 config |
| [`scripts/apply-engine.py`](scripts/apply-engine.py) | Idempotently `ALTER TABLE … ENGINE=<target>` for each given table. Skips tables already on the target engine. Writer-side counterpart of `probe-server-flavor.py` and a common prerequisite to `probe-fk-readiness.py` (MyISAM blocks FKs). | `SKIP:` / `EXEC:` / `OK:` / `FAIL:` | 0 all on target / 1 some FAIL / 2 config |
| [`scripts/apply-indexes.py`](scripts/apply-indexes.py) | Idempotently `ALTER TABLE … ADD INDEX` for each given `table.column[:idx_name]`. Skips already-indexed columns based on `information_schema.STATISTICS`. Writer-side counterpart of `probe-required-indexes.py`. | `SKIP:` / `EXEC:` / `OK:` / `FAIL:` | 0 all present after run / 1 some FAIL / 2 config |
| [`scripts/probe-fk-readiness.py`](scripts/probe-fk-readiness.py) | For each proposed FK `child.col=parent.col`: report storage ENGINE (MyISAM blocks FKs), existing FK constraints, column nullability, top-level (NULL) counts, and orphan row counts. Prerequisite check before `ALTER TABLE … ADD FOREIGN KEY` (which fails with `ERROR 1452` when orphans exist). Optional `--list-orphans [--list-limit N]` flag enumerates the first N orphan rows (PK + FK column) inline for each FK with orphans > 0 — overlaps with `probe-orphan-rows.py` for the simple FK-orphan case but keeps the pre-flight in a single invocation. | Sectioned report + terminal `FK_READY: True\|False` | 0 ready / 1 blockers / 2 config |
| [`scripts/probe-orphan-rows.py`](scripts/probe-orphan-rows.py) | Enumerate the actual orphan ROWS (not just counts) for each proposed FK `child.col=parent.col`. Sister of `probe-fk-readiness.py`: that probe answers "are we ready?"; this one answers "which rows must we fix?". Treats both `IS NULL` and `=0` as no-parent by default (legacy sentinel pattern); `--strict-null` restricts to NULL only. | Per-check section with COUNT and first `--limit` rows + terminal `ORPHAN_TOTAL: <N> across <K> check(s)` | 0 zero orphans / 1 some found (informational) / 2 config |
| [`scripts/probe-null-rows.py`](scripts/probe-null-rows.py) | Enumerate the actual ROWS whose values in one or more columns are NULL (or the sentinel `0`). Single-sided (no FK join) — used BEFORE a NULL-migration / NOT-NULL ALTER, or before choosing a backfill default. Sister of `probe-orphan-rows.py`. Treats both `IS NULL` and `=0` as no-value by default (legacy sentinel pattern); `--strict-null` restricts to NULL only. | Per-check section with COUNT and first `--limit` rows + terminal `NULL_TOTAL: <N> across <K> check(s)` | 0 zero no-value / 1 some found (informational) / 2 config |

Each probe / DDL script accepts `--secrets <path>` (KEY=VALUE file, same schema as
`probe-multi-statement.py`). The index probes additionally take repeatable `--check`,
`--index`, or `--fk` flags — see each script's `--help`.

Example: pre-flight an FK migration end-to-end —

```bash
SCRIPTS_DIR=.agents/skills/mysql-capability-probe-pymysql/scripts
SECRETS=~/<private-config-repo>/<project>/act.secrets

# 0. Know what server flavor / version / default engine we are aiming DDL at.
python3 "$SCRIPTS_DIR"/probe-server-flavor.py --secrets "$SECRETS" --table transactionsv2

# 1. Are the indexes the FK needs already in place?
python3 "$SCRIPTS_DIR"/probe-required-indexes.py --secrets "$SECRETS" \
    --check transactionsv2.from_account_id \
    --check transactionsv2.to_account_id

# 2. If missing, add them.
python3 "$SCRIPTS_DIR"/apply-indexes.py --secrets "$SECRETS" \
    --index transactionsv2.from_account_id \
    --index transactionsv2.to_account_id

# 3. Is the FK itself addable (engine, orphans, etc.)?
python3 "$SCRIPTS_DIR"/probe-fk-readiness.py --secrets "$SECRETS" \
    --fk transactionsv2.from_account_id=accounts.account_id \
    --fk transactionsv2.to_account_id=accounts.account_id

# 4. If step 3 reported orphans, enumerate them to plan the fix (delete /
#    repoint / create missing parent) — defaults treat both NULL and 0 as
#    "no parent claimed".
python3 "$SCRIPTS_DIR"/probe-orphan-rows.py --secrets "$SECRETS" \
    --check transactionsv2.from_account_id=accounts.account_id \
    --check transactionsv2.to_account_id=accounts.account_id \
    --cols transactionsv2:id,from_account_id,to_account_id,amount,event_date_time \
    --limit 50

# 5. Before a NULL-migration / NOT-NULL ALTER on a column that currently
#    permits NULL or carries 0-sentinels, enumerate the affected rows to
#    decide the backfill default (or whether to delete them outright).
python3 "$SCRIPTS_DIR"/probe-null-rows.py --secrets "$SECRETS" \
    --check transactionsv2.from_account_id \
    --check transactionsv2.to_account_id \
    --cols transactionsv2:id,from_account_id,to_account_id,amount,event_date_time \
    --limit 50
```

## 5. Composition

This skill composes with:

- [`mise-tool-management`](../mise-tool-management/SKILL.md) — Layer 5 (Bypass `mise exec`
  Cascade) provides the direct-binary invocation rule used by `probe-runner.py`.
- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md) — captures probe
  stdout/stderr to gitignored `scratch/` files.
- [`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md) — repairs
  broken secrets-file symlinks before the probe runs.
- [`remote-mysql-roundtrip-minimization`](../remote-mysql-roundtrip-minimization/SKILL.md) —
  the primary CONSUMER of this skill (probes server BEFORE adopting `multi_query`).
- [`mysql-fk-hardening-workflow`](../mysql-fk-hardening-workflow/SKILL.md) —
  end-to-end composer that orchestrates these probes through judgement-gated FK rollout (Phase 1 probe → migrate → bracket → ALTER → verify).

## 6. Prohibited Behaviors

- Calling `mise exec -- python ...` from a CWD whose ancestor `mise.toml` chain contains
  unwanted tools (triggers cascading auto-install of Flutter, PHP, etc.).
- Using `/usr/bin/python3` (Apple Xcode 3.9) — `pymysql` may install there but the version
  is unmanaged and not the developer's pinned environment.
- Installing the full MariaDB server just to issue one probe query.
- Hard-coding credentials in the probe script — always use a secrets file argument.
- Probing a production server without read-only-safe queries (`SELECT 1+1` is safe;
  multi-statement DML probes are NOT — keep probes idempotent and side-effect-free).

## 7. Cross-References

- [`remote-mysql-roundtrip-minimization`](../remote-mysql-roundtrip-minimization/SKILL.md)
- [`mise-tool-management`](../mise-tool-management/SKILL.md) §Layer 5
- [`repo-scratch-output-capture`](../repo-scratch-output-capture/SKILL.md)
- [`dev-env-private-config-symlink`](../dev-env-private-config-symlink/SKILL.md)
