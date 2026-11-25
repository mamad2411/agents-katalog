---
name: pueue-job-orchestration
description: Manage long-running jobs and batch processing with pueue queue orchestration, CLI telemetry, and companion monitoring tools (noti, ntfy, mprocs,
allowed-tools: Read, Bash, Write
---

# Pueue Job Orchestration

> Universal CLI telemetry layer and job management — every command routed through pueue gets precise timing, exit code capture, full stdout/stderr logs, environment snapshots, and callback-on-completion.

> **Self-Evolving Skill**: This skill improves through use. If instructions are wrong, parameters drifted, or a workaround was needed — fix this file immediately, don't defer. Only update for real, reproducible issues.

## Overview

[Pueue](https://github.com/Nukesor/pueue) is a Rust CLI tool for managing shell command queues. It provides:

- **Daemon persistence** - Survives SSH disconnects, crashes, reboots
- **Disk-backed queue** - Auto-resumes after any failure
- **Group-based parallelism** - Control concurrent jobs per group
- **Easy failure recovery** - Restart failed jobs with one command
- **Full telemetry** - Timing, exit codes, stdout/stderr logs, env snapshots per task

## When to Route Through Pueue

| Operation                             | Route Through Pueue? | Why                                    |
| ------------------------------------- | -------------------- | -------------------------------------- |
| Any command >30 seconds               | **Always**           | Telemetry, persistence, log capture    |
| Batch operations (>3 items)           | **Always**           | Parallelism control, failure isolation |
| Build/test pipelines                  | **Recommended**      | `--after` DAGs, group monitoring       |
| Data processing                       | **Always**           | Checkpoint resume, state management    |
| Quick one-off commands (<5s)          | Optional             | Overhead is ~100ms, but you get logs   |
| Interactive commands (editors, REPLs) | **Never**            | Pueue can't handle stdin interaction   |

## When to Use This Skill

Use this skill when the user mentions:

| Trigger                      | Example                                    |
| ---------------------------- | ------------------------------------------ |
| Running tasks on gpu-host-1    | "Run this on gpu-host-1"                     |
| Long-running data processing | "Populate the cache for all symbols"       |
| Batch/parallel operations    | "Process these 70 jobs"                    |
| SSH remote execution         | "Execute this overnight on the GPU server" |
| Cache population             | "Fill the ClickHouse cache"                |
| Pueue features               | "Set up a callback", "delay this job"      |

## Quick Reference

### Check Status

```bash
# Local
pueue status

# Remote (gpu-host-1)
ssh gpu-host-1 "~/.local/bin/pueue status"
```

### Queue a Job

```bash
# Local (with working directory)
pueue add -w ~/project -- python long_running_script.py

# Local (simple)
pueue add -- python long_running_script.py

# Remote (gpu-host-1)
ssh gpu-host-1 "~/.local/bin/pueue add -w ~/project -- uv run python script.py"

# With group (for parallelism control)
pueue add --group p1 --label "BTCUSDT@1000" -w ~/project -- python populate.py --symbol BTCUSDT
```

### Monitor Jobs

```bash
pueue follow <id>         # Watch job output in real-time
pueue log <id>            # View completed job output
pueue log <id> --full     # Full output (not truncated)
```

### Manage Jobs

```bash
pueue restart <id>         # ⚠ Creates NEW task (see warning below)
pueue restart --in-place <id>  # Restarts task in-place (no new ID)
pueue restart --all-failed # ⚠ Restarts ALL failed across ALL groups
pueue kill <id>            # Kill running job
pueue clean                # Remove completed jobs from list
pueue reset                # Clear all jobs (use with caution)
```

**CRITICAL WARNING — `pueue restart` semantics**:

`pueue restart <id>` does **NOT** restart the task in-place. It creates a **brand new task** with a new ID, copying the command from the original. The original stays as Done/Failed. This causes exponential task growth when used in loops or by autonomous agents. In a 2026-03-04 incident, agents calling `pueue restart` on failed tasks grew 60 jobs to ~12,800.

- **Use `--in-place`** if you truly need to restart: `pueue restart --in-place <id>`
- **Verify before restart**: Read `pueue log <id>` to check if the failure is persistent (missing data, bad args) — retrying will never help
- **Never use `--all-failed`** without `--group` filter — it restarts every failed task across ALL groups

## Host Configuration

| Host          | Location                  | GPU         | Parallelism Groups              |
| ------------- | ------------------------- | ----------- | ------------------------------- |
| gpu-host-1      | `~/.local/bin/pueue`      | RTX 4090    | p1 (16), p2 (2), p3 (3), p4 (1) |
| gpu-host-2   | `~/.local/bin/pueue`      | RTX 2080 Ti | p1 (8), p2 (2)                  |
| Local (macOS) | `/opt/homebrew/bin/pueue` | N/A         | default                         |

## Core Workflows

### 1. Queue Single Remote Job

```bash
# Step 1: Verify daemon is running
ssh gpu-host-1 "~/.local/bin/pueue status"

# Step 2: Queue the job
ssh gpu-host-1 "~/.local/bin/pueue add --label 'my-job' -- cd ~/project && uv run python script.py"

# Step 3: Monitor progress
ssh gpu-host-1 "~/.local/bin/pueue follow <id>"
```

### 2. Batch Job Submission (Multiple Symbols)

For rangebar cache population or similar batch operations:

```bash
# Use the pueue-populate.sh script
ssh gpu-host-1 "cd ~/rangebar-py && ./scripts/pueue-populate.sh setup"   # One-time
ssh gpu-host-1 "cd ~/rangebar-py && ./scripts/pueue-populate.sh phase1"  # Queue Phase 1
ssh gpu-host-1 "cd ~/rangebar-py && ./scripts/pueue-populate.sh status"  # Check progress
```

### 3. Configure Parallelism Groups

```bash
# Create groups with different parallelism limits
pueue group add fast      # Create 'fast' group
pueue parallel 4 --group fast  # Allow 4 parallel jobs

pueue group add slow
pueue parallel 1 --group slow  # Sequential execution

# Queue jobs to specific groups
pueue add --group fast -- echo "fast job"
pueue add --group slow -- echo "slow job"
```

### 4. Handle Failed Jobs

```bash
# Check what failed
pueue status | grep Failed

# View error output FIRST (distinguish transient vs persistent)
pueue log <id>

# Restart specific job IN-PLACE (no new task created)
pueue restart --in-place <id>

# ⚠ NEVER blindly restart all failed — classify failures first
# pueue restart --all-failed  # DANGEROUS: no group filter, creates duplicates
```

**Failure classification before restart**: Exit code 1 (app error) may be persistent (missing data, bad args — will never succeed). Exit code 137 (OOM) or 143 (SIGTERM) may be transient. Always read `pueue log` before restarting.

## Troubleshooting

| Issue                      | Cause                    | Solution                                            |
| -------------------------- | ------------------------ | --------------------------------------------------- |
| `pueue: command not found` | Not in PATH              | Use full path: `~/.local/bin/pueue`                 |
| `Connection refused`       | Daemon not running       | Start with `pueued -d`                              |
| Jobs stuck in Queued       | Group paused or at limit | Check `pueue status`, `pueue start`                 |
| SSH disconnect kills jobs  | Not using Pueue          | Queue via Pueue instead of direct SSH               |
| Job fails immediately      | Wrong working directory  | Use `pueue add -w /path` or `cd /path && pueue add` |

## Priority Scheduling (`--priority`)

Higher priority number = runs first when a queue slot opens:

```bash
# Urgent validation (runs before queued lower-priority jobs)
pueue add --priority 10 -- python validate_critical.py

# Normal compute (default priority is 0)
pueue add -- python train_model.py

# Low-priority background task
pueue add --priority -5 -- python cleanup_logs.py
```

Priority only affects **queued** jobs waiting for an open slot. Running jobs are not preempted.

## Per-Task Environment Override (`pueue env`)

Inject or override environment variables on **stashed or queued** tasks:

```bash
# Create a stashed job
JOB_ID=$(pueue add --stashed --print-task-id -- python train.py)

# Set environment variables (NOTE: separate args, NOT KEY=VALUE)
pueue env set "$JOB_ID" BATCH_SIZE 64
pueue env set "$JOB_ID" LEARNING_RATE 0.001

# Enqueue when ready
pueue enqueue "$JOB_ID"
```

**Syntax**: `pueue env set <id> KEY VALUE` -- the key and value are separate positional arguments.

**Constraint**: Only works on stashed/queued tasks. Cannot modify environment of running tasks.

**Relationship to mise.toml `[env]`**: mise `[env]` remains the SSoT for default environment. Use `pueue env set` only for one-off overrides (e.g., hyperparameter sweeps) without modifying config files.

## Blocking Wait (`pueue wait`)

Block until tasks complete -- simpler than polling loops for scripts:

```bash
# Wait for specific task
pueue wait 42

# Wait for all tasks in a group
pueue wait --group mygroup

# Wait for ALL tasks across all groups
pueue wait --all

# Wait quietly (no progress output)
pueue wait 42 --quiet

# Wait for tasks to reach a specific status
pueue wait --status queued
```

### Script Integration Pattern

```bash
# Queue -> wait -> process results
TASK_ID=$(pueue add --print-task-id -- python etl_pipeline.py)
pueue wait "$TASK_ID" --quiet
EXIT_CODE=$(pueue status --json | jq -r ".tasks[\"$TASK_ID\"].status.Done.result" 2>/dev/null)
if [ "$EXIT_CODE" = "Success" ]; then
    echo "Pipeline succeeded"
    pueue log "$TASK_ID" --full
else
    echo "Pipeline failed"
    pueue log "$TASK_ID" --full >&2
fi
```

---

## Companion CLI Tools (gpu-host-1)

Four lightweight CLI tools complement pueue for monitoring and notifications. All installed on gpu-host-1 at `/usr/local/bin/` (noti, mprocs) or via apt (ntfy, task-spooler).

### noti — Wrap Any Command with Telegram Notification

Best for one-off "notify me when this finishes" workflows. Native Telegram support.

```bash
# Wrap any command — sends Telegram when it finishes
noti -g mise run kintsugi:catchup

# With execution time in message
noti -g -e python long_script.py

# Custom title/message
noti -g -t "Deploy done" -m "gpu-host-1 updated" mise run deploy:gpu-host-1
```

**Config**: `~/.config/noti/noti.yaml` + env vars `NOTI_TELEGRAM_TOKEN`, `NOTI_TELEGRAM_CHAT_ID`, `NOTI_DEFAULT=telegram` in `~/.bashrc`.

### ntfy — Push Notifications from Scripts/Callbacks

Best for programmatic notifications from scripts, pueue callbacks, or curl one-liners.

```bash
# One-liner from any script
ntfy pub --title "Backfill done" odb-alerts "BTCUSDT@500 complete"

# With priority and tags
ntfy pub --priority high --tags "warning" odb-alerts "Job failed"

# curl variant (works anywhere, no binary needed)
curl -d "Backup finished" ntfy.sh/my-topic

# Subscribe to topic (poll mode)
ntfy sub --poll odb-alerts
```

**Pueue callback integration** — add to `~/.config/pueue/pueue.yml`:

```yaml
callback: 'ntfy pub --title "pueue: {{label}}" --tags "{{status}}" odb-alerts "Task #{{id}} {{status}} ({{command}})"'
```

### mprocs — Multi-Process TUI

Best for interactive SSH sessions watching multiple processes side-by-side.

```bash
# Watch multiple pueue jobs in split panes
mprocs "pueue follow 3" "pueue follow 7" "pueue follow 8"

# Monitor services
mprocs "journalctl -fu opendeviationbar-sidecar" "journalctl -fu opendeviationbar-kintsugi"
```

Requires interactive TTY (SSH directly, not via scripts).

### task-spooler (tsp) — Simplest Job Queue

Best for quick ad-hoc sequential/parallel tasks without pueue group setup.

```bash
# Queue tasks (default: 1 parallel)
tsp python train.py
tsp python validate.py

# Set parallel slots
tsp -S 3

# List queue
tsp -l

# View job output
tsp -c 0

# Combine with noti
tsp bash -c 'python train.py && noti -g -m "training done"'
```

### Tool Selection Guide

```
Need to...
├── Get notified when a command finishes? → noti -g <command>
├── Send notification from a script/callback? → ntfy pub topic "msg"
├── Watch multiple logs/processes live? → mprocs "cmd1" "cmd2"
├── Quick sequential queue (no groups needed)? → tsp <command>
└── Persistent queue with groups, priorities? → pueue add <command>
```

---

## Deep-Dive References

| Topic                                                                                                 | Reference                                                              |
| ----------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------------- |
| Installation (macOS, Linux, systemd, launchd)                                                         | [Installation Guide](./references/installation-guide.md)               |
| Production lessons: `--after` chaining, forensic audit, per-year parallelization, pipeline monitoring | [Production Lessons](./references/production-lessons.md)               |
| State bloat prevention, bulk xargs -P submission, two-tier architecture (300K+ jobs), crash recovery  | [State Management & Bulk Submission](./references/state-management.md) |
| ClickHouse thread tuning, parallelism sizing formula, live tuning                                     | [ClickHouse Tuning](./references/clickhouse-tuning.md)                 |
| Callback hooks, template variables, delayed scheduling (`--delay`)                                    | [Callbacks & Scheduling](./references/callbacks-and-scheduling.md)     |
| python-dotenv secrets pattern, rangebar-py integration                                                | [Environment & Secrets](./references/environment-secrets.md)           |
| Claude Code integration, synchronous wrapper, telemetry queries                                       | [Claude Code Integration](./references/claude-code-integration.md)     |
| All `pueue.yml` settings (shared, client, daemon, profiles)                                           | [Pueue Config Reference](./references/pueue-config-reference.md)       |

---

## Pueue vs Temporal: When to Use Which

For structured, repeatable workflows needing durability and dedup, consider [Temporal](https://temporal.io/) (`pip install temporalio`, `brew install temporal`):

| Dimension        | Pueue                                  | Temporal                                                  |
| ---------------- | -------------------------------------- | --------------------------------------------------------- |
| **Best for**     | Ad-hoc shell commands, SSH remote jobs | Structured, repeatable workflows                          |
| **Setup**        | Single binary, zero infra              | Server + database (dev: `temporal server start-dev`)      |
| **Dedup**        | None — `restart` creates new tasks     | Workflow ID uniqueness (built-in)                         |
| **Retry policy** | None — manual or external agent        | Per-activity: max attempts, backoff, non-retryable errors |
| **Parallelism**  | `pueue parallel N --group G`           | `max_concurrent_activities=N` on worker                   |
| **Visibility**   | `pueue status` (text, scales poorly)   | Web UI with pagination, search, event history             |

**Recommendation**: Keep pueue for ad-hoc work. Migrate structured pipelines to Temporal when dedup and retry policies matter. See `devops-tools:distributed-job-safety` for invariants that apply to both.

---

## Related

- **Hook**: `itp-hooks/posttooluse-reminder.ts` - Reminds to use Pueue for detected long-running commands
- **Reference**: [Pueue GitHub](https://github.com/Nukesor/pueue)
- **Companion tools**: [noti](https://github.com/variadico/noti) (command wrapper → Telegram), [ntfy](https://github.com/binwiederhier/ntfy) (pub-sub notifications), [mprocs](https://github.com/pvolok/mprocs) (multi-process TUI), [task-spooler](https://vicerveza.homeunix.net/~viric/soft/ts/) (minimal job queue)
- **SOTA Alternative**: [Temporal](https://temporal.io/) — durable workflow orchestration with built-in dedup, retry, visibility
- **Issue**: [rangebar-py#77](https://github.com/terrylica/rangebar-py/issues/77) - Original implementation
- **Issue**: [rangebar-py#88](https://github.com/terrylica/rangebar-py/issues/88) - Production deployment lessons

## Post-Execution Reflection

After this skill completes, check before closing:

1. **Did the command succeed?** — If not, fix the instruction or error table that caused the failure.
2. **Did parameters or output change?** — If the underlying tool's interface drifted, update Usage examples and Parameters table to match.
3. **Was a workaround needed?** — If you had to improvise (different flags, extra steps), update this SKILL.md so the next invocation doesn't need the same workaround.

Only update if the issue is real and reproducible — not speculative.
