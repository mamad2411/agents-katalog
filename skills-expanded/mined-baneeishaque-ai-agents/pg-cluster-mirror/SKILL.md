---
name: pg-cluster-mirror
description: >
  Mirror an on-disk PostgreSQL ClusterSplit dump onto a target cluster (local DSN or SSH-fronted remote) with
    mandatory permission preflight, audit-before-act, pre-mirror backup, and three DB naming modes.
category: Database-Operations
---

# PostgreSQL Cluster Mirror Skill

Restores a ClusterSplit dump (`globals.sql` + per-DB `*.dump`) produced by the
[`pg-cluster-backup-compare`](../pg-cluster-backup-compare/SKILL.md) skill onto
a target PostgreSQL cluster. The mirror is gated by a five-phase pipeline; each
phase **must succeed** before the next runs. The audit report is **always the
first substantial output** rendered — the operator sees the full plan before any
data is touched.

***

## 1. Environment & Dependencies

| Tool | Required for | Install |
|---|---|---|
| `pwsh` (PowerShell 7+) | Script runtime | `brew install powershell` / `apt install powershell` |
| `psql` | Target queries, globals apply | `brew install libpq` / `apt install postgresql-client` |
| `pg_restore` | Per-DB restore | same package |
| `pg_dump` | Local pre-mirror backup | same package |
| `pg_dumpall` | Local globals backup | same package |
| `sshpass` | SSH mode — non-interactive auth | `brew install sshpass` / `apt install sshpass` |

All tools must be on `PATH`. The script performs a dependency check before any network calls.

***

## 2. Parameters Reference

### Source selection

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-SourceDir` | `string` | _(auto)_ | Absolute or relative path to a ClusterSplit dump directory containing `globals.sql` and `*.dump` files. If omitted, the newest directory matching `-SourcePattern` under `db_dumps/` is auto-selected. |
| `-SourcePattern` | `string` | `*-cluster-*-UTC` | Glob applied to `db_dumps/` when `-SourceDir` is omitted. |
| `-OutputDirName` | `string` | `db_dumps` | Sub-directory of the repo root where source dumps are found and pre-mirror backups are written. |

### Target — Local mode

| Parameter | Type | Required | Description |
|---|---|---|---|
| `-TargetDsn` | `string` | **Yes** | Full PostgreSQL DSN: `postgres://user:pass@host:port/db`. The database segment is replaced with `postgres` for the maintenance connection. |

### Target — SSH mode

All four SSH parameters are mutually exclusive with `-TargetDsn`.

| Parameter | Type | Required | Description |
|---|---|---|---|
| `-TargetUser` | `string` | **Yes** | SSH username on the remote server. |
| `-TargetHost` | `string` | **Yes** | Remote hostname or IP address (only port 22 must be reachable). |
| `-TargetPassword` | `string` | **Yes** | SSH password. Passed to `sshpass` via `SSHPASS` env var — never as a CLI argument. |
| `-TargetEnvPath` | `string` | **Yes** | Absolute path to the `.env` file on the **remote** server. Must contain `DATABASE_URL` (or the key set by `-TargetEnvDbKey`). |
| `-TargetEnvDbKey` | `string` | No | `DATABASE_URL` | Key to extract from the remote `.env`. Commented-out lines (starting with `#`) are automatically skipped. |
| `-TunnelLocalPort` | `int` | No | `15432` | Local TCP port for the SSH port-forward tunnel. Auto-increments if in use. |

### Target labelling

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-TargetLabel` | `string` | `mirror-target` | Human-readable identifier included in pre-mirror backup directory names: `db_dumps/<label>-pre-mirror-cluster-<ts>-UTC/`. Use something descriptive like `<env>-<project>`. |

### DB naming mode

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-Mode` | `SameName` \| `Map` \| `New` | `SameName` | Controls how each source DB name is mapped to a target DB name. See §3 for full mode details. |
| `-Mapping` | `hashtable` | `@{}` | Source → target DB name map. **Required** when `-Mode Map`. Must cover every DB in the selected set. |

### DB selection

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-Databases` | `string[]` | _(all)_ | Explicit list of source DB names to mirror. All names must match `*.dump` files in `-SourceDir`. |
| `-IncludePostgresDb` | `switch` | off | Include the `postgres` system database. Off by default because mirroring `postgres` onto an active cluster is rarely desired. |

### Globals

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-IncludeGlobals` | `switch` | off | Apply `globals.sql` (roles, tablespaces, privileges) from the source dump to the target maintenance DB before per-DB restore. Requires `CREATEROLE` or `SUPERUSER`. Off by default — most prod→staging mirrors have their own role set. |

### Safety & control

| Parameter | Type | Default | Description |
|---|---|---|---|
| `-SkipBackup` | `switch` | off | Skip the mandatory pre-mirror backup of the target. **Requires `-Force`** as a paired safety interlock. |
| `-Force` | `switch` | off | Unlocks `-SkipBackup`. Has no other effect. |
| `-WhatIf` | `switch` | off | Run Phases 1–3 only (source resolution, data collection, audit report). No backup, no mirror. |
| `-Confirm` | `switch` | off | Skip the interactive `[y/N]` prompt after the audit report. Useful in CI/CD or scripted workflows. |
| `-Jobs` | `int` | `1` | Number of parallel `pg_restore` workers per database (`--jobs=N`). Typically safe to set to the number of target CPU cores. |

***

## 3. Naming Modes

### SameName (default)

Every source DB is mirrored to an identically named target DB.

```
Source          →  Target          Action
─────────────────────────────────────────────────
<main-db>       →  <main-db>       DROP + CREATE (if exists)
<main-db>       →  <main-db>       CREATE (if not exists)
postgres        →  postgres        (only if -IncludePostgresDb)
```

### Map

Each source DB is renamed to an explicit target name provided via `-Mapping`.
Every selected DB **must** appear in `-Mapping`.

```
Source          →  Target          Action
─────────────────────────────────────────────────
<main-db>       →  <main-db>_prod  DROP + CREATE (if exists)
```

### New

Each source DB is suffixed with a timestamp (`_yyyyMMdd_HHmmss`) to create a
fresh non-colliding target DB. All DBs share the same suffix.

```
Source          →  Target                    Action
──────────────────────────────────────────────────────────────
<main-db>       →  <main-db>_20260514_185500  CREATE (new)
postgres        →  postgres_20260514_185500   CREATE (new)
```

- **Never drops** anything on the target — safe for sandbox restores.
- **Collision guard**: aborts if `<src>_<timestamp>` already exists.

***

## 4. Five-Phase Pipeline

Each phase is gated by the previous one's success. A failure in any phase
produces a red diagnostic, closes the SSH tunnel (if open), and exits 1 **before
any data modification** (Phases 0–3) or **after the backup is already safe**
(Phases 4–5).

### Phase 0 — Dependency check

Verifies that `psql`, `pg_restore`, `pg_dump`, `pg_dumpall` are on `PATH`.
In SSH mode, also checks for `sshpass`.

### Phase 1 — Resolve

**1a — Source directory**: auto-selects newest dump dir if `-SourceDir` omitted.

**1b — Target DSN**: uses `-TargetDsn` in local mode; reads `DATABASE_URL` from
remote `.env` via single `sshpass` SSH command in SSH mode.

**1c — SSH tunnel (SSH mode only)**: opens `sshpass -e ssh -L <port>:localhost:5432 -N`.
Waits up to 15 seconds for the port to accept connections. Always closed in a
`finally` block.

### Phase 2 — Silent data collection

Gathers target role privileges, target PG version, source dump inventory,
per-dump PG versions, target DB list, and resolved target names. No output.

### Phase 3 — Audit report

The audit report is **always the first substantial output**:

```
╔══════════════════════════════════════════════════════════════════╗
║               CLUSTER MIRROR — AUDIT REPORT                     ║
╚══════════════════════════════════════════════════════════════════╝

  Source cluster  : /path/to/db_dumps/<env>-cluster-<ts>-UTC
  Target          : postgres:*****@host:5432 — PG 16.3
  Mode            : SameName
  Transport       : SSH (tunnel → <host>:5432)
  Pre-mirror bkp  : db_dumps/<label>-pre-mirror-cluster-<ts>-UTC/

  Permissions (target role: <user>):
    ✓  CREATEDB   (required)
    ✓  CREATEROLE (required only with -IncludeGlobals)
    ✗  SUPERUSER

  Options:
    globals.sql     : skip  (pass -IncludeGlobals to apply)
    postgres system : skip  (pass -IncludePostgresDb to include)
    Parallel jobs   : 1 per DB

  ┌────────────────────────────┬────────┬────────────────────────────┬──────────────────┐
  │ Source DB                  │ pg-ver │ → Target DB                │ Action           │
  ├────────────────────────────┼────────┼────────────────────────────┼──────────────────┤
  │ <main-db>                  │ 14.20  │ <main-db>                  │ DROP + CREATE    │
  └────────────────────────────┴────────┴────────────────────────────┴──────────────────┘

  Total payload   : 7.92 MB across 1 DB(s)
  ℹ  Forward-restore: source PG 14 → target PG 16 (supported).
```

### Phase 4 — Pre-mirror backup

Always runs unless `-SkipBackup -Force` was passed.

| Target type | Mechanism |
|---|---|
| SSH | Calls `Sync-RemoteDatabaseBackup.ps1 -Scope ClusterSplit -PostDumpAction None` (separate SSH session, independent of the port-forward tunnel) |
| Local | Inline `pg_dumpall --globals-only --no-role-passwords` + `pg_dump --format=custom` per existing target DB |

### Phase 5 — Mirror

Per selected DB in source order:

1. **Terminate connections** (skipped for `New` mode)
2. **DROP DATABASE IF EXISTS** (skipped for `New` mode)
3. **CREATE DATABASE**
4. **pg_restore** `--clean --if-exists --no-owner --no-acl --jobs=<N>`

**Apply globals** (if `-IncludeGlobals`): `psql -d <maintenance-dsn> -v ON_ERROR_STOP=0 -f globals.sql`

***

## 5. SSH Architecture

```
Local machine                    Remote server
─────────────────                ─────────────────────
Mirror-DatabaseCluster.ps1       sshd (port 22)
  ├─ sshpass ssh (env extract) ──→ read .env → DATABASE_URL
  ├─ sshpass ssh -L port:localhost:5432 -N ──────────────┐
  │         (port-forward tunnel)                         ↓
  ├─ psql :port ──────────────────────────────→ PostgreSQL :5432
  ├─ pg_restore ... ───────────────────────────→ PostgreSQL :5432
  └─ pg_dump ──────────────────────────────────→ PostgreSQL :5432
```

- The remote PostgreSQL port (5432) does **not** need to be publicly reachable.
- Credentials via `SSHPASS` env var — never CLI args.
- Tunnel closed in a `finally` block — guaranteed on exit, Ctrl-C, or error.
- Tunnel port starts at `15432` and auto-increments if in use.

### `.env` path notes

The path to the remote `.env` varies per environment. The file must contain
`DATABASE_URL=postgres://...` (or the key set by `-TargetEnvDbKey`) as an
un-commented line.

***

## 6. Permission Matrix

| Action | Minimum required | Who grants it |
|---|---|---|
| Drop + create databases | `CREATEDB` (rolcreatedb) | `ALTER ROLE <user> CREATEDB;` |
| Apply globals | `CREATEROLE` or `SUPERUSER` | `ALTER ROLE <user> CREATEROLE;` |
| pg_restore with `--no-owner --no-acl` | `CREATEDB` + connect | Granted by CREATE DATABASE |
| Terminate other sessions | `pg_terminate_backend()` | DB owner or superuser |

***

## 7. Safety Interlocks

| Guard | Trigger | Override |
|---|---|---|
| Pre-mirror backup | Always runs before Phase 5 | `-SkipBackup -Force` (both required) |
| `-SkipBackup` alone | Immediate error | Must also pass `-Force` |
| Missing CREATEDB | Hard block, exit 1 | Fix role, re-run |
| Missing CREATEROLE + `-IncludeGlobals` | Hard block, exit 1 | Fix role or omit `-IncludeGlobals` |
| Operator confirmation | `[y/N]` prompt after audit | `-Confirm` switch |
| `-WhatIf` | Exits 0 after audit, zero side effects | _(the override itself)_ |
| `Mode=New` collision | Aborts if target exists | Choose different mode or clean up |
| PG version downgrade | ⚠ warning; script does NOT hard-block | Operator must refuse manually |
| pg_restore exit 2+ | `failed(code)` in summary, exit 1 | Use pre-mirror backup to rollback |

***

## 8. Invocation Examples

### Dry run — audit only, local target

```pwsh
pwsh ./scripts/Mirror-DatabaseCluster.ps1 `
    -SourceDir db_dumps/<env>-cluster-<ts>-UTC `
    -TargetDsn 'postgres://<user>@127.0.0.1:5432/postgres' `
    -TargetLabel <env>-local `
    -WhatIf
```

### Full mirror, SSH target, auto-pick newest source

```pwsh
pwsh ./scripts/Mirror-DatabaseCluster.ps1 `
    -TargetUser <ssh-user> -TargetHost <host-ip> -TargetPassword '<ssh-pass>' `
    -TargetEnvPath '<remote-path>/.env' `
    -TargetLabel <env>-<project> `
    -Confirm
```

### New mode — sandbox restore

```pwsh
pwsh ./scripts/Mirror-DatabaseCluster.ps1 `
    -TargetDsn 'postgres://<user>@localhost/postgres' `
    -Mode New -Databases <main-db> -SkipBackup -Force -Confirm
```

### Parallel restore — 4 workers per DB

```pwsh
pwsh ./scripts/Mirror-DatabaseCluster.ps1 `
    -TargetDsn 'postgres://<user>@host/postgres' -TargetLabel <env>-<project> `
    -Databases <main-db> -Jobs 4 -Confirm
```

***

## 9. Exit Codes

| Code | Meaning |
|---|---|
| `0` | All selected DBs restored with status `ok` or `ok-with-warnings`; or `-WhatIf` exited after audit |
| `1` | One or more DBs failed, or a phase error occurred |

When exit 1 occurs after Phase 4, the pre-mirror backup is available for rollback.

***

## 10. Prohibited Behaviors

- MUST NOT skip the permission preflight.
- MUST NOT bypass the audit report.
- MUST NOT skip the pre-mirror backup without explicit `-SkipBackup -Force`.
- MUST NOT recommend `-IncludeGlobals` when the target has its own role set.
- MUST NOT proceed when a PG version downgrade is detected (source major > target major).
- MUST NOT log passwords, full DSN strings, or raw `-Mapping` values to any committed artifact.

***

## 11. Script Inventory

| Script | Language | Purpose |
|---|---|---|
| `scripts/Mirror-DatabaseCluster.ps1` | PowerShell 7+ | Five-phase mirror orchestrator |
| `scripts/Restore-LocalDatabase.ps1` | PowerShell 7+ | Single-DB local restore (narrower scope) |
| `scripts/Sync-RemoteDatabaseBackup.ps1` | PowerShell 7+ | Shared with pg-cluster-backup-compare; used for SSH pre-mirror backup |

## 12. Traceability

Related skills:

- [`pg-cluster-backup-compare`](../pg-cluster-backup-compare/SKILL.md) — produces ClusterSplit dumps; comparison
protocol that informs the audit report
- [`staging-env-fetch`](../staging-env-fetch/SKILL.md) — companion for fetching `.env` from staging environments
- [`postgres-local-dump-restore`](../../postgres-local-dump-restore/SKILL.md) — local single-DB restore counterpart
