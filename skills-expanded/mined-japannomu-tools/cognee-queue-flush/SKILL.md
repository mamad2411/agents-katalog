---
name: cognee-queue-flush
description: Process the Cognee remember queue accumulated by hooks. Use this skill on a schedule (loop / CronCreate) inside Claude Code to drain ~/.claude/cognee_pending_remembers.jsonl by calling mcp__cognee__remember on the existing MCP cognee server (no new process spawn). This avoids the Ladybug DB lock contention error (Could not set lock on file).
---

# cognee-queue-flush

Drain the Cognee remember queue accumulated by `auto_remember_*.py` hooks.

## Why this skill exists

Two `auto_remember_*.py` hooks (UserPromptSubmit / Stop) append entries to a queue file:

- Queue: `~/.claude/cognee_pending_remembers.jsonl`
- Each line: `{"timestamp": "...", "session_id": "...", "dataset_name": "...", "data": "..."}`

The hooks **only append to the queue**; they never call cognee. Calling cognee from a hook would either delay the AI turn (sync MCP call) or spawn a new cognee-mcp process, which trips the Ladybug DB lock contention error `Could not set lock on file`. So a separate batch processor is needed.

This skill is that batch processor. It runs **inside the current Claude Code session** (under loop / CronCreate scheduling), so it shares the existing MCP cognee server process — no new cognee-mcp is spawned, no lock contention occurs.

## When to invoke

| Method | Description |
|---|---|
| `/loop 5m cognee-queue-flush` | Repeat every 5 minutes during the current session |
| `CronCreate(...)` | Schedule periodic runs via cron expression |
| Manual `/cognee-queue-flush` | One-shot drain |

The skill terminates after one drain. The scheduler invokes it again on the next tick.

## What this skill does

When invoked, you (Claude) follow this procedure:

### Step 1: Read the queue file

Use the `Read` tool on `~/.claude/cognee_pending_remembers.jsonl`. If the file does not exist, the queue is empty — exit immediately.

### Step 2: Parse each line as JSON

Each non-empty line is a JSON object with keys `data` and `dataset_name`. Lines that fail to parse are malformed and should be removed from the queue (do not attempt to retry forever).

### Step 3: Process at most N entries per invocation

Determine the per-invocation cap **N**:

- Read environment variable `COGNEE_QUEUE_FLUSH_MAX_PER_RUN`.
- If unset or not a positive integer, use the default: **3**.

> **The default of 3 is conservative.** How many entries your machine can drain
> within one schedule interval depends entirely on **your environment** (CPU/GPU,
> VRAM, the LLM you chose, network latency for cloud LLMs). Run with the default
> first, observe how long one invocation takes (the skill reports timing in its
> summary), and **tune `COGNEE_QUEUE_FLUSH_MAX_PER_RUN` to match your machine**.
> The table below is just a rough starting point.

Take the first N entries from the queue (in order). Leave any remaining entries in the queue — they will be drained by the next scheduled invocation. This per-invocation cap exists because each `mcp__cognee__remember` call takes several seconds to tens of seconds (depending on the LLM and PC specs), and a single drain that exceeds the schedule interval (default 5 min) overlaps with the next firing.

**Rough starting points** (always tune to your own environment):

| Setup | Suggested N |
|---|---|
| Cloud LLM (Claude / OpenAI / Gemini) | 10 — 20 |
| Local Ollama, qwen2.5:14b on a discrete GPU (8GB+ VRAM) | 3 — 5 (default 3) |
| Local Ollama, qwen2.5:14b on CPU only | 1 — 2 |
| Local Ollama, smaller models (qwen2.5:7b etc) | 5 — 10 |

For each of the first N entries, call:

`mcp__cognee__remember(data=entry["data"], dataset_name=entry.get("dataset_name", "main_dataset"))`

This call uses the **existing MCP cognee session** — it does not spawn a new process.

Apply the 3-fold failure check:

1. **is_error check**: if the result has `is_error=True`, the call failed.
2. **Error text check**: if any `content[*].text` starts with `"Error:"`, the call failed (cognee-mcp upstream defect: it returns is_error=False even on failure).
3. **Exception check**: if the call raises an exception, it failed.

If all three checks pass, the call succeeded.

### Step 4: Update the queue and the failed-entries file

For the N entries you processed in Step 3:

- For each **successful** entry: remove it from the queue.
- For each **failed** entry: keep it in the queue AND append a copy to `~/.claude/cognee_failed_remembers.jsonl` for later review.

Entries beyond the first N (the not-yet-processed ones) stay in the queue untouched and will be picked up by the next invocation.

### Step 5: Write back

- Write the remaining queue entries (failures from this run + entries beyond the first N that you did not process) back to the queue file, preserving their original order.
- If the queue is empty, you may delete the file or leave it empty — both are fine.

### Step 6: Report

Report the result: `(succeeded_count, failed_count, remaining_in_queue)`. `remaining_in_queue` is the number of entries still in the queue file after Step 5 (failures + unprocessed). If `failed_count > 0`, mention that failed entries are saved in `~/.claude/cognee_failed_remembers.jsonl` for review. If `remaining_in_queue > 0` because of the per-invocation cap, mention that the next scheduled invocation will pick them up.

## Critical design constraints (no second cognee-mcp process)

- **DO NOT spawn a new `cognee-mcp` process** (e.g. via `fastmcp.StdioTransport` or `subprocess`). The Claude Code session already has a cognee-mcp server running; reuse it via `mcp__cognee__remember`.
- **DO NOT install a new MCP server with a different `claude mcp add` invocation**. The MCP cognee server is already registered.
- **DO NOT call cognee Python APIs directly from this skill**. They would also try to acquire the Ladybug DB lock and conflict with the running cognee-mcp.

## What this skill does NOT do

- It does not delete sample data or user data.
- It does not modify cognee configuration.
- It does not run `cognify` / `prune` / `improve`. Those are explicit user actions.

## Failure recovery

If failed entries pile up in `~/.claude/cognee_failed_remembers.jsonl`, the user should:

1. Inspect the file (`cat ~/.claude/cognee_failed_remembers.jsonl`).
2. Diagnose the root cause (Ollama down? Disk full? cognee-mcp crashed?).
3. Once resolved, manually copy entries back to the queue: `cat ~/.claude/cognee_failed_remembers.jsonl >> ~/.claude/cognee_pending_remembers.jsonl`
4. Trigger this skill again (e.g. `/cognee-queue-flush`).

## Related

- Hooks: `harness/hooks/auto_remember_completion.py`, `harness/hooks/auto_remember_user_message.py` (queue producers)
- Architecture rationale: see the v0.3.0 entry of `CHANGELOG.md`.
- Verification: this skill is expected to succeed even when a separate CLI script (e.g. `src/sample_src/load_sample.py`) is concurrently spawning its own `cognee-mcp` process — the spawning CLI script will fail with the Ladybug DB lock contention error (`Could not set lock on file`), but this skill, running inside the existing Claude Code session via the shared MCP cognee server, is unaffected.
