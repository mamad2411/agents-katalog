---
name: runner-status
description: |
  Use this skill when the user asks about the Claude task runner's
  status, queue health, or what's currently running. Examples: "is
  the runner alive?", "what's in flight?", "/runner-status", "queue
  status", "what's the supervisor doing?". Replaces the older
  /queue-tend skill — same use case, new implementation. Surfaces:
  supervisor liveness, current state machine vertex, 5h + weekly
  utilization, pending count, in-flight count, awaiting-sidecar tasks,
  recent failures, parser drift state.
---

# /runner-status — task runner health snapshot

This skill is mechanical: it shells out to `claude-task-runner` plus
some `ps` / file-glob queries to gather state, then presents a
prioritized summary so the user sees the most-important condition
first.

## Single-command form

For a comprehensive, consistent snapshot in one shell call:

```bash
bash /home/bill/.claude/skills/runner-status/snapshot.sh --queue <CWD>
```

The bundled `snapshot.sh` produces a markdown block with: supervisor
process liveness (PID + etime + cmd), `supervisor.json` fields
(state / 5h / weekly / in_flight / since / scheduled_wakeup / drift),
state-file counts (a row for every task status, one for any status
the runner does not know, and one for files it could not read or
that name no status; the rows add up to the total), todo/
count, open-sidecar list (task_id + sequence + the outstanding
question ids), and a **per-account
state table** sourced from supervisor.json's v3 `accounts` map
(state, 5h/weekly util, paused, in-flight count, throttle target,
reset + wakeup times, last-capture timestamp). The target is the
most tasks dispatch lets the account run (below its
`max_concurrency`): the ADR-0022 ramp while `slowing_down`, 0 while
throttled, "—" when no decision has set one. Multi-account queues
see one row per configured `[[accounts]]` block; single-account
queues see a single `default` row that tracks the top-level fields.

The script's exit code says whether the report can be trusted:

- **2, no report:** the queue does not exist or has no `todo/`
  subdirectory, usually a mistyped `--queue` or a working directory
  that is not the queue. The reason and the path are on stderr. Tell
  the user which path was tried and ask for the queue's path. Never
  describe it as an idle or empty queue.
- **1, report printed:** the open sidecars could not be listed. The
  **Open sidecars** line reads "could not list" and gives the reason.
  Say the open sidecars are unknown, never "no open sidecars".
- **0:** every section of the report was gathered.

This is the **default invocation** when the user says
`/runner-status` or "queue status" — produces the same output shape
every time so snapshots can be compared across time.

The per-account table replaces an earlier `claude-task-runner usage
render` block that captured a fresh `/usage` reading for one account
per call. The supervisor's per-account snapshot is at most one
`poll_interval_s` old (typically 30-60s), shows every account, and
costs no API tokens — better default for status checks. Operators
who want a current `/usage` capture can still run
`claude-task-runner usage render` directly.

If the user wants a deeper investigation (e.g. focused on hung tasks
or recent failures), follow the prioritized triage flow below.

## Steps (priority-triage form)

1. **Run** `claude-task-runner supervisor status --queue <CWD> --json`
   to get the supervisor snapshot, alive flag, and counts. The user's
   working directory is the default queue; use `--queue <PATH>` if
   they referenced a different one.

2. **Parse** the JSON. Surface findings in this priority order
   (highest first — only show every line that is relevant):

   1. **Parser drift** — if `snapshot.last_drift_message` is non-empty
      OR `snapshot.state == "error_drift"`: this is critical. Print a
      red line with the message. Suggest the user run
      `claude-task-runner usage healthcheck` or invoke `/runner-usage`
      to investigate. Stop here unless the user wants more.

   2. **No usage reading** — if `snapshot.state == "no_reading"`, or
      any entry of `snapshot.accounts` has `state == "no_reading"`:
      that account takes no tasks until a clean `/usage` capture lands.
      Print each such account with its `last_reading_at` ("never" when
      null) in yellow. Every account starts there after a supervisor
      start and leaves within one capture cycle (one poll per account),
      so only one that persists is a problem; point the user at the
      runbook section "An account stays in `no_reading`".

   3. **Weekly cap** — if `snapshot.state == "throttled_weekly"`:
      print "Weekly utilization NN% > target (throttled)" in yellow.
      The trace-following rule (ADR-0022) means the supervisor will
      auto-resume when the curve catches up; surface
      `snapshot.scheduled_wakeup_at` if present.

   4. **5h throttle** — if `snapshot.state in ("throttled_5h",
      "slowing_down")`: print 5h utilization + state. For each
      `slowing_down` account, also give its target from the
      per-account table ("personal slowing down, target 2").

   5. **Awaiting sidecars** — run
      `claude-task-runner queue states --status awaiting_sidecar
      --queue <CWD> --json` and report count + task IDs. Suggest
      `/runner-answer-sidecar` if any.

      Report the **question** count alongside the request count: sidecars
      are open per question (ADR-0031), so one request can owe four
      answers, and a request whose response answered only some of its
      questions is still open. `sidecar list --json` carries both as
      `n_open` and `n_outstanding_questions`. Never report "0 open
      sidecars" off the request count alone.

   6. **Hung tasks** — run with `--status possibly_hung`. Report each.

   7. **Recent failures** — `--status failed` and
      `--status failed_circuit_breaker`. Report counts; if non-zero,
      offer the task IDs.

   8. **Deferred tasks** — run `claude-task-runner queue states
      --status deferred --queue <CWD> --json` and report the count,
      grouped by how each state's `deferred_reason` starts:

      - `readiness hold:` — waiting on an unmet readiness requirement,
        such as a file or a sidecar response (ADR-0030). The supervisor
        checks it every tick and un-parks the task the first tick after
        the requirement is met. Give the count and offer the task IDs.
      - `invalid effort:` — the task's `(model, effort)` pair is not in
        `[effort_levels]` (ADR-0010). It stays parked until the task
        YAML is fixed, or the pair is added to the TOML and the
        supervisor gets SIGHUP. This needs the operator: list each task
        with its reason.
      - `pre-dispatch hook deferred (exit 1)` — the queue's pre-dispatch
        hook asked to wait. The hook runs again once the task's
        `next_eligible_at` passes, which is `deferral_recheck_cooldown_s`
        in `[failure_classifier]` (900 s by default) after the deferral.
        Of the runner's own deferrals, only these set
        `next_eligible_at`. Give the count and the earliest
        `next_eligible_at`.
      - Anything else was written by hand or by another tool. The
        reason is only a label and does not hold the task. Once its
        `next_eligible_at` passes, or at the next tick if it has none,
        the task can be dispatched again. If a gate holds it then, the
        gate's own reason replaces the hand-written one. List each task
        with its reason and `next_eligible_at`.

      A row with an `error` field is a state file that could not be
      parsed. `queue states` lists those whatever `--status` asks for,
      so report them separately, not as deferred.

   9. **Healthy summary** — if none of the above, one terse line:
      "Supervisor (state) · 5h NN% · weekly NN% · pending K ·
      in-flight M".

3. **Don't auto-fix anything.** This skill is read-only. If the user
   wants action (resume a failed task, answer a sidecar, restart the
   supervisor), name the right next skill / command but wait for
   confirmation.

## Things this skill does NOT do

- Doesn't restart the supervisor. (User can do that with
  `claude-task-runner supervisor start`, or rely on the
  watchdog if installed.)
- Doesn't dispatch new tasks.
- Doesn't modify state files.

## When the supervisor isn't alive

If `supervisor_alive == false`, that's not always bad — the watchdog
may be about to restart it. Mention liveness, mention whether a PID
file exists (stale vs missing), then suggest:

- `claude-task-runner watchdog tick` to trigger an immediate watchdog
  evaluation.
- `claude-task-runner watchdog queues` to check that a cron watchdog
  manages this queue. It manages one queue, the last line printed; if
  that is not this one, `claude-task-runner watchdog register --queue <queue>`
  makes it so, replacing the other. It warns on stderr about any other
  queue listed, which the watchdog ignores, and when the managed queue
  is no longer an existing directory, which every tick skips; drop that
  one with `claude-task-runner watchdog unregister --queue <path>`.
  `verdict=locked` in `~/.claude_task_runner/watchdog.log` means another
  supervisor holds the per-user lock, so no tick starts this queue's
  supervisor until that one exits.
- `claude-task-runner install` if no watchdog is configured.
- `claude-task-runner supervisor start` to manually start in
  foreground.
