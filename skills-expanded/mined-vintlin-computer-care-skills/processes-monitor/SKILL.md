---
name: processes-monitor
description: Use when monitoring long-running local commands with heartbeat liveness checks — background jobs, builds, scripts, services, downloads, or batch automation that may hang, timeout, crash, or lose logs.
---

# Processes Monitor

## Overview

Monitor long-running work with explicit status files, heartbeats, logs, and timeouts. A PID alone proves a process exists; it does not prove progress.

## Sentinel Pattern

Create a monitor directory with:

| File | Purpose |
| --- | --- |
| `<name>.pid` | Process ID |
| `<name>.heartbeat` | Updated periodically while work progresses |
| `<name>.status` | `SUCCESS`, `FAILED`, `TIMEOUT`, or `HUNG` |
| `<name>.log` | Captured stdout/stderr |
| `<name>.result` | Optional structured output |

## Minimal Wrapper

```bash
#!/usr/bin/env bash
set -uo pipefail
name="${1:?name required}"
monitor_dir="${2:-/tmp/process-monitor}"
mkdir -p "$monitor_dir"
echo $$ > "$monitor_dir/$name.pid"

(while true; do touch "$monitor_dir/$name.heartbeat"; sleep 10; done) &
heartbeat_pid=$!
trap 'kill "$heartbeat_pid" 2>/dev/null' EXIT

if your_command >"$monitor_dir/$name.log" 2>&1; then
  echo SUCCESS > "$monitor_dir/$name.status"
else
  echo FAILED > "$monitor_dir/$name.status"
fi
```

Always write a final status — never leave monitor files in an ambiguous state. The `trap` ensures the heartbeat loop is cleaned up on exit.

## Monitor Logic

Check in a loop:

1. If `.status` exists, read it and stop.
2. If `.heartbeat` is stale beyond the threshold, treat as hung. Do not kill a process only because it is slow — compare heartbeat age, log output, and elapsed time before deciding.
3. If elapsed time exceeds the timeout, stop or escalate. Do not restart a failing process repeatedly without reading its log first.
4. Otherwise wait and check again. Avoid `tail -f | grep -m1` for log watching — it can hang on macOS due to buffering. Prefer polling the status file.

Recommended defaults:

| Setting | Value |
| --- | --- |
| heartbeat interval | 10 seconds |
| stale threshold | 60 seconds |
| poll interval | 10-15 seconds |
| max timeout | based on task, declared before start |
