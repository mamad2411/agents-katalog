---
name: watch-errors
description: Quiet operator watch for a detached clawback proxy — stream ONLY legitimate errors and never the benign flood. Wakes on [error]/[fatal] lines, crash signatures (uncaught/EADDRINUSE/ECONN*/Error:/self-loop), server-side 5xx that are NOT the transient 529, real (non-keep-alive) request failures, and a loud "PROXY DOWN" the instant the pid dies (then exits non-zero). Deliberately silences keep-alive ping failures (401 auth-stale / 404 retired-model / 429/529), real-request 429+529 (Claude Code auto-retries), and [info] no-route attach probes — all observed-benign and not actionable. Use when pointing an agent's Monitor tool at the live proxy and you want zero token burn on no-ops, only real errors. Prefer this over the broader `operate` skill when noise/cost matters.
---

# clawback watch-errors (quiet operator watch)

Run `.skills/watch-errors/scripts/watch_errors.sh` from the project root. It watches a proxy you
already started with the [monitor](../monitor/SKILL.md) skill
(`run_monitor.sh --detach`) and emits **one line per genuinely actionable
error** on stdout — and nothing during the constant benign churn.

```bash
.skills/watch-errors/scripts/watch_errors.sh                                   # defaults below
.skills/watch-errors/scripts/watch_errors.sh data/clawback.run.log data/clawback.run.pid
.skills/watch-errors/scripts/watch_errors.sh selftest                          # run the filter corpus; exit!=0 on regression
```

Defaults match `run_monitor.sh`:

- `LOG_FILE` = `data/clawback.run.log`
- `PID_FILE` = `data/clawback.run.pid`
- poll cadence: `WATCH_ERRORS_POLL_SEC` (default 5s)

## What wakes you (legitimate errors)

- **tier A (hard) — always**: any `[error]` / `[fatal]` line, unhandled/uncaught
  exceptions, `Error:` stack traces, bind/connection failures (`EADDRINUSE`,
  `ECONNREFUSED`, `ECONNRESET`, `ETIMEDOUT`, `ENOTFOUND`), `self-loop`, and the
  synthetic `PROXY DOWN`. A hard error wakes you **even if it also mentions a
  benign token** (e.g. `[error] keep-alive scheduler crashed: uncaught …`).
- **tier B (soft) — unless benign**: status-code / `failed` lines — i.e.
  server-side **5xx that are not 529** (500/502/503/504…) and any
  **non-keep-alive** request that 4xx/5xx'd for a reason outside the benign set
  below.
- **liveness**: a synthetic `[error] PROXY DOWN …` the moment the proxy pid
  stops responding — the most important error of all (the dev server is gone) —
  after which the watch **exits non-zero** so it ends deliberately instead of
  hanging silent.

## What it silences (benign, never actionable)

Every one of these was observed live as a repeating flood; none is worth a
wake-up (and each wake replays the whole agent context = pure token burn):

- **keep-alive ping failures** — `401` (auth-stale: the captured OAuth bearer
  rotated; the scheduler *pauses* until the next real request refreshes it),
  `404` (a session pinned to a now-retired model loops on `not_found`),
  `429`/`529` (transient). Keep-alive is cache-warming **only**; its failures
  never block real work.
- **real-request `429` (rate limit) and `529` (overloaded)** — Claude Code
  auto-retries these with backoff; you have no lever, so they are not
  actionable.
- **`[info]` attach probes** — `HEAD /<id> → 404 [no-route]` is normal
  probe-then-decide session negotiation.

**Deliberate non-goal:** a *sustained* transient outage (hundreds of `529`s in a
row = a real Anthropic outage) will **not** wake you. The filter is per-line and
stateless, so a transient code is dropped no matter how often it repeats — the
right trade to kill the noise. Add rate-based escalation if you ever need outage
alerts.

## Why a separate skill from `operate`?

[operate](../operate/SKILL.md) (`operator_watch.sh`) surfaces **every** `[warn]`
and **every** 4xx/5xx, plus rebind / runtime-mode info. That is the right tool
when you want to see *all* proxy activity. But against the live proxy it wakes an
agent every few minutes on keep-alive 401/404/529 and request 429/529 — benign
churn that costs a full context replay each time. `watch-errors` keeps the
liveness guarantee and the hard-error net while dropping that flood, so an
agent's Monitor stays silent until something is genuinely wrong.

## The filter is tested

The classifier is one awk program (single source of truth for live watching and
the test). `.skills/watch-errors/scripts/watch_errors.sh selftest` runs a corpus of **real** log
shapes captured live — 8 benign (must drop) + 7 legitimate (must wake),
including the tricky `[error] keep-alive … uncaught` (hard-wins) and a
real-request `404` with `[session=…]` (wakes) vs a keep-alive `404` (drops) — and
exits non-zero on any regression. Re-run it after editing the patterns.

## Agent usage (the quiet operator loop)

1. `.skills/scripts/run_monitor.sh --detach` — start the proxy (if not already up).
2. Point the **Monitor** tool at `.skills/watch-errors/scripts/watch_errors.sh` with
   `persistent: true`. Each emitted line becomes a notification — and during
   healthy operation there are none.
3. On a `PROXY DOWN` (or any hard error), read the tail of
   `data/clawback.run.log` for the cause, then bring it back with the
   [restart](../restart/SKILL.md) skill and re-arm the Monitor.

Stop the proxy with the [shutdown](../shutdown/SKILL.md) skill; the watch exits
on its own when the proxy is gone.

## Notes

- Logs/pidfile are owner-only (`umask 077`) — the proxy log can contain captured
  auth headers and upstream error bodies.
- `-F` re-opens the log across the truncate-and-recreate that
  `run_monitor.sh --detach` does on restart, so the watch survives a restart.
