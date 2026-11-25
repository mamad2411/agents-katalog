---
name: restart
description: Restart the detached clawback proxy and reconnect its monitor. Stops the proxy previously started with run_monitor.sh --detach (if any), then starts a fresh one in the background; the run log is recreated in place so a tail -F follower (run_monitor.sh --attach, or an agent's Monitor tool) re-attaches automatically. Honors the same --log-file/--pid-file options and `--` passthrough as run_monitor.sh. Use after a config or code change to cycle the proxy without disrupting the monitor. Pass --watch to keep restarting automatically whenever a source file under src/ or bin/ changes.
---

# clawback restart

Run `.skills/restart/scripts/restart.sh` from the project root. It is exactly
`run_monitor.sh --stop` followed by `run_monitor.sh --detach`: it stops the
currently detached proxy (graceful SIGTERM, then SIGKILL after ~5s) and
starts a fresh one in the background, printing the new PID and log path.

```bash
.skills/restart/scripts/restart.sh                              # restart with current config
.skills/restart/scripts/restart.sh -- --port 8090 --log-level debug
.skills/restart/scripts/restart.sh --log-file data/other.log    # target a non-default log/pidfile
```

## Watch mode (`--watch`)

`.skills/restart/scripts/restart.sh --watch` restarts once now, then keeps restarting
automatically whenever a source file under `src/` or `bin/` changes — handy
when another `clawback claude` session is editing the code and you want the
proxy to pick it up hands-free.

```bash
.skills/restart/scripts/restart.sh --watch                      # auto-restart on src/ + bin/ edits
.skills/restart/scripts/restart.sh --watch -- --port 8090       # passthrough is forwarded to every restart
```

It runs in the foreground and prints each restart as it happens. **Ctrl-C
stops watching but leaves the proxy running** (restarts are spawned in their
own session, so the signal can't reach them) — same survivability as a plain
`--detach`.

Mechanics, in case you need to reason about it:

- Only `src/` and `bin/` are watched, recursively. The proxy's own writes
  live under `data/`, which is deliberately **not** watched, so there is no
  restart loop.
- Watching is limited to `.js`/`.mjs`/`.cjs` files; editor swap/backup files
  (`.swp`, `~`, vim's `4913` probe) and `node_modules`/`.git` are ignored, so
  a single `:w` triggers exactly one restart.
- A burst of edits is debounced (300 ms) into one restart, and restarts are
  serialized: a change arriving mid-restart queues exactly one more once the
  current one finishes, so two restarts never race on the pidfile.
- Implemented by `.skills/restart/scripts/watch.mjs` (zero deps, built-in recursive
  `fs.watch`). It is a general debounced run-on-change runner — `restart.sh`
  just points it at `src/`+`bin/` with the restart command.

## Why the monitor survives a restart

`--detach` truncates and reuses the same log file (`data/clawback.run.log`
by default). A follower started with `tail -n +1 -F` re-opens the recreated
file on its own, so:

- a foreground `.skills/scripts/run_monitor.sh --attach` keeps streaming across the
  restart — no need to stop and relaunch it;
- an agent's Monitor tool watching the same path likewise keeps emitting,
  with a brief gap while the proxy is down.

## Effect on live sessions

Under clawback's probe-then-decide model, interactive `clawback claude`
sessions ATTACH to this proxy rather than running their own. A restart drops
their upstream for the ~1s the proxy is down: in-flight requests fail and
Claude Code retries, while session state is reloaded from the state file on
boot (look for `resumed N session(s)`), so the sessions continue afterward.
Restart when that brief blip is acceptable.

## Options & passthrough

`--log-file PATH` / `--pid-file PATH` are forwarded to BOTH phases, so the
stop targets the same proxy the detach replaces. Anything after `--` is
forwarded verbatim to the new `clawback` (the stop phase ignores it). See the
[monitor](../monitor/SKILL.md) skill for the full option set and the
highlighting/agent-usage notes that apply to the recreated log.

## Verify

```bash
.skills/scripts/run_monitor.sh --status     # should report RUNNING with the new pid
```
