---
name: shutdown
description: Shut down the clawback proxy stack. By default stops ONLY the detached proxy started via run_monitor.sh --detach (graceful SIGTERM, then SIGKILL after ~5s) and removes its pidfile, letting the monitor go quiet — interactive `clawback claude` sessions are left running on purpose. Pass --sessions for a full teardown that also SIGTERMs every clawback claude wrapper, listing each before signaling. Use to cleanly stop the proxy, or to tear the whole stack down.
---

# clawback shutdown

Run `.skills/shutdown/scripts/shutdown.sh` from the project root.

```bash
.skills/shutdown/scripts/shutdown.sh              # stop the proxy + let the monitor go quiet
.skills/shutdown/scripts/shutdown.sh --sessions   # also SIGTERM clawback claude sessions
```

## Default: proxy + monitor only

With no flags this is identical to `run_monitor.sh --stop`: it stops the
detached proxy via its pidfile (SIGTERM first so it flushes state and closes
its logger, escalating to SIGKILL only if it does not exit within ~5s) and
removes the pidfile. A foreground `--attach` follower then prints the
synthetic "process exited" line and can be Ctrl-C'd; an agent's Monitor tool
simply stops seeing new lines.

## Why interactive sessions are left alone by default

Under probe-then-decide, `clawback claude` sessions ATTACH to an
already-listening proxy rather than spawning their own, so stopping the proxy
already cuts their upstream. But the session processes — and any unsaved
in-flight edit inside Claude Code — are yours to end deliberately, not
something this script should kill out from under you. This is the
soft-default (stop the proxy) plus an explicit escape knob (`--sessions`),
not a hard teardown.

## `--sessions`: full teardown

Adds a pass that sends SIGTERM to every `clawback claude` wrapper process. It
lists each match (pid + full command) before signaling, so nothing dies
silently. Specifics:

- The match is `pgrep -f 'clawback claude'`, which hits only the wrappers —
  the bare proxy is `node …/bin/clawback.js` (no "claude"), and neither this
  script nor `run_monitor.sh` contains the phrase.
- The spawned `claude` CLI child is NOT signaled; if it lingers after its
  wrapper exits, end it yourself.

## Options

`--log-file PATH` / `--pid-file PATH` are forwarded to `run_monitor.sh
--stop` so a non-default proxy can be targeted. To bring the proxy back, use
the [restart](../restart/SKILL.md) skill (or `run_monitor.sh --detach`).
