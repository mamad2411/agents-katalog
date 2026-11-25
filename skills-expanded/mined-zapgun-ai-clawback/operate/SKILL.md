---
name: operate
description: Watch an already-detached clawback proxy as an event stream — surface only actionable log lines (error/warn/4xx/5xx/crash signatures, plus rebind and runtime-mode toggles) AND announce a loud "PROXY DOWN" line the instant the proxy pid dies. Fills the gap that run_monitor.sh --attach leaves: a bare tail goes SILENT on a crash (BSD tail has no --pid), so silence reads as healthy-idle. Use when acting as the operator agent keeping the server alive — point an agent's Monitor tool at it (persistent), react to PROXY DOWN by reading the log tail for the crash cause and restarting via the restart skill.
---

# clawback operate (operator watch)

Run `.skills/operate/scripts/operator_watch.sh` from the project root. It watches a proxy you
already started with the [monitor](../monitor/SKILL.md) skill
(`run_monitor.sh --detach`) and emits **one line per actionable event** on
stdout, staying quiet during healthy idle.

```bash
.skills/operate/scripts/operator_watch.sh                              # defaults below
.skills/operate/scripts/operator_watch.sh data/clawback.run.log data/clawback.run.pid
```

Defaults match `run_monitor.sh`:

- `LOG_FILE` = `data/clawback.run.log`
- `PID_FILE` = `data/clawback.run.pid`
- poll cadence: `OPERATOR_WATCH_POLL_SEC` (default 5s)

## What it emits

- log lines matching `[error]` / `[warn]` / `→ 4xx|5xx` / `failed` /
  `self-loop` / `EADDRINUSE` / `ECONN*` / `unhandled` / `Error:`
- two INFO signals an operator wants: `clawback listening` (a (re)bind) and
  `runtime mode toggled` (e.g. the baseline→armed flip after a fresh proxy's
  5-turn capture window, or any admin toggle)
- a synthetic `[error] PROXY DOWN …` line the moment the proxy pid stops
  responding — then it **exits non-zero** so the watch ends deliberately
  instead of hanging silent

## Why not just `run_monitor.sh --attach`?

`--attach` only tails the log. macOS/BSD `tail` has no `--pid`, so a crash
makes the log go quiet and an attached follower can't tell "dead" from
"idle". Only `run_monitor.sh`'s foreground `follow` mode has a liveness
watcher — but that mode starts its **own** proxy and would collide on the
port with one already detached. This script adds liveness to the
already-detached case without touching the port.

## Agent usage (the operator loop)

1. `.skills/scripts/run_monitor.sh --detach` — start the proxy.
2. Point the **Monitor** tool at `.skills/operate/scripts/operator_watch.sh` with
   `persistent: true`. Each emitted line becomes a notification.
3. On a `PROXY DOWN` (or a crash signature), read the tail of
   `data/clawback.run.log` to find the cause — that's the "pattern in the
   logs that needs fixing" — then bring it back with the
   [restart](../restart/SKILL.md) skill and re-arm the Monitor.

Stop the proxy with the [shutdown](../shutdown/SKILL.md) skill; the watch
exits on its own when the proxy is gone.
