---
name: monitor
description: Run the clawback proxy and watch its log output for errors. Starts the bare proxy (honoring config layering), captures combined stdout+stderr to a log file, and follows it with warn/error/4xx/5xx lines highlighted. Supports foreground follow, background --detach (with --stop/--status), and --attach to tail an already-running proxy's log. Use when you want to launch clawback and monitor it for errors/regressions, or smoke-watch it after a change.
---

# clawback run + monitor

Run `.skills/scripts/run_monitor.sh` from the project root. It starts the bare
`clawback` proxy, captures its combined stdout+stderr to a log file, and
follows that log with error-ish lines highlighted.

Capturing both file descriptors (rather than passing `--log-file` to the
proxy) is deliberate: pre-logger startup failures — `EADDRINUSE`, a missing
TLS cert, an upstream self-loop — write to stderr before the logger exists,
so they would otherwise vanish. Here they land in the same log.

## Modes

```bash
.skills/scripts/run_monitor.sh                 # foreground: start proxy + follow logs; Ctrl-C stops both
.skills/scripts/run_monitor.sh --detach        # background: start proxy, print PID + log path, exit
.skills/scripts/run_monitor.sh --stop          # stop a --detach'd proxy (graceful SIGTERM, then SIGKILL)
.skills/scripts/run_monitor.sh --status        # is the --detach'd proxy alive?
.skills/scripts/run_monitor.sh --attach        # don't start anything; just follow an existing log file
```

Only one mode at a time; default is foreground follow.

## Options

- `--errors-only` — while following, surface only warn/error/4xx/5xx/failure
  lines (everything else is filtered out).
- `--log-file PATH` — log destination (default `data/clawback.run.log`).
- `--pid-file PATH` — pidfile for detach/stop/status (default
  `data/clawback.run.pid`).
- `--no-color` — disable ANSI highlighting (also honored: `NO_COLOR` env, and
  auto-off when stdout is not a TTY).
- `-h`, `--help` — show usage.

Anything after `--` is forwarded verbatim to `clawback`:

```bash
.skills/scripts/run_monitor.sh -- --port 8090 --log-level debug
.skills/scripts/run_monitor.sh --detach -- --passthrough        # baseline arm, backgrounded
```

## Highlighting

When stdout is a color-capable TTY, the follower colors:

- **red** — `[error]` lines, unhandled exceptions, `Error:` stack traces.
- **yellow** — `[warn]` lines.
- **magenta** — any `→ 4xx` / `→ 5xx` request/ping response.

A liveness watcher appends a synthetic red line if the proxy process exits on
its own, so a crash shows up in the follow stream instead of the log just
going quiet (BSD/macOS `tail` has no `--pid`).

## Agent usage

For an agent, `--detach` then tail the log path (e.g. with the Monitor tool,
filtering on `\[error\]|\[warn\]|→ [45][0-9][0-9]|failed`) is the cleanest
pattern — it doesn't block, and `--stop` cleans up afterward. `--detach`
refuses to start a second proxy if its pidfile points at a live one; a
separate proxy already holding the port surfaces as an `EADDRINUSE` failure
with the last log lines echoed.

## Notes

- The proxy binds per your config (`./CLAWBACK.md` here sets `host:
  0.0.0.0`, so it is LAN-reachable over HTTPS with the self-signed cert;
  mutating endpoints are `adminToken`-gated, GETs are open).
- Logs and the pidfile are created with `umask 077` (owner-only) — the proxy
  log can contain captured auth headers / upstream error bodies.
- `--stop` sends `SIGTERM` first so the proxy flushes state and closes its
  logger, escalating to `SIGKILL` only if it does not exit within ~5s.
