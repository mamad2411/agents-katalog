---
name: runner-status
description: |
  Use this skill when the user asks about the Claude task runner's
  status, queue health, or what's currently running. Examples: "is
  the runner alive?", "what's in flight?", "/runner-status", "queue
  status", "what's the supervisor doing?". Replaces the older
  /queue-tend skill — same use case, new implementation. Leads with a
  plain-language explanation anyone can read, then the details:
  supervisor liveness, what each account is doing, the queue's
  concurrency ceiling, broken account settings files, 5h + weekly
  utilization, task counts, open questions, the last "no eligible
  tasks" report, recent failures, parser drift state.
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

The bundled `snapshot.sh` prints, first, **In plain words**, a summary a
non-specialist can read in ten seconds, as five short lines:

- **Supervisor**: running, not running, or running but no longer saving
  its state (stuck). Running means its PID is alive and `supervisor.json`,
  which it rewrites every tick, was saved within three
  `[usage].poll_interval_s` of the settings it was started with.
- **Accounts**: one line each: taking tasks (slots in use out of the slots
  it is allowed now), or not, and why (paused, its 5-hour allowance used
  up, using its weekly allowance faster than planned, waiting for its
  end-of-week window (an account with `early_pct = 0`), no recent usage
  reading, its usage could not be read, or a problem that stops it taking
  tasks at all until fixed, such as a runner-account.toml that does not
  load).
- **How many can run**: the concurrency ceiling (the most tasks the queue
  may run at once), where it comes from (the sum of the accounts' own
  `max_concurrency`, or a queue-wide `[concurrency].max_concurrency` that
  binds below it, and the warm-up cap while it applies), and how many run
  now with how much room is left.
- **Tasks**: what the supervisor's own selection says about every task in
  `todo/`: how many run, how many can start as soon as a slot is free
  (and how many of those were answered after asking), how many wait for
  your answer, a file, another task or a retry time, how many wait for a
  task that does not exist or cannot finish, how many the block list
  holds, how many look stuck or failed for good, how many finished.
- **Questions for you**: the open sidecar questions, and notices to
  acknowledge.

Then **Not normal right now**: one sentence per condition that needs the
operator, saying what it means and what to do (an account that cannot take
tasks until a problem is fixed, a paused account, an expired login or an unreadable usage page, a
binding queue-wide cap, tasks that look stuck, failed for good or cannot be
read, tasks whose `depends_on` names a task that does not exist (each with
the ids it is missing) or that cannot finish (itself, a loop of tasks
waiting on one another, a task stopped after repeated failures; each with
why), tasks whose worker could not be started, an
unwatched worker past its time limit while no supervisor runs to stop it,
or one that exited unrecorded, unreadable sidecar requests,
a supervisor that is down or stuck, an unreadable `supervisor.json` or
queue settings file, nothing running although tasks can start). And **For
your information**: routine conditions that resolve by themselves, with
when (an account throttled until a time, tasks waiting for the account
their session runs on, a worker still running that the supervisor does
not watch, the queue drained because every task is held). While the supervisor is not
running, the tasks and accounts it last recorded as running are given as
its last record, not as running now.
"Everything looks normal." when there is neither.

The facts come from the runner, not from re-reading its files:
`claude-task-runner account list --json` (each account's state, caps,
pause, settings-file error, `weekly_catch_up_at`, `weekly_window_opens_at`
and `usage_error`, and the
queue ceiling), `claude-task-runner queue holds --json` (the supervisor's
candidate selection run once, read-only, with the poll interval, the
parked workers, why each task waiting for a retry time was deferred, the
missing dependency ids of each task held `depends_on_missing`, and the
dependencies that cannot finish of each task held `depends_on_unmeetable`) and
`claude-task-runner sidecar list --json`. The script passes the live
supervisor's own `--config` to `account list` and `queue holds`
(`sidecar list` reads no settings), resolving a relative path against the
supervisor's working directory. When that directory cannot be read it
passes none, and the summary says the supervisor's settings are unknown.

`claude-task-runner account list --json` exits 1 both when an account
cannot take tasks (its runner-account.toml does not load, its config_dir
cannot hold one, or its linux_user needs sudo, which is not on PATH; the
listing shows it, in that row's `policy_error`) and when the queue TOML
cannot be read for now; output of
the form `{"ok": false, "error": ...}` is an error with nothing listed, and
exit 78 means the queue TOML's content is wrong. `queue holds --json` fails
the same way. The summary then says, once, that the queue settings file
cannot be read, with the error, and whether it may clear up (exit 1) or
needs fixing (78).

Of the tasks that can start, `queue holds --json` counts in
`eligible.can_start_now` those an account can take now, and in
`eligible.waiting_for_their_account` those held to the account their
session runs on, which cannot take them; such a task moves to any account
after `affinity_ttl_s` without running. "Nothing is running although N can
start" counts only the first.

Under **Details** come the sections the summary is built from, each opening
with a line saying what it shows and defining its terms:

- **Supervisor**: process liveness (PID + etime + command line).
- **supervisor.json**: state / 5h / weekly / in_flight / since /
  scheduled_wakeup / drift, and `last saved` (the file's modification
  time). `scheduled_wakeup` is the supervisor's next re-check, not when a
  throttled account resumes.
- **Accounts and concurrency**: each account's own limit, how many it is
  allowed now (0 while paused, throttled, without a reading, or unable to
  take tasks), in flight, paused, when a weekly-throttled account resumes,
  its settings file and any problem that stops it taking tasks; then the
  queue ceiling with its parts.
- **Per-account state**, from supervisor.json's `accounts` map: state,
  5h/weekly util (5h "not reported" for an account whose usage reading
  has no 5-hour window, ADR-0038), paused (read from the
  `account_paused/` markers, which `supervisor.json` trails by a tick),
  in-flight count, throttle target,
  reset + wakeup times, last-capture timestamp. The target is the most
  tasks dispatch lets the account run (below its `max_concurrency`): the
  ADR-0022 ramp while `slowing_down`, 0 while throttled, "—" when no
  decision has set one.
- **What holds the tasks**: `queue holds`' counts per category, why the
  tasks waiting for a retry time were deferred, the parked workers, every
  task held `depends_on_missing` with its missing dependency ids, and every
  task held `depends_on_unmeetable` with its dependencies that cannot
  finish and why.
- **Queue counts**: a row for every task status across every state file,
  finished tasks included, one for any status the runner does not know,
  and one for files it could not read or that name no status (the rows
  add up to the total), and the todo/ count.
- **Last idle report**: the newest `no eligible tasks:` or `eligible tasks
  available again:` line the running supervisor logged (its journal
  entries, or `<queue>/.claude_task_runner/supervisor.log` under cron, text
  or JSON log format), with its time. A line from before the supervisor
  started is shown as such; when neither log can be read it says so.
- **Open sidecars**: task_id + sequence + the outstanding question ids.

## How to reply

1. **Lead with the plain-language explanation.** Start from the script's
   **In plain words** block and say it in your own plain words: no jargon,
   and define any term you must use the first time it appears. Plain
   definitions that are accurate:
   - "in flight": running now;
   - "throttled": the supervisor has stopped starting new tasks on that
     account to keep its usage on plan, either because its 5-hour
     allowance is used up (it resumes when the 5-hour window resets) or
     because it is using its weekly allowance faster than planned (it
     resumes when its weekly use falls back under plan, which the summary
     dates), or because it is kept for the end of its week with
     `early_pct = 0` and its window has not opened yet (ADR-0041; the
     summary dates the opening);
   - "awaiting_sidecar": the task stopped to ask a question, and keeps
     this status until it runs again, so an awaiting_sidecar task may
     already be answered and only waiting for a slot. Only **Questions for
     you** counts questions that are still open;
   - "deferred": on hold until a file appears, a retry time passes or a
     setting is fixed;
   - "concurrency ceiling": the most tasks the queue may run at once.

   Give every **Not normal right now** item with what to do, then the
   **For your information** items.
2. **Then the details**, section by section, each with one sentence on
   what it means, including the concurrency ceiling (its value, where it
   comes from, whether the queue-wide cap binds) and any account that
   cannot take tasks (the runner's error, which names the file when its
   runner-account.toml is at fault, and that the account takes tasks again
   within a tick of the fix).
3. If a section could not be gathered it says "unknown", "could not list"
   or "unavailable"; say its facts are unknown, never empty or healthy.

The script's exit code says whether the report can be trusted:

- **2, no report:** the queue does not exist or has no `todo/`
  subdirectory, usually a mistyped `--queue` or a working directory
  that is not the queue. The reason and the path are on stderr. Tell
  the user which path was tried and ask for the queue's path. Never
  describe it as an idle or empty queue.
- **1, report printed:** the open sidecars could not be listed. The
  **Open sidecars** line reads "could not list" and gives the reason.
  Say the open sidecars are unknown, never "no open sidecars".
- **0:** the report was printed. A part that could not be gathered still
  says so in place: an account list or task selection the CLI could not
  give ("unknown" in the summary, "could not list" in the details), a
  section that failed ("**<section>**: unavailable: <error>"), or
  report.py failing as a whole ("**Report**: report.py exited N"). Say
  those facts are unknown.

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
   they referenced a different one. `claude-task-runner account list
   --json` carries each account's `weekly_catch_up_at`, `usage_error` and
   `dispatch_cap`; `claude-task-runner queue holds --json` says what can
   start and what holds the rest.

2. **Parse** the JSON. Surface findings in this priority order
   (highest first — only show every line that is relevant):

   1. **Usage could not be read** — if `snapshot.last_drift_message` is
      non-empty OR `snapshot.state == "error_drift"`, or an account is in
      `error_drift`: this is critical, the account takes no tasks. Print
      a red line with the message. `account list --json`'s `usage_error`
      says which kind: `auth` (the login was rejected, an expired
      token): log the account in again, `CLAUDE_CONFIG_DIR=<its
      config_dir> claude /login`, or renew its long-lived token with
      `claude setup-token`; `format` (the usage page changed): run
      `claude-task-runner usage --config <the queue's claude_runner.toml>
      healthcheck` (the supervisor's own `--config` when it was started
      with one; without `--config` it reads the package's default account,
      not the queue's), or invoke `/runner-usage`. On a multi-account
      queue also name the account, `usage --config <toml> --account <name>
      healthcheck`, once `usage` has `--account`; until then it checks
      the queue's `[claude].config_dir`. Stop here unless the user wants
      more.

   2. **Account that cannot take tasks** — if `account_errors` is
      non-empty: each entry is an account that silently takes no tasks
      and counts 0 toward the ceiling, while every other account runs as
      usual, so nothing else looks wrong. Its `cause` says why, and what
      to fix: `file`, its `runner-account.toml` (`path`) does not load:
      fix the file; `config_dir`, its config_dir cannot hold that file
      (it does not exist, as on a mount not up yet, names no user's home,
      or a path on the way is not a directory): fix the config_dir or
      bring its mount up; `sudo`, its linux_user needs sudo, which is not
      on the supervisor's PATH: install sudo or put it on that PATH (the
      file is not the problem, so do not name it). Give the account and
      the `error` (which names the file or directory at fault), and say
      the account takes tasks again at the supervisor's next tick after
      the fix. `snapshot.accounts.<name>.policy_error` carries the same
      error.

   3. **No usage reading** — if `snapshot.state == "no_reading"`, or
      any entry of `snapshot.accounts` has `state == "no_reading"`:
      that account takes no tasks until a clean `/usage` capture lands.
      Print each such account with its `last_reading_at` ("never" when
      null) in yellow. Every account starts there after a supervisor
      start and leaves within one capture cycle (one poll per account),
      so only one that persists is a problem; point the user at the
      runbook section "An account stays in `no_reading`".

   4. **Weekly cap** — if `snapshot.state == "throttled_weekly"`, or an
      account is: print "Weekly utilization NN% > target (throttled)" in
      yellow. The trace-following rule (ADR-0022) resumes the account
      when the weekly curve catches up with its use: give that time from
      `account list --json`'s `weekly_catch_up_at` ("resumes about …, when
      its weekly use falls back under plan"). When `weekly_window_opens_at`
      is set, the account has `early_pct = 0` and is waiting for its
      end-of-week window (ADR-0041): say so and give that time instead
      of calling its use over plan. `scheduled_wakeup_at` is
      only the supervisor's next re-check, clamped to the next 5-hour
      reset when the account has a 5-hour window, so never give it as
      the resume time.

   5. **5h throttle** — if `snapshot.state in ("throttled_5h",
      "slowing_down")`: print 5h utilization + state. For each
      `slowing_down` account, also give its target from the
      per-account table ("personal slowing down, target 2").

   6. **Queue-wide cap binds** — if `queue_ceiling.binds` is true: the
      queue TOML's `[concurrency].max_concurrency` (`queue_ceiling.
      max_concurrency`) is below the sum of the accounts' own caps
      (`queue_ceiling.accounts_total`, broken down in
      `queue_ceiling.account_caps`), so it, not the accounts, limits how
      many tasks run. Say so in plain words and that raising or removing
      it uses every account slot. Otherwise give the ceiling in one line
      ("may run 8 at once: personal 5 + work 3, no queue-wide cap").

   7. **Open questions** — run `claude-task-runner sidecar list --queue
      <CWD> --json` and report the requests with outstanding questions,
      by task ID. Suggest `/runner-answer-sidecar` if any.

      Report the **question** count alongside the request count: sidecars
      are open per question (ADR-0031), so one request can owe four
      answers, and a request whose response answered only some of its
      questions is still open. `sidecar list --json` carries both as
      `n_open` and `n_outstanding_questions`. Never report "0 open
      sidecars" off the request count alone. A row with no outstanding
      question is a notice to acknowledge; a row with an `error` is a
      request that cannot be read and needs repair.

      Do not count `awaiting_sidecar` tasks as questions: a task keeps
      that status after its questions are answered, until it runs again.
      `queue holds --json` counts the answered ones as able to start
      (`eligible.by_status.awaiting_sidecar`) and the ones still waiting
      as `unanswered_sidecar`.

   8. **Hung tasks** — run with `--status possibly_hung`. Report each.
      One whose `stop_reason` is `worker_still_running` is not stuck: the
      supervisor parked it because a worker it does not watch was still
      running (left from before a restart, or alive after it was
      stopped), so it starts no second worker beside it. `queue holds
      --json` lists these as `parked_workers`, with whether each still
      runs and whether it has passed its time limit. While it runs and is
      within its limit there is nothing to do; to end it sooner, stop it
      with `kill -TERM -<pid>` (the minus signals its process group).
      Past its limit, a running supervisor stops it at its next check and
      records the run; stop it yourself only while the supervisor is not
      running, or when it is still listed after that check.

   9. **Recent failures** — `--status failed` and
      `--status failed_circuit_breaker`. Report counts; if non-zero,
      offer the task IDs.

   10. **Deferred tasks** — run `claude-task-runner queue states
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
       - `missing dependency:` — the task's `depends_on` names a task id
         that has no task file in `todo/` and is not completed or running
         (no task has it, or only a state left by a renamed or deleted
         task), so it can never complete (ADR-0036). It stays parked
         until the task's `depends_on` is fixed or the missing task is
         created in `todo/`; the supervisor un-parks it at its next check.
         This needs the operator: list each task with the ids its reason
         names.
       - `unmeetable dependency:` — the task's `depends_on` names a task
         that exists but cannot complete: the task itself, a task in a
         dependency cycle with it, or a `failed_circuit_breaker` task
         (ADR-0036). It stays parked until the depends_on is fixed or the
         cycle broken, or, for a stopped task, until its state file
         (`.claude_task_runner/state/<id>.yaml`) is edited back to
         `status: pending` once the cause of its failures is fixed: no
         `queue` command resets a circuit breaker, and `queue
         force-dispatch` refuses that status. This needs the operator:
         list each task with the dependencies and causes its reason names.
       - `pre-dispatch hook deferred (exit 1)` — the queue's pre-dispatch
         hook asked to wait. The hook runs again once the task's
         `next_eligible_at` passes, which is `deferral_recheck_cooldown_s`
         in `[failure_classifier]` (900 s by default) after the deferral.
         Give the count and the earliest `next_eligible_at`.
       - `cannot start the worker:` (stop reason `worker_start_deferred`)
         — the worker failed its checks before it was spawned: the
         account's `config_dir` is missing or cannot be expanded, `sudo`
         is missing for its `linux_user`, the task's `working_dir` is not
         trusted or cannot be expanded, or its log files or the spawn
         itself failed. The rest of the reason names which. Like a hook
         deferral it sets `next_eligible_at` (`deferral_recheck_cooldown_s`
         after it) and is tried again once that passes. This needs the
         operator: give each task with its reason and `next_eligible_at`,
         and say to fix the named cause; `queue force-dispatch <id>`
         starts it at once after the fix. The summary words these as
         "could not start its worker".

         Of the runner's own deferrals, these two set
         `next_eligible_at`; the readiness, effort, missing-dependency and
         unmeetable-dependency holds do not.
       - Anything else was written by hand or by another tool. The
         reason is only a label and does not hold the task. Once its
         `next_eligible_at` passes, or at the next tick if it has none,
         the task can be dispatched again. A `next_eligible_at` with no
         offset never passes: the task is held as
         `next_eligible_at_without_timezone` until the time is written in
         UTC with an offset. If a gate holds it then, the
         gate's own reason replaces the hand-written one. List each task
         with its reason and `next_eligible_at`.

       A row with an `error` field is a state file that could not be
       parsed. `queue states` lists those whatever `--status` asks for,
       so report them separately, not as deferred.

   11. **Nothing in flight** — if no task is in flight and some account
       is open for dispatch, `queue holds --json` says why now: no task
       can start when `eligible.count` is 0 and `held` counts what holds
       the rest (`block_dispatch`, `readiness_missing_file`, `depends_on`,
       `depends_on_missing`, `depends_on_unmeetable`,
       `unanswered_sidecar`, a status name, ...). `depends_on` waits for a
       task that exists and has not finished; `depends_on_missing` names
       one with no task file in `todo/` that is not completed or running,
       and `depends_on_unmeetable` one that exists but cannot complete
       (the task itself, a cycle, a circuit-broken task). Neither clears by
       waiting, and both need the operator: `missing_dependencies` lists
       each missing task with its `missing` ids, `unmeetable_dependencies`
       each unmeetable one with its `unmeetable` dependencies and their
       `cause`, a cycle's by its index in `dependency_cycles`, which lists
       every task of each cycle once. If tasks can start and
       an account has room but nothing runs, look in the supervisor's log
       for `dispatch skipped task` lines. The snapshot's **Last idle
       report** is the supervisor's own `no eligible tasks:` line, which is
       history: logged only when the counts change, so it may be days old.
       The runbook section "Nothing dispatches, but an account has room"
       explains each category.

   12. **Healthy summary** — if none of the above, one terse line:
       "Supervisor (state) · 5h NN% · weekly NN% · pending K ·
       in-flight M · ceiling C", with "5h not reported" for an account
       whose reading has no 5-hour window (never "5h 0%").

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
