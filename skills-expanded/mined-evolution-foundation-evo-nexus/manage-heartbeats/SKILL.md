---
name: manage-heartbeats
description: "List, enable, disable, or manually trigger heartbeats (proactive agents). Shows last 10 runs with status and cost. Use when the user says 'list heartbeats', 'show active heartbeats', 'enable atlas-4h', 'disable zara-2h', 'run atlas heartbeat now', 'which heartbeats are running', or wants visibility into proactive agent state."
---

# Manage Heartbeats

> **Auth note:** Use `from dashboard.backend.sdk_client import evo` — auto-handles URL + auth, no Bearer token needed in code.

Inspect and control existing heartbeats — list them, enable/disable, trigger manual runs, review run history.

## When to use

Use this skill when the user wants to:
- See which heartbeats exist and their status
- Enable a heartbeat they set up but left disabled
- Disable a heartbeat that's costing too much or misbehaving
- Manually trigger a run (outside the normal interval)
- Review recent runs and decide if the heartbeat is working

Don't use this to create new heartbeats — use `/create-heartbeat`.

## Step 1: List all heartbeats

```python
from dashboard.backend.sdk_client import evo
heartbeats = evo.get("/api/heartbeats")
```

Response shape per heartbeat: `id`, `agent`, `interval_seconds`, `enabled`, `last_run_at`, `last_run_status`, `last_run_cost_usd`, `next_trigger_at`.

Present to user as a table:
- ID
- Agent
- Status (enabled / disabled)
- Interval (human format: "every 4h")
- Last run (time + status)
- Cost 7d (sum of `cost_usd` in last 7 days)

## Step 2: Detailed view (one heartbeat)

```python
from dashboard.backend.sdk_client import evo
hb = evo.get(f"/api/heartbeats/{hb_id}")
```

Includes last 10 runs with full fields: `started_at`, `ended_at`, `duration_ms`, `tokens_in`, `tokens_out`, `cost_usd`, `status`, `prompt_preview`, `error`.

Show the user the latest 3 runs, summarize patterns (always-skip / always-act / mixed).

## Step 3: Enable / disable

```python
from dashboard.backend.sdk_client import evo

# Enable
evo.patch(f"/api/heartbeats/{hb_id}", {"enabled": True})

# Disable (preserves data, just stops the dispatcher from scheduling)
evo.patch(f"/api/heartbeats/{hb_id}", {"enabled": False})
```

Warn the user:
- Enable doesn't run immediately — next trigger fires at the top of the next interval.
- Disable doesn't cancel a currently-running execution.

## Step 4: Run Now (manual trigger)

```python
from dashboard.backend.sdk_client import evo
result = evo.post(f"/api/heartbeats/{hb_id}/run")
```

Response `{"run_id": "...", "status": "queued"}` within ~500ms. Execution happens async.

Tell the user:
- Run logs appear in `workspace/ADWs/logs/heartbeats/<id>-<date>.jsonl` in real time.
- Or poll `GET /api/heartbeats/<id>` to see `last_run_status` flip from `running` → `success` / `fail` / `timeout`.

## Step 5: Paginated run history

```python
from dashboard.backend.sdk_client import evo
runs = evo.get(f"/api/heartbeats/{hb_id}/runs", params={"limit": 50})
```

Useful to audit a heartbeat that was misbehaving historically. Filter by:
- `?status=fail` — only failures
- `?status=timeout` — only timeouts
- `?from=YYYY-MM-DD&to=YYYY-MM-DD` — date range

## Step 6: Delete (rare)

Only if truly obsolete:

```python
from dashboard.backend.sdk_client import evo

# Gracefully — returns 409 if currently running
evo.delete(f"/api/heartbeats/{hb_id}")

# Force-kill currently-running
evo.delete(f"/api/heartbeats/{hb_id}", params={"force": "true"})
```

Confirm with user before forcing. Disable first, then delete once runs stop.

## Notes

- UI equivalent: `/scheduler` → Heartbeats tab. The skill is useful for scripted management or when Davidson prefers CLI.
- Cost visibility: `/costs` shows heartbeat cost per agent alongside routine costs.

Related: `.claude/rules/heartbeats.md`, `/create-heartbeat`.
