---
name: hermes-usage-analytics
description: Query Hermes' own state.db for usage, cost, and session analytics — schema reference, query patterns, dashboard generation, and cron integration. Covers the sessions, session_model_usage, and messages tables for building tools that track and visualize Hermes' operational data.
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [hermes, analytics, dashboards, state-db, sqlite, costs, usage-tracking]
    triggers:
      - "build usage dashboard for hermes"
      - "query state.db for analytics"
      - "track hermes token costs"
      - "hermes usage report"
      - "analyze session data in state.db"
      - "hermes cost tracking"
      - "hermes analytics dashboard"
      - "state.db schema"
      - "hermes session analytics"
      - "recover discord thread from state.db"
      - "read past discord conversation"
      - "find what was discussed in thread"
      - "where did we leave off"
      - "look over thread"
      - "mining thread content"
    related_skills: [hermes-system-backup, pim-ingestion-pipeline, hermes-agent]
---
# Hermes Usage Analytics

Patterns and reference for querying Hermes' operational database (`state.db`) to build usage, cost, and session analytics.

## Database Location

`~/AppData/Local/hermes/state.db` — SQLite database. Can be 1-4GB depending on session history.

**Cron run history is NOT in state.db.** `state.db` has no cron tables — queries like `SELECT * FROM cron_runs` fail with `no such table: cron_runs`. Scheduler run history lives in `~/AppData/Local/hermes/cron/executions.db` (table `executions`, columns: `id, job_id, source, process_id, pid, process_started_at, status, claimed_at, started_at, finished_at, error`). Quick failure check for health pulses:

```python
import sqlite3
db = sqlite3.connect('${USER_HOME}/AppData/Local/hermes/cron/executions.db')
for r in db.execute("""SELECT job_id, status, started_at, substr(error,1,120)
FROM executions WHERE status='failed' ORDER BY started_at DESC LIMIT 5"""):
    print(r)
```

Scheduler liveness markers: `cron/ticker_heartbeat` and `cron/ticker_last_success` mtimes update every tick (minutes old = scheduler alive). `cron/cron.db` exists but is an empty stub — don't query it.

## Key Tables

### `sessions` — One row per conversation
| Column | Type | Notes |
|--------|------|-------|
| `id` | TEXT | UUID primary key |
| `title` | TEXT | Human-readable session name |
| `source` | TEXT | Platform: `cli`, `cron`, `telegram`, `discord`, `subagent`, `desktop`, `api_server`, `tui`, `tool` |
| `model` | TEXT | Model name (e.g. `deepseek-v4-flash`) |
| `billing_provider` | TEXT | Provider (e.g. `opencode-go`) |
| `input_tokens` | INTEGER | Total input tokens |
| `output_tokens` | INTEGER | Total output tokens |
| `cache_read_tokens` | INTEGER | Context cache read |
| `cache_write_tokens` | INTEGER | Context cache write |
| `reasoning_tokens` | INTEGER | Reasoning tokens |
| `estimated_cost_usd` | REAL | Cost estimate (model-priced) |
| `message_count` | INTEGER | Messages in session |
| `tool_call_count` | INTEGER | Tool invocations |
| `api_call_count` | INTEGER | LLM API calls |
| `started_at` | REAL | **Unix epoch float** — NOT ISO string |
| `ended_at` | REAL | Unix epoch float |
| `profile_name` | TEXT | Profile used |

### `session_model_usage` — Per-model breakdown per session
Multiple rows per session when model switches mid-conversation. Same columns as sessions for tokens/costs, plus `api_call_count`, `task` (e.g. `chat`, `vision`), `first_seen`, `last_seen`.

### `messages` — Individual messages
Has `token_count` per message, `role`, `tool_name`, `timestamp` (Unix epoch float).

## CRITICAL: Timestamps Are Unix Epoch Floats

ALL timestamps in state.db are **seconds since 1970-01-01 UTC** as floats (e.g. `1785146481.67`). They are NOT ISO-8601 strings.

### Querying (Python)
```python
from datetime import datetime, timezone, timedelta

# Filter by time range
cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).timestamp()
rows = conn.execute("SELECT * FROM sessions WHERE started_at >= ?", (cutoff,))

# Convert for display
dt = datetime.fromtimestamp(row["started_at"], tz=timezone.utc)
day_str = dt.strftime("%Y-%m-%d")
```

### Common Mistake
```python
# WRONG — timestamps are floats, not strings
cutoff = datetime.now().isoformat()
day = session["started_at"][:10]  # TypeError: float index
```

## Query Patterns

### Total cost by model (last N days)
```python
cutoff = (datetime.now(timezone.utc) - timedelta(days=30)).timestamp()
cur = conn.execute("""
    SELECT model, SUM(api_call_count) as calls,
           SUM(input_tokens), SUM(output_tokens),
           SUM(estimated_cost_usd) as cost
    FROM session_model_usage
    WHERE last_seen >= ?
    GROUP BY model ORDER BY cost DESC
""", (cutoff,))
```

### Sessions by platform
```python
cur = conn.execute("""
    SELECT source, COUNT(*) as cnt,
           SUM(estimated_cost_usd) as total_cost
    FROM sessions WHERE started_at >= ?
    GROUP BY source ORDER BY cnt DESC
""", (cutoff,))
```

### Daily aggregation (Python)
```python
from collections import defaultdict
daily = defaultdict(lambda: {"input": 0, "output": 0, "cost": 0.0, "sessions": 0})
for s in sessions:
    day = datetime.fromtimestamp(s["started_at"], tz=timezone.utc).strftime("%Y-%m-%d")
    daily[day]["input"] += s.get("input_tokens", 0) or 0
    daily[day]["output"] += s.get("output_tokens", 0) or 0
    daily[day]["cost"] += s.get("estimated_cost_usd", 0) or 0
    daily[day]["sessions"] += 1
```

## Mining a Past Discord Thread's Content (thread_id → full conversation)

state.db is also the archive of everything discussed in Discord threads. When a user says
"look over thread <id> where we discussed X", recover it without re-prompting:

```python
import sqlite3
db = sqlite3.connect('file:state.db?mode=ro', uri=True)
db.text_factory = lambda b: b.decode('utf-8', 'replace')
# thread_id == chat_id for Discord; sessions may have been compacted into multiple rows
sids = db.execute(
    "SELECT id, title, started_at, message_count FROM sessions WHERE thread_id=?",
    ('<discord-channel-id>',)).fetchall()
```

Then for each session, walk `messages` ordered by `timestamp ASC` and:
1. **User messages first** — they carry the actual asks (`WHERE session_id=? AND role='user'`).
   Compaction markers appear as synthetic user rows; the real messages are the ones NOT prefixed
   with `[CONTEXT COMPACTION]` / `[Recent channel messages]`.
2. **CONTEXT COMPACTION rows are the semantic index.** Sessions with 40k+ rows have 100–160
   compaction summaries; each contains a `## Historical Task Snapshot`, `## Goal`, and
   `## Constraints & Preferences` that distill whole chunks of work. Scanning compactions is
   ~100x cheaper than reading every message and recovers decisions, offers, and pricing.
3. **Keyword-delta extraction:** for "what did we decide about X", grep compaction bodies for
   the terms (e.g. `$497|stripe|offer|pricing`) and print the matching summaries; the
   `## Historical Task Snapshot` of the LAST compaction lists the most recent outstanding asks
   in chronological order — the best single answer to "where did we leave off?".
4. The `sessions` row's `display_name` gives the channel (`Automation Team / #revenue / Website
   Landlord`) and `chat_id`/`thread_id` are identical for Discord, so lookups by either work.

Timestamp columns are Unix epoch floats (see Pitfalls); `message_count` on sessions tells you
which of multiple sessions in one thread is the long one. This technique was used to reconstruct
the full website-sales offer structure (pricing tiers, payment→launch automation, drip schedule)
from thread `<discord-channel-id>` without reading 45k raw messages.

## Dashboard Pattern

A working reference implementation exists at `~/AppData/Local/hermes/scripts/usage_dashboard.py`.

### Architecture
- Self-contained Python (stdlib only, plus Chart.js loaded from CDN in HTML)
- Opens state.db in read-only mode: `sqlite3.connect(f"file:{STATE_DB}?mode=ro", uri=True)`
- Generates both **text summary** (stdout) and **HTML dashboard** (with Chart.js charts)
- Dark theme matching GitHub's color scheme

### Charts (10 total)
1. Daily token usage (stacked bar: input, output, cache read, cache write, reasoning)
2. Daily sessions (line)
3. Daily cost (bar)
4. Cost by model (doughnut)
5. API calls by model (bar)
6. Sessions by platform (polar area)
7. Hourly activity (bar)
8. Session cost distribution (pie)
9. Averages: messages, tool calls, tokens per session
10. Top sessions by cost (table)

### Output
- HTML: `~/Documents/github/hermes-config/dashboard/report.html`
- Cron: daily at 9:00 UTC, no_agent mode, job id `usage_dashboard` in `cron/jobs.json`

## Cron Job Integration for Analytics Scripts

When adding script-based (no_agent) analytics cron jobs:

1. **Via CLI:** `hermes cron create --no-agent --script my_script.py --schedule "0 9 * * *"`
2. **Directly in jobs.json:** Edit `~/AppData/Local/hermes/cron/jobs.json`:
   ```json
   {"id": "my_job", "name": "...", "script": "my_script.py",
    "schedule": "0 9 * * *", "no_agent": true, "enabled": true, "deliver": "discord"}
   ```

Note: `hermes cron list` may show "No scheduled jobs" while `cron/jobs.json` has entries if jobs were created outside the CLI workflow. The scheduler reads jobs.json directly.

## Pitfalls

- **Timestamp format**: Always use `.timestamp()` for cutoff and `fromtimestamp()` for display. Never `.isoformat()` or string slicing.
- **Large DB**: state.db can be 1-4GB. Full table scans on sessions table are fast (indexed by started_at), but aggregate queries should use time-range filters.
- **Read-only connection**: Use `?mode=ro` URI parameter to prevent accidental writes.
- **Null safety**: Token/cost columns can be NULL (not just 0). Always use `s.get("col", 0) or 0` in aggregations.
- **Daily bucketing**: Use `datetime.fromtimestamp(ts, tz=timezone.utc)` — sessions from cron may span UTC day boundaries.
- **Cost data**: Most costs are `estimated` (model-priced) rather than `actual`. The `cost_status` column distinguishes them.
