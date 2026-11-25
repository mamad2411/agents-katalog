---
name: pg-cluster-backup-compare
description: >
  General protocol for backing up PostgreSQL clusters (production + staging) via SSH-streamed pg_dumpall_split, and
    comparing dump contents (globals, schema, data) across environments.
category: Database-Operations
---

# PostgreSQL Cluster Backup & Compare Skill (v1)

This skill covers two tightly coupled workflows built on the `Sync-RemoteDatabaseBackup.ps1` +
`parse_dotenv_and_stream_pg_dump.bash` toolchain:

1. **ClusterSplit Backup** — stream a full logical cluster backup from any remote server over SSH into
   timestamped local directories, commit, and push.
2. **Cluster Dump Compare** — diff two cluster dump directories (globals + per-DB schema/data) to surface
   role drift, schema drift, and data volume differences between environments.

***

## 1. Environment & Dependencies

The agent MUST verify the following tools before proceeding:

| Tool | Verify | Install (brew) | Install (apt) | Install (yum) |
|---|---|---|---|---|
| `pwsh` | `pwsh --version` | `brew install --cask powershell` | [MS docs](https://learn.microsoft.com/powershell/scripting/install/installing-powershell-on-linux) | same |
| `sshpass` | `which sshpass` | `brew install sshpass` | `sudo apt install sshpass` | `sudo yum install sshpass` |
| `pg_restore` | `pg_restore --version` | `brew install libpq` | `sudo apt install postgresql-client` | `sudo yum install postgresql` |
| `psql` | `psql --version` | `brew install libpq` | `sudo apt install postgresql-client` | `sudo yum install postgresql` |
| `diff` | `which diff` | preinstalled | preinstalled | preinstalled |

On macOS, `libpq` binaries require a PATH addition:

```bash
export PATH="/opt/homebrew/opt/libpq/bin:$PATH"
```

The remote server MUST have `pg_dumpall`, `pg_dump`, `psql`, `bash 3.2+`, `mktemp`, `wc` available.

***

## 2. Toolchain Overview

```
Sync-RemoteDatabaseBackup.ps1   ← PowerShell orchestrator (local)
  └─ parse_dotenv_and_stream_pg_dump.bash  ← bash helper (executed remotely via SSH stdin)
```

Scripts live at:

```
scripts/Sync-RemoteDatabaseBackup.ps1
scripts/parse_dotenv_and_stream_pg_dump.bash
```

***

## 3. ClusterSplit Backup

### 3.1 What ClusterSplit Does

`-Scope ClusterSplit` triggers `DUMP_TOOL=pg_dumpall_split` in the bash helper, which:

1. Runs `pg_dumpall --globals-only --no-role-passwords` → `globals.sql` (plain SQL)
2. Enumerates all connectable non-template databases:
   ```bash
   psql "$DB_URL" -Atc \
     "SELECT datname FROM pg_database WHERE NOT datistemplate AND datallowconn ORDER BY datname"
   ```
3. Runs `pg_dump --format=custom` per database → `<dbname>.dump` (compressed binary)

Each file is emitted over the SSH stdout stream using the **length-prefixed wire protocol** (§3.2).

**Why `--no-role-passwords`**: The `DATABASE_URL` role is typically a non-superuser and cannot read
`pg_authid`. Omitting passwords lets `pg_dumpall --globals-only` succeed. Role definitions (name,
attributes, session config) are still fully backed up. Reset passwords on staging post-restore.

**Why custom format for databases**: Already zlib-compressed; supports parallel restore via
`pg_restore -j N`; supports surgical per-table/schema restore. Plain SQL would require single-threaded
`psql` execution and is 3–5× larger on the wire.

### 3.2 Wire Protocol (Length-Prefixed Multiplexing)

The bash helper emits all files over a single SSH stdout stream using this protocol:

```
FILE:<filename>:<20-digit-zero-padded-byte-count>:\n
<raw bytes>
FILE:<filename>:<20-digit-zero-padded-byte-count>:\n
<raw bytes>
...
DONE\n
```

**Why not tar**: `tar` requires file sizes upfront; using `<(process substitution)` gives tar a
`/dev/fd/N` path whose size it cannot determine, causing silent corruption on non-GNU tar (e.g., macOS
`bsdtar`). Custom archives are already compressed — gzip wrapping adds overhead with no benefit.

**Remote temp disk**: `emit_stream_file()` writes one file at a time to a `mktemp` file, emits it,
then `rm -f`. Peak remote disk usage = size of the largest single database dump, not the total.

### 3.3 Positional Argument Contract (SSH)

The bash script receives four positional args via `bash -s -- arg1 arg2 arg3 arg4`:

| Position | Name | ClusterSplit value | Note |
|---|---|---|---|
| `$1` | `REMOTE_ENV_PATH` | actual path | path to `.env` on remote |
| `$2` | `DUMP_FORMAT_FLAG` | `--format=plain` | **placeholder only** — ignored in split mode |
| `$3` | `ENV_DB_KEY` | `DATABASE_URL` | key to parse from `.env` |
| `$4` | `DUMP_TOOL` | `pg_dumpall_split` | selects ClusterSplit path |

**Critical**: `$2` MUST be a non-empty string. SSH collapses empty quoted args (`''`) when reassembling
the remote command, shifting `$3` and `$4` — causing the bash script to grep the `.env` file for a key
named `pg_dumpall_split` and emit `ERR:pg_dumpall_split_not_found`.

### 3.4 PowerShell Stream Reader

`Read-ClusterSplitStream` uses `System.Diagnostics.Process` (not PowerShell's `>` operator) to capture
stdout as a raw binary `System.IO.Stream`. PowerShell's own redirection operators corrupt binary data
(they decode to strings using the console encoding).

The reader:
- Reads header bytes one-by-one until `LF (0x0A)` — headers are short ASCII
- Parses `FILE:<name>:<020d>:\n` with a regex
- Streams file bytes directly to `System.IO.File::OpenWrite` using a 65 536-byte copy buffer
- Writes each file to `<prefix>-pending/<filename>` — no mux/temp file locally
- Returns a list of written paths

### 3.5 Invocation

All SSH connection parameters are mandatory:

```bash
$DatabasePrefix = '<env-prefix>'    # e.g. 'myapp-production', 'myapp-staging'
$RemoteEnvPath  = '<remote-env-path>'  # absolute path to .env on remote server

pwsh ./scripts/Sync-RemoteDatabaseBackup.ps1 \
  -User '<ssh-user>' \
  -ServerHost '<host-ip>' \
  -Password '<ssh-password>' \
  -RemoteEnvPath $RemoteEnvPath \
  -DatabasePrefix $DatabasePrefix \
  -Scope ClusterSplit \
  -PostDumpAction Push
```

**`-RemoteEnvPath` discovery**: If the path is unknown, run:

```bash
sshpass -p '<password>' ssh -o StrictHostKeyChecking=no '<user>@<host>' \
  "find /home -name '.env' 2>/dev/null"
```

Pick the path under the active deployment directory (ignore dated-backup dirs like `<app>-<DD-MM-YY>/`).

### 3.6 Output

A timestamped subdirectory under `db_dumps/`:

```
db_dumps/
  <env-prefix>-cluster-<dd-MM-yyyy-HH-mm>-UTC/
    globals.sql           ← roles, tablespaces, DB-level settings (plain SQL)
    <main-db>.dump        ← main application DB (custom format, compressed)
    postgres.dump         ← system DB (usually trivial; safe to skip on restore)
```

Timestamp is extracted from the `-- Started on` header in `globals.sql`. Falls back to local clock if
header is absent.

### 3.7 Commit Message Format

The commit message is auto-derived from `$DatabasePrefix`:

```
DB Dump (Production): May 12 2026 19:19 UTC, May 13 2026 00:49 IST, May 12 2026 23:19 GST
DB Dump (Staging):    May 12 2026 19:32 UTC, May 13 2026 01:02 IST, May 12 2026 23:32 GST
```

The `(Production)` / `(Staging)` label is extracted via regex from the prefix:

```powershell
$EnvMatch = [regex]::Match($DatabasePrefix, '(?i)(production|prod|staging|stg|development|dev|uat|qa|test)')
```

***

## 4. Cluster Dump Compare

The agent MUST execute every sub-step below — partial comparisons (e.g., only `globals.sql` + main DB)
are FORBIDDEN. Two clusters are considered "compared" only after **every database**, **every globals
artifact**, and **every cluster-level metadata** has been diffed.

### 4.1 Find the Latest Dumps

```bash
ls db_dumps/
```

Identify the two dump directories to compare by timestamp in the directory name. Record both as
variables:

```bash
ENV_A="db_dumps/<env-a-cluster-dir>"
ENV_B="db_dumps/<env-b-cluster-dir>"
```

### 4.2 Compare PostgreSQL Server Version (Cluster-Level)

```bash
echo "Env A PG version: $(pg_restore --list "$ENV_A/postgres.dump" | grep 'database version' | head -1)"
echo "Env B PG version: $(pg_restore --list "$ENV_B/postgres.dump" | grep 'database version' | head -1)"
```

| Result | Implication |
|---|---|
| Versions match | No restore-direction constraint |
| Env A major < Env B major | A → B restore OK; B → A restore FORBIDDEN (forward-only) |
| Env A major > Env B major | B → A restore OK; A → B restore requires `pg_upgrade` or fresh cluster on matching major |

### 4.3 Compare globals.sql

```bash
diff "$ENV_A/globals.sql" "$ENV_B/globals.sql"
```

| Diff element | Meaning |
|---|---|
| `CREATE ROLE` / `ALTER ROLE` name differs | Environments use different app roles — restore needs role mapping |
| `ALTER ROLE ... SET ...` absent in one side | One env has explicit session config; other relies on cluster defaults |
| `\restrict` token differs | Per-dump random nonce — always differs, always safe to ignore |
| Extra `-- User Configurations` block | One role has persistent session settings the other lacks |

### 4.4 Compare Database Inventory (Cluster Clutter Audit)

```bash
a_dbs=$(ls "$ENV_A"/*.dump | xargs -n1 basename | sed 's/\.dump$//' | sort)
b_dbs=$(ls "$ENV_B"/*.dump | xargs -n1 basename | sed 's/\.dump$//' | sort)

echo "=== Databases ONLY in Env A ==="
comm -23 <(echo "$a_dbs") <(echo "$b_dbs")
echo "=== Databases ONLY in Env B (potential clutter) ==="
comm -13 <(echo "$a_dbs") <(echo "$b_dbs")
echo "=== Databases in BOTH ==="
comm -12 <(echo "$a_dbs") <(echo "$b_dbs")
```

For each env-B-only database, classify it as:

| Pattern | Likely identity | Recommendation |
|---|---|---|
| `<dbname>_<DD_MM_YYYY>` | Old snapshot (manual `CREATE DATABASE ... TEMPLATE`) | Confirm with user, then `DROP DATABASE` |
| `myproject` | Django startproject default | Drop after confirming no app uses it |
| Other | Unknown — INVESTIGATE | Ask user before recommending action |

### 4.5 Compare Each Common Database (Schema)

```bash
tables_of() {
    pg_restore --list "$1" | grep " TABLE public " \
        | sed 's/.*TABLE public //' | sed 's/ [^ ]*$//' | sort
}

# 4.5a Common databases — strict A vs B diff per DB
for db in $(comm -12 <(echo "$a_dbs") <(echo "$b_dbs")); do
    echo ""
    echo "=== Database: $db ==="
    p=$(tables_of "$ENV_A/$db.dump")
    s=$(tables_of "$ENV_B/$db.dump")
    echo "  Tables: env_a=$(echo "$p" | grep -c .)  env_b=$(echo "$s" | grep -c .)"
    miss=$(comm -23 <(echo "$p") <(echo "$s"))
    extra=$(comm -13 <(echo "$p") <(echo "$s"))
    [ -n "$miss"  ] && { echo "  Missing from Env B:"; echo "$miss"  | sed 's/^/    /'; }
    [ -n "$extra" ] && { echo "  Extra in Env B:";    echo "$extra" | sed 's/^/    /'; }
done

# 4.5b Env-B-only databases — schema diff vs the main app DB from Env A
main_app_db="<main-db>"   # the project's primary application database name
for db in $(comm -13 <(echo "$a_dbs") <(echo "$b_dbs")); do
    [ ! -f "$ENV_B/$db.dump" ] && continue
    echo ""
    echo "=== Env-B-only DB: $db (vs Env A $main_app_db) ==="
    p=$(tables_of "$ENV_A/$main_app_db.dump")
    s=$(tables_of "$ENV_B/$db.dump")
    echo "  Tables: $db=$(echo "$s" | grep -c .)  env_a_$main_app_db=$(echo "$p" | grep -c .)"
    miss=$(comm -23 <(echo "$p") <(echo "$s"))
    extra=$(comm -13 <(echo "$p") <(echo "$s"))
    [ -n "$miss"  ] && { echo "  Missing from $db:"; echo "$miss"  | sed 's/^/    /'; }
    [ -n "$extra" ] && { echo "  Extra in $db:";    echo "$extra" | sed 's/^/    /'; }
done
```

Schema-identical env-B-only databases (zero missing, zero extra) are usually **historical snapshots**
taken before schema drift — note the snapshot date encoded in the name and treat as historical reference.

### 4.6 Compare postgres System Database

```bash
echo "=== postgres system DB (Env A) ==="
pg_restore --list "$ENV_A/postgres.dump" | tail -20

echo "=== postgres system DB (Env B) ==="
pg_restore --list "$ENV_B/postgres.dump" | tail -20
```

Flag any `SCHEMA`, `TABLE`, `FUNCTION`, `DEFAULT ACL`, `EXTENSION` entries as anomalies and recommend
investigation — application data in the `postgres` DB is almost always a misconfiguration.

### 4.7 Compare Data Coverage Per Common Database

```bash
for db in $(comm -12 <(echo "$a_dbs") <(echo "$b_dbs")); do
    pd=$(pg_restore --list "$ENV_A/$db.dump" | grep -c " TABLE DATA ")
    sd=$(pg_restore --list "$ENV_B/$db.dump" | grep -c " TABLE DATA ")
    psize=$(du -sh "$ENV_A/$db.dump" | cut -f1)
    ssize=$(du -sh "$ENV_B/$db.dump" | cut -f1)
    printf "  %-20s env_a: %3d data tables (%s)  |  env_b: %3d data tables (%s)\n" \
        "$db" "$pd" "$psize" "$sd" "$ssize"
done
```

A lower data-table count on env B is consistent with schema drift (missing tables can't have data).
A lower dump size with **identical** schema indicates volume drift.

### 4.8 Compare Extensions Per Common Database

```bash
for db in $(comm -12 <(echo "$a_dbs") <(echo "$b_dbs")); do
    echo "=== $db extensions ==="
    echo "  Env A: $(pg_restore --list "$ENV_A/$db.dump" | grep -c EXTENSION) extension(s)"
    pg_restore --list "$ENV_A/$db.dump" | grep EXTENSION | sed 's/^/    /'
    echo "  Env B: $(pg_restore --list "$ENV_B/$db.dump" | grep -c EXTENSION) extension(s)"
    pg_restore --list "$ENV_B/$db.dump" | grep EXTENSION | sed 's/^/    /'
done
```

Extension drift (e.g., `pgcrypto` on one side but not the other) WILL break restores — the target
must `CREATE EXTENSION` before the dump can apply.

### 4.9 Summary Report Format (MANDATORY)

After running §4.2–4.8, the agent MUST present a structured summary. Example template:

```
Cluster-level:
  PG version     : env_a=14.20  env_b=16.13   ← MAJOR VERSION DRIFT (A→B OK, reverse FORBIDDEN)
  App role       : env_a=appuser  env_b=myprojectuser   ← DRIFT
  Role config    : env_b has ALTER ROLE session settings; env_a has none

Database inventory:
  Env A-only    : (none)
  Env B-only    : app_20_01_2026 (snapshot Jan 2026, schema = current env_a), myproject (Django default)
  Common        : <main-db>, postgres

Common DB drift:
  <main-db>     : 80 env_a / 74 env_b  ← 6 tables missing from env_b
  postgres      : env_a empty; env_b has SCHEMA public + DEFAULT ACL ← ANOMALY

Data volume:
  <main-db>     : env_a=7.9 MB / env_b=1.8 MB (4.4× smaller)

Extensions:
  <main-db>     : none either side
  postgres      : none either side

Recommended actions:
  1. Migrate the 6 missing tables to env_b (forward-only restore)
  2. Drop staging cluster clutter: app_20_01_2026, myproject
  3. Investigate why env_b postgres system DB has non-default schema
  4. Reset appuser password on env_b if applying globals
```

***

## 5. Restore (Production → Staging Mirror)

### 5.1 Pre-requisites

- `globals.sql` from the source creates the app role on the target
- If the target already has the required roles, `psql -f globals.sql` emits harmless
  `ERROR: role already exists` — safe to ignore (redirect stderr to `/dev/null` if needed)
- `postgres.dump` is trivially small (system DB) — safe to skip

### 5.2 Commands

```bash
# 1. Apply globals (roles, tablespaces, DB-level settings)
psql -h <target-host> -U postgres -f db_dumps/<source-cluster-dir>/globals.sql 2>/dev/null

# 2. Drop and recreate the target database for a clean mirror
psql -h <target-host> -U postgres -c "DROP DATABASE IF EXISTS <main-db>;"
psql -h <target-host> -U postgres -c "CREATE DATABASE <main-db> OWNER <app-role>;"

# 3. Parallel restore (tune -j to target CPU count; never exceed max_connections / 2)
pg_restore \
  -h <target-host> -U postgres \
  -d <main-db> \
  --no-owner --no-privileges \
  --clean --if-exists \
  -j 4 \
  db_dumps/<source-cluster-dir>/<main-db>.dump

# 4. Reset app role password (no hashes in --no-role-passwords backup)
psql -h <target-host> -U postgres \
  -c "ALTER ROLE <app-role> WITH PASSWORD '<target-password>';"
```

### 5.3 Flags Explained

| Flag | Reason |
|---|---|
| `--no-owner` | Reassigns all objects to the connecting role; the production owner may not exist identically on target |
| `--no-privileges` | Strips GRANT statements referencing non-existent roles |
| `--clean --if-exists` | Drops objects before recreating — idempotent across re-runs |
| `-j 4` | Parallel restore workers — custom format only; invalid for plain SQL |

***

## 6. Prohibited Behaviors

- MUST NOT log SSH passwords, `DATABASE_URL` values, or role passwords to any committed artifact.
  Show only masked forms (`***`).
- MUST NOT pass an empty string `''` as `$2` (DUMP_FORMAT_FLAG) in the SSH invocation — SSH collapses
  it and corrupts the positional arg contract.
- MUST NOT suppress `emit_stream_file` stderr entirely — capture it to a `tmperr` file and relay it on
  failure so the root cause is visible.
- MUST NOT use `pg_restore` on a plain SQL dump (`.sql`) — use `psql -f` instead.
- MUST NOT grant `SUPERUSER` to the application role during restore bootstrap.
- MUST NOT delete or overwrite existing dumps.
- MUST NOT declare a cluster comparison "complete" after diffing only `globals.sql` and the main app
  database. §4.2–4.8 are ALL mandatory.
- MUST NOT recommend `DROP DATABASE` on an env-B-only database without first classifying it via §4.4
  and confirming with the user.
- MUST NOT recommend a reverse restore across PostgreSQL major version boundaries (§4.2).

***

## 7. Script Inventory

| Script | Language | Purpose |
|---|---|---|
| `scripts/Sync-RemoteDatabaseBackup.ps1` | PowerShell 7+ | Orchestrates remote backup via SSH, reads length-prefixed stream, writes local dump files |
| `scripts/parse_dotenv_and_stream_pg_dump.bash` | Bash 3.2+ | Executed remotely via SSH stdin; parses `.env` and streams dump output |

## 8. Environment & Dependencies

See §1 for the full dependency table. The scripts are self-contained — no external packages beyond
the system tools listed.

## 9. Traceability

Related skills:

- [`pg-cluster-mirror`](../pg-cluster-mirror/SKILL.md) — restores these dumps onto a target cluster with
audit-before-act safety
- [`postgres-local-dump-restore`](../../postgres-local-dump-restore/SKILL.md) — local single-DB restore counterpart
- [`env-example-creation`](../../env-example-creation/SKILL.md) — companion for sanitizing fetched `.env` files
