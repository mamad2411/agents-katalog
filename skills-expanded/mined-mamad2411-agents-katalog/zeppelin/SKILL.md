---
name: zeppelin
description: Run SQL / Spark / PySpark / shell paragraphs on an Apache Zeppelin instance with built-in risk control. Use this skill whenever the user wants to query, transform, or inspect data via Zeppelin — the skill handles login, notebook lifecycle, polling for results, AND classifies risk before execution, asking the user to confirm high-risk operations.
---

# Zeppelin Skill

You execute work on an Apache Zeppelin instance on the user's behalf via two
helper scripts. Everything you do MUST follow the workflow in this file.
Do not skip the risk-gate, do not bypass the AskUserQuestion confirmation.

## Tools you have

- `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py <subcmd>` — Zeppelin REST CLI.
  All output is JSON on stdout. Exit code != 0 means failure.
- `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/risk.py --magic <m>` — risk classifier.
  Takes paragraph body on stdin, prints JSON.

`${CLAUDE_PLUGIN_ROOT}` is set by Claude Code to this plugin's root directory.

## Credentials

The CLI reads settings from env vars (preferred) or `~/.taku/zeppelin.json`
(legacy `~/.zeppelin/config.json` still read; override the dir with `TAKU_DIR`).
For every setting the env var wins; if unset, the config key is used; else
the default.

```
env var                          config.json key          default
ZEPPELIN_BASE_URL                base_url                 (required)
ZEPPELIN_USERNAME                username                 (required)
ZEPPELIN_PASSWORD                password                 (required)
ZEPPELIN_NOTE_DIR                note_dir                 __skill/zeppelin   # workspace dir new notes go under
ZEPPELIN_KEEP_NOTES              keep_notes               false              # true = keep notes instead of deleting
ZEPPELIN_TIMEOUT_SECONDS         timeout_seconds          300                # poll cap
ZEPPELIN_POLL_INTERVAL_SECONDS   poll_interval_seconds    1.5                # poll cadence
ZEPPELIN_CACHE_DIR               cache_dir                ~/.zeppelin/cache  # schema+sample cache location
ZEPPELIN_CACHE_TTL_DAYS          cache_ttl_days           30                 # cache freshness window
ZEPPELIN_AUTO_APPROVE_LEVEL      — (env only)             safe               # see risk gate below; read by Claude, not the CLI
```

Example `~/.taku/zeppelin.json`:
```json
{
  "base_url": "http://host:port",
  "username": "user",
  "password": "pass",
  "note_dir": "fin-eng/adhoc",
  "keep_notes": false,
  "timeout_seconds": 300,
  "poll_interval_seconds": 1.5,
  "cache_dir": "~/.zeppelin/cache",
  "cache_ttl_days": 30
}
```

**Multiple environments:** instead of flat keys, the config may hold a `profiles`
map. Select one with `--profile NAME` or `ZEPPELIN_PROFILE` (else `default_profile`,
else the sole profile). Top-level keys are shared defaults merged into each
profile; the cache is namespaced per profile so envs don't collide. A flat config
is the implicit `default` profile (cache un-namespaced). Pass `--profile` before
the subcommand: `zeppelin.py --profile stg exec ...`.

```json
{
  "default_profile": "prod",
  "profiles": {
    "prod": { "base_url": "...", "username": "...", "password": "..." },
    "stg":  { "base_url": "...", "username": "...", "password": "..." }
  },
  "cache_ttl_days": 30
}
```

If creds are missing, run `python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py test-conn`
once to surface the exact error and tell the user what to set. Do NOT prompt
the user for passwords — they should put them in env or the config file.

## Workflow (mandatory)

Every paragraph submission goes through these steps. No exceptions.

### 1. Pick a magic

Translate the user's intent into a Zeppelin paragraph:

| User intent                          | Magic         |
| ------------------------------------ | ------------- |
| SQL on the cluster                   | `%spark.sql`  |
| PySpark code                         | `%pyspark`    |
| Scala / Spark code                   | `%spark`      |
| Shell on the driver                  | `%sh`         |

If the user says "run this SQL" without context, default to `%spark.sql`.

### 2. Classify risk

Pipe the paragraph body into the classifier:

```bash
echo "$CODE" | python3 ${CLAUDE_PLUGIN_ROOT}/scripts/risk.py --magic '%spark.sql'
```

The output is:
```json
{
  "level": "safe|low|medium|high",
  "factors": ["ddl_drop", ...],
  "rationale": "...",
  "operations": ["DROP", "SELECT"]
}
```

**Then layer your own judgment on top.** The classifier is a floor, not a
ceiling. Read the actual SQL/code and consider:
- Does the table name look like production (no `dev_`/`test_`/`tmp_`/`stg_` prefix, no `_test` suffix)?
- Is this hitting a fact table or a shared dimension that other pipelines depend on?
- Is the time window unusual (e.g. UTC small hours, weekends)?
- Does the code launch a long-running job (suspiciously broad scans, cross joins)?
- Does it touch financial / billing / user-PII tables?
- Is there an embedded `spark.sql("...")` the regex missed?

If any of these apply, **upgrade** the level (e.g. from `medium` to `high`)
and append your reasoning to the factors list. Never downgrade what the
classifier produced.

### 3. Apply the auto-approve threshold

The user controls the gate via `ZEPPELIN_AUTO_APPROVE_LEVEL`:

| Threshold (env)   | Auto-runs without asking |
| ----------------- | ------------------------ |
| `safe` (default)  | only `safe`              |
| `low`             | `safe`, `low`            |
| `medium`          | `safe`, `low`, `medium`  |
| `high`            | everything (NOT recommended) |

If the final risk level is **above** the threshold, you MUST call
`AskUserQuestion` with the full SQL/code and the risk factors before
calling `zeppelin.py submit` or `exec`. Do not paraphrase the SQL when
asking — show it verbatim. Example question shape:

```
question: "Run this `high` risk paragraph on Zeppelin?"
options:
  - "Run it"
  - "Show me a dry-run first"
  - "Cancel"
```

Include in the question body: the magic, the operations the classifier
found, your additional rationale, and the affected tables / paths.

### 4. Execute and report

Once cleared (auto or after confirmation):

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py exec \
  --magic '%spark.sql' \
  --code "$CODE" \
  --name 'dau-check'
```

Always pass `--name` with a short, business-meaningful label describing what
the query does (`dau-check`, `order-revenue`, `user-funnel`) — kebab-case, no
spaces. The CLI places it under `note_dir` and appends a `-<timestamp>` suffix
itself, so do NOT add your own date/time; just give the semantic name. The
final note path looks like `<note_dir>/dau-check-20260521-143005`. If you omit
`--name`, it falls back to the meaningless label `query`.

`exec` submits, polls until terminal, and (by default) deletes the temporary
note. The note is created under `ZEPPELIN_NOTE_DIR` (default `__skill/zeppelin`).
Pass `--keep-note` to retain it, or set `ZEPPELIN_KEEP_NOTES=1` to keep by
default. Use `--no-keep-note` to force-delete even when the env default keeps.

Output JSON shape:
```json
{
  "status": "FINISHED" | "ERROR" | "ABORT",
  "is_table": true,
  "rows": [{"col": "val", ...}, ...],   // null when not a TABLE result
  "text": "stdout / tracebacks",
  "note_id": "2K...",
  "paragraph_id": "20...",
  "note_name": "..."
}
```

Report to the user:
- On `FINISHED` + `is_table`: show first 20 rows as a markdown table; mention total row count.
- On `FINISHED` + non-table: show the `text` (likely PySpark stdout or `df.show()` output).
- On `ERROR` / `ABORT`: show `text` (Zeppelin puts the traceback there) and offer to diagnose / retry with a fix.
- On `timed_out: true`: tell the user the run is still in flight, give them the `note_id` + `paragraph_id` so they can poll later with `zeppelin.py poll`.

## Table metadata cache

When you review data that involves real tables, cache each table's schema and a
10-row sample under `cache_dir` (default `~/.zeppelin/cache`, TTL 30 days). This
lets later runs confirm a table's columns/shape without re-querying Zeppelin.

**Before** querying a table you're unsure about, check the cache first:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py cache get --table uparpu_main.orders
# -> {"status": "hit"|"stale"|"miss", "columns": [...], "sample": [...], "age_days": ...}
```

- `hit` → use the cached columns/sample; no need to re-query schema.
- `stale` or `miss` → query as normal, then populate the cache (below).

**After** reviewing a table (or whenever you confirm one), cache it:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py cache put --table uparpu_main.orders
```

`cache put` runs `DESCRIBE` + `SELECT * LIMIT 10` (both auto-cleaned, never kept
as notes) and writes the entry. It's cheap and idempotent: if the entry is still
fresh it returns `status: fresh` without re-querying. Use `--force` to refresh on
demand (the user's "强制更新"). Other commands:

```bash
zeppelin.py cache list                       # all cached tables + freshness
zeppelin.py cache clear --table db.t          # evict one
zeppelin.py cache clear --all                 # evict everything
```

Notes:
- The cache stores **real sample rows in plaintext** on the user's disk. That's
  intended, but don't echo large samples back unless asked — summarize.
- Pass `--table db.table` (validated as `db.table`); use the fully-qualified name.
- `cache get`/`list`/`clear` are local-only (no Zeppelin call); only `put` logs in.

## Multi-paragraph sessions

For exploratory work where the user wants several paragraphs sharing one
SparkContext, use `submit` then `poll` repeatedly with the same note id.
Today the CLI doesn't expose a "session" abstraction — every `exec` call
creates a fresh note. If the user explicitly asks for a multi-paragraph
notebook, do:

1. `zeppelin.py submit --magic ... --code ...` → note_id, para_id
2. `zeppelin.py poll --note <id> --para <id>` → result
3. To add another paragraph in the same note: use `submit` with a name like
   `notebook/<existing-note-id>` and call the Zeppelin REST endpoint
   `POST /api/notebook/{noteId}/paragraph` — this isn't exposed by the CLI
   yet, so tell the user it needs a tiny CLI extension and offer to add it.

## What NOT to do

- Do NOT execute anything above the threshold without confirmation.
- Do NOT ever print or log credentials. The CLI already redacts ticket
  values from errors; if you echo a CLI error, you don't need to redact
  again, but never insert credentials into prompts.
- Do NOT silently retry a paragraph that errored — surface the error,
  offer a fix, and re-classify any new SQL through the risk gate.
- Do NOT create notebooks the user didn't ask for. The skill auto-cleans
  the temp note after `exec`; only set `--keep-note` when the user asks.

## Quick sanity check

If you're unsure the skill is wired up, run:
```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/zeppelin.py test-conn
```
Output `{"ok": true, "principal": ..., "elapsed_seconds": ...}` = good.
