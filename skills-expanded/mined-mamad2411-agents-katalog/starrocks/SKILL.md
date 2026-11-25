---
name: starrocks
description: Run SQL against a StarRocks cluster (MySQL protocol) with built-in risk control. Use this skill whenever the user wants to query, transform, or inspect data in StarRocks — it handles connection, risk classification before execution (asking to confirm high-risk operations), and a schema/sample cache.
---

# StarRocks Skill

You execute SQL on a StarRocks cluster on the user's behalf via two helper
scripts. Everything you do MUST follow the workflow in this file. Do not skip
the risk gate, do not bypass the AskUserQuestion confirmation.

StarRocks speaks the MySQL wire protocol. The CLI is pure-Python (stdlib only —
no driver, no `mysql` binary) and connects to the FE query port (default 9030).

## Tools you have

- `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py <subcmd>` — StarRocks CLI.
  All output is JSON on stdout. Exit code != 0 means failure.
- `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/risk.py --magic '%sql'` — risk classifier.
  Takes the SQL on stdin, prints JSON. (Shared with the zeppelin skill.)

## Connection & profiles

Settings come from env (preferred) or `~/.taku/starrocks.json` (legacy
`~/.starrocks/config.json` still read; override the dir with `TAKU_DIR`). The
config can be a single flat connection, or a `profiles` map for multiple environments:

```json
{
  "default_profile": "prod",
  "profiles": {
    "prod":    { "host": "fe-prod",    "port": 9030, "user": "u", "password": "p" },
    "staging": { "host": "fe-staging", "user": "u", "password": "p" }
  },
  "cache_ttl_days": 30
}
```

- Pick a profile with `--profile NAME` or `STARROCKS_PROFILE`; else `default_profile`,
  else the sole profile. A flat config (no `profiles`) is the implicit `default`.
- Top-level keys outside `profiles` are shared defaults merged into each profile.
- The metadata cache is namespaced per profile, so prod/staging samples never collide.

```
env var                      profile key       default
STARROCKS_HOST               host              (required)
STARROCKS_PORT               port              9030
STARROCKS_USER               user              (required)
STARROCKS_PASSWORD           password          (required)
STARROCKS_DATABASE           database          (optional)
STARROCKS_TIMEOUT_SECONDS    timeout_seconds   30
STARROCKS_CACHE_DIR          cache_dir         ~/.starrocks/cache
STARROCKS_CACHE_TTL_DAYS     cache_ttl_days    30
```

Only `mysql_native_password` accounts are supported. If creds are missing or the
account uses another auth plugin, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py
test-conn` once to surface the exact error and tell the user what to set. Do NOT
prompt the user for passwords — they put them in env or the config file.

## Workflow (mandatory)

Every statement you run goes through these steps. No exceptions.

### 1. Classify risk

Pipe the SQL into the classifier (StarRocks is SQL, so always `--magic '%sql'`):

```bash
echo "$SQL" | python3 ${CLAUDE_PLUGIN_ROOT}/scripts/risk.py --magic '%sql'
```

Output: `{"level": "safe|low|medium|high", "factors": [...], "operations": [...]}`.

**Then layer your own judgment on top.** The classifier is a floor, not a ceiling.
Read the actual SQL and consider:
- Does the table look like production (no `dev_`/`test_`/`tmp_`/`stg_` prefix)?
- Is it a fact table or shared dimension other pipelines depend on?
- Unusual time window, suspiciously broad scan, financial / PII tables?

If any apply, **upgrade** the level and append your reasoning. Never downgrade.

### 2. Apply the auto-approve threshold

The user controls the gate via `STARROCKS_AUTO_APPROVE_LEVEL` (default `safe`):

| Threshold (env)  | Auto-runs without asking |
| ---------------- | ------------------------ |
| `safe` (default) | only `safe`              |
| `low`            | `safe`, `low`            |
| `medium`         | `safe`, `low`, `medium`  |
| `high`           | everything (NOT recommended) |

If the final risk level is **above** the threshold, you MUST call `AskUserQuestion`
with the verbatim SQL, the operations found, your rationale, and the affected
tables before running it. Do not paraphrase the SQL when asking.

### 3. Execute and report

Once cleared (auto or after confirmation):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py query --sql "$SQL"
```

Output JSON shape:
```json
{ "is_table": true, "columns": ["..."], "rows": [{"col": "val"}, ...], "text": "" }
// non-SELECT (DDL/DML) → {"is_table": false, "affected_rows": N, "rows": null}
```

Report to the user:
- `is_table` → show first 20 rows as a markdown table; mention total row count.
- non-table → report `affected_rows`.
- On error: the CLI exits non-zero with the StarRocks error on stderr — show it and offer to diagnose / retry (re-classify any new SQL through the gate).

## Table metadata cache

When you review data involving real tables, cache each table's schema and a
10-row sample so later runs can confirm columns/shape without re-querying.

**Before** querying a table you're unsure about:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py cache get --table mydb.orders
# -> {"status": "hit"|"stale"|"miss", "columns": [...], "sample": [...], "age_days": ...}
```
`hit` → use cached schema/sample. `stale`/`miss` → query, then `cache put`.

**After** confirming a table:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py cache put --table mydb.orders
```
`cache put` runs `DESCRIBE` + `SELECT * LIMIT 10`, idempotent (returns `fresh`
without re-querying if still within TTL); `--force` refreshes on demand. Also:
`cache list`, `cache clear --table db.t | --all`. Cache is per-profile, so the
same `db.table` in prod vs staging is stored separately.

Notes:
- The cache stores **real sample rows in plaintext** on disk. Don't echo large
  samples back unless asked — summarize.
- Pass `--table db.table` (validated); use the fully-qualified name.
- `cache get`/`list`/`clear` are local-only (no connection); only `put` connects.

## What NOT to do

- Do NOT execute anything above the threshold without confirmation.
- Do NOT ever print or log credentials. The CLI redacts passwords from errors.
- Do NOT silently retry a statement that errored — surface it, offer a fix, and
  re-classify any new SQL through the risk gate.

## Quick sanity check

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/starrocks.py test-conn
# {"ok": true, "profile": "...", "result": [{"1": "1"}], "elapsed_seconds": 0.05}
```
