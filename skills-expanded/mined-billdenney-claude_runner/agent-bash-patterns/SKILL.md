---
name: agent-bash-patterns
description: |
  How a task-running agent runs a long command (R, Python, builds,
  test suites) WITHOUT hanging itself or getting reaped by
  claude_task_runner. Core rule: never background a command in one
  Bash tool call and poll for its completion with pgrep/sleep in a
  later call — that race spins forever and the runner kills the
  worker. Use a synchronous `timeout`, a marker-file sentinel, or an
  `&&`-chain instead.

  Triggers: about to write `<cmd> &` then `until ! pgrep -f X; do
  sleep N; done`; "wait until the background command finishes"; "poll
  until the build / render / check is done"; running
  `buildModelDb()`, `devtools::check()`, `rmarkdown::render()`,
  `pytest`, `npm run build`, or any multi-second command split across
  two Bash tool calls. Universally good advice; especially
  load-bearing under claude_task_runner, where a spinning poll loop
  is a kill-on-sight antipattern.
---

# /agent-bash-patterns — run long commands without hanging or getting reaped

When a step needs a command that takes more than a few seconds
(`nlmixr2lib:::buildModelDb()`, `devtools::check()`, a vignette
render, `pytest`, a package install, `npm run build`), run it so the
result comes back in a **single** Bash tool call. Do **not** launch it
in the background in one call and "wait until it's done" in a later
call with a `pgrep` / `sleep` loop.

## The antipattern — explicitly forbidden

```bash
# Call 1 — start the command in the background:
Rscript -e 'devtools::load_all("."); nlmixr2lib:::buildModelDb()' &

# Call 2 (a later tool call) — "wait until done":
until ! pgrep -f "[b]uildModelDb\(\)" > /dev/null; do sleep 5; done
```

The bracket trick `[b]uildModelDb` (so `pgrep -f` can't match its own
argv) does **not** save you here — it only addresses self-matching,
not the race below.

## Why it breaks (race-and-spin)

The command usually finishes in seconds. If it completes **between**
call 1 and call 2 — the common case — call 2's `pgrep` matches
nothing and exits non-zero, the `until !` test is true on entry, the
body runs `sleep`, the next iteration also finds nothing, and the loop
spins **forever**. Your agent is now blocked on a Bash tool call whose
output will never return.

Under claude_task_runner this is the worst-case shape: `claude
--print` blocks on the bash subprocess; the dispatcher's monitor
thread keeps `dispatcher_alive_at` fresh (it's pumping an empty pipe),
but your agent emits no events so `last_heartbeat_at` goes stale. The
dual-heartbeat short-circuit reads "monitor fine + agent silent" and
the only backstop used to be the 4-hour duration cap. Real incidents
on nlmixr2lib_ingestion burned 2h–24h+ each before the cap fired:
`frompeople-919-dong_2014` (24h+), `frompeople-948-van_2015` (10h+),
`frompeople-937-hoglund_2015` (2h, $16.45), `frompeople-950-yu_2015`
(2h45m, $12.38).

The reaper now detects this signature generally — ANY live descendant
running a `while`/`until`/`for` loop around a `sleep` while the agent is
heartbeat-silent past `stuck_sleep_loop_kill_threshold_s` (default 10
min) and the monitor is still alive — and terminates the worker's
process group (SIGTERM → SIGKILL → verify) with stop_reason
`killed_stuck_sleep_loop` instead of waiting 4h. This covers the
`until ! pgrep …; do sleep N; done` form AND the
`while ! [ -e <marker> ]; do sleep N; done` background-marker wait (and
the broad fallback), but a killed task is still a failed task.
**Prevention beats detection: don't write the loop.**

## Use one of these instead

### Pattern A — synchronous with timeout (preferred for almost everything)

```bash
timeout 600 Rscript -e 'devtools::load_all("."); nlmixr2lib:::buildModelDb()'
```

Single Bash call; foreground; returns when done; exits non-zero on
timeout. No race, no spin. Use this unless the command **genuinely**
needs to overlap with other work — which a build/check/render almost
never does.

### Pattern B — marker-file sentinel (only when async is genuinely required)

```bash
# Call 1 — launch with a marker write at the very end:
rm -f .cmd-done
( timeout 600 Rscript -e '
    devtools::load_all(".")
    nlmixr2lib:::buildModelDb()
    writeLines("done", ".cmd-done")
' ) &

# Call 2 — wait for the marker file, with a FINITE retry cap:
for _ in $(seq 1 120); do
  [ -f .cmd-done ] && break
  sleep 5
done
test -f .cmd-done && echo OK || { echo TIMEOUT; exit 1; }
```

File existence is monotonic — once the marker exists it stays, so
there is no race with process exit. The `seq 1 120 * sleep 5 = 600 s`
ceiling guarantees the loop terminates even if the command dies before
writing the marker. Never poll on `pgrep`; poll on the artifact.

### Pattern C — foreground `&&`-chain (when later commands depend on completion)

```bash
timeout 600 Rscript -e 'devtools::load_all("."); nlmixr2lib:::buildModelDb()' \
  && ls -la data/modeldb.rda inst/modeldb.qs2 \
  && echo BUILD_DONE_AND_VERIFIED
```

Composes the command and its post-check in one tool call; the
post-check runs only if the command exits clean.

## The rule

**DO NOT** use `until ! pgrep -f X; do sleep N; done` — or any
sleep-and-pgrep poll loop — to wait for a command issued in an earlier
Bash tool call. If you want to do this, restructure to Pattern A
(synchronous), Pattern B (marker file), or Pattern C (chain). The
hazard is not specific to any one command; it applies to every
cross-tool-call wait.

## See also

- `agent-stop-and-ask` — the sibling rule for the *other* poll that
  burns a worker: never poll for a sidecar **response** file either.
  Write the request, exit, let the runner re-dispatch you.
- The runner-side reaper (`stuck_sleep_loop_zombie_killed` event,
  stop_reason `killed_stuck_sleep_loop`) is the safety net, not a
  substitute for writing the command correctly. It detects any stuck
  `while`/`until`/`for` + `sleep` loop by behaviour + time (silent past
  the kill threshold while the monitor is alive), so a *bounded* poll
  like Pattern B above — which self-terminates at its `seq … × sleep`
  ceiling and lets your agent resume emitting events — never trips it;
  only an unbounded loop that stays silent does.
