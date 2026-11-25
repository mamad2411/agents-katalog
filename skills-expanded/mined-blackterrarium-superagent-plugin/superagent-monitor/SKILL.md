---
name: superagent-monitor
description: Use to monitor and control the superagent external loops running on this host — list every concurrent loop and its live state (status, iteration, timer/tick/lock, WAITING FOR INPUT, DONE), answer a parked decision, and perform lifecycle actions (drain, hard-stop, uninstall a DONE loop, re-arm a stopped one). The console/control plane for the plugin's external driver.
argument-hint: "[<slug>]   (omit to cover all loops)"
license: MIT
related skills: superagent, superloop
---

# Superagent monitor

The **console / control plane** for superagent external loops (the driver plane is this
plugin's `scripts/` directory + the per-goal scheduler entry, a systemd user timer on
Linux or a launchd LaunchAgent on macOS — see
[scripts/README.md](../../scripts/README.md)). This skill is read-first and
start/stop-independent of the driver: it reads the same gitignored loop-status files the
drivers own and never blocks their ticks. It is **multi-instance by default** — the
registry is every per-goal env file under `~/.config/superagent/*.env`, so one invocation
covers all concurrent loops. Pass a `<slug>` to scope to one.

## Project loops and separate identities

These controls also handle supercode projects. Monitor text/JSON retain existing fields and expose
`supervisor`, `project`, `round`, `inner_slug`, `inner_status`, `last_verdict`, and `pending_owner`.
Use the registered custom slug from status output; never guess it from a project/goal basename.
`stop.sh (<PLAN.md> | <project-dir> | --slug SLUG)` and
`force-stop.sh (<PLAN.md> | <project-dir> | --slug SLUG)` resolve exact registration, repo and state
identity before mutation. Unknown or mismatched targets refuse. Existing drain/hard/purge and
force-stop apply/drain/no-kick semantics remain; a selected outer action affects only that outer.
Its output reports the remaining child registration and exact separate `stop.sh --slug CHILD`
command. Run that child command only when stopping the child was explicitly requested. Never imply
an outer stop killed the inner. Both state files and committed artifacts remain preserved.

Project force recovery uses the persistent `.reclaim` advisory guard and refuses a live peer.
It leaves state untouched: the next native tick reconciles artifacts before mapping META-PLANNING
→ WAITING FOR META-PLAN, EVALUATING → WAITING FOR EVAL, or DIAGNOSING → WAITING FOR DIAGNOSIS.
It never maps project transients to WAITING FOR RUN. Agreement adoption and raised limits require
explicit recorded answers per supercode; a rearm alone is not an answer.

## Repo configuration (.superenv)

Resolve project context before any workflow action by sourcing `${CLAUDE_PLUGIN_ROOT}/scripts/_common.sh` under bash (it refuses zsh and other shells — wrap the call in `bash -c '…'` when your shell is not bash) and calling `superagent_load_context "$PWD" run` (lifecycle control commands first load the registered `SUPERAGENT_PROJECT_ROOT`). Use its exported physical `REPO` and validated `SUPER_GIT_MODE`. Resolution is process environment > nearest/explicit project `.superenv` > packaged default; missing mode means `github`. In `none`, never run git, gh, GitHub API, credential discovery, worktree, commit, push, PR, merge, sync, or CI-poll operations. An existing `.git` directory does not change this rule.

## Step 1 — Enumerate (always safe, read-only)

Run the deterministic enumerator and present its table to the user:

```
$SUPERAGENT_SCRIPTS/status.sh          # table across ALL loops
$SUPERAGENT_SCRIPTS/status.sh <slug>   # drill into one (pending decision + tails)
$SUPERAGENT_SCRIPTS/status.sh --json    # machine-readable, for your own parsing
```

The table columns are `SLUG STATUS ITER TIMER TICK LOCK INPUT GH-AUTH`. Each registry row is
resolved in its own subshell, so one project's values cannot become another project's overrides.
Read them, then **interpret** for the user:

- **`GH-AUTH=disabled`** — the row records `SUPER_GIT_MODE=none`; status did not load a token or
  contact `gh`. **`unauth`** (or `no-gh`) on a GitHub row blocks that row's CI/PR operations and its
  tick preflight aborts loudly. Fix the affected project's `GH_TOKEN`/authentication as described in
  [scripts/README.md](../../scripts/README.md#prerequisites).
- **`INPUT=YES`** (status `WAITING FOR INPUT`) — the loop is parked on a decision the L7 panel could not
  resolve. Offer to answer it (Step 2). The operator was notified once when it parked (SUPER_NOTIFY_CMD /
  desktop), and scheduled fires are free until answered (SUPER_INPUT_GATE). `INPUT=ans` means an answer is
  already recorded and the next fire (or `answer.sh`'s kick) resumes — nothing to do.
- **`STATUS=DONE`** — the goal is complete. The tick wrapper self-disarms the scheduler entry on the
  `DONE` tick (`SUPER_AUTO_DISARM_ON_DONE`, default `true`), so the timer is normally already gone;
  if one is still armed (opt-out, or a loop armed by a pre-0.4.6 build), offer to uninstall it (Step 3).
- **`STATUS=WAITING FOR CI`** — the loop is **parked on a long CI wait** (run ids in the loop file's
  `ci_wait:` block), not stuck: the wrapper checks the runs with `gh run view` in bash each interval and
  launches no session until every run is terminal (`SUPER_CI_GATE`). A long park is normal for 60–120 min
  lanes; check the runs (`gh run view <id>`) only if the user asks or the park exceeds the lane's expected
  runtime. A park older than `SUPER_CI_MAX_WAIT_MIN` (default 180 min, per `ci_wait.since`) is announced
  once as `ci-stale` (`SUPER_NOTIFY_CMD` / desktop) and the gate falls open — sessions then run each
  interval; if the user asks about that notification, inspect the runs and offer to cancel/re-trigger.
- **`TIMER!=active` but STATUS non-terminal** — the driver was stopped/removed while work remains; offer
  to re-arm (Step 3).
- **`TICK=yes` / `LOCK=yes`** — a tick is running right now. Do **not** mutate that loop's file or
  hard-stop without warning the user; monitoring is still fine.
- **loop file missing** (`status.sh` shows `<none>`/exists=no) — the local loop-status file is gone
  (wiped checkout / different host). Progress lives in the vault plan tree, not the loop file — resuming
  means re-running `bootstrap.sh` (a FRESH START that re-derives next-step from the tree); flag this.

For live following, either re-run Step 1 on request, or arm the watcher (event-gated, one per loop):
`$SUPERAGENT_SCRIPTS/console-watch.sh <LOOP_FILE>` (it emits
`AGENT_LOOP_WAKE_superagent {...}` on `WAITING FOR INPUT`/`DONE`).

## Step 2 — Answer a `WAITING FOR INPUT` loop

Drill in first (`status.sh <slug>`) and show the user the `## Pending decision` block verbatim. It
leads with what failed, the most likely cause and the recommended option; identifiers and the
panel's analysis sit in its trailing reference list. A protected-change request is a yes/no question:
`yes` approves exactly the change it names, `yes <value>` the same change with a different value, and
`no` takes the path the block states. A block that offers only requests for more evidence, authority
or budget, or that names no likely cause, is malformed (superloop L7 Rung 2) — say so to the user. So
is a block that asks the user to write specification or policy text, or to settle a specification gap
without saying which acceptance case depends on it and whether narrowing or postponing that case would
avoid it.
Then choose a path. **Prefer the attended tick** — it is
race-free (runs under the L3 lock and applies + continues in one step).

Read the loop's `LOOP_FILE` from `~/.config/superagent/<slug>.env`.

**Path A — `answer.sh` (preferred).** Present the decision options to the user with `AskQuestion` (the
block's recommended option first), then
record the answer and resume the loop in one step — it takes the loop's L3 lock (refuses if a tick is
mid-flight: retry), writes `answer: <option>` under `## Pending decision`, and kicks one tick
immediately so the loop resumes now rather than after the interval (the wrapper's `SUPER_INPUT_GATE`
otherwise skips sessions until that line exists):

```
"$SUPERAGENT_SCRIPTS/answer.sh" <slug> "<option>"        # --no-kick records only; --replace overwrites a recorded answer
tail -f /tmp/superagent-<loop-basename>.log               # watch the resumed tick
```

Exit codes: 2 = usage (unknown flag / missing slug or answer), 1 = unknown slug or missing loop file,
3 = not `WAITING FOR INPUT`, 4 = lock held (a tick is running — wait, then retry; if no tick is
running the lock is stale, `force-stop.sh --slug <slug>` reaps it), 5 = no `## Pending decision`
heading in the loop file.

**Path B — attended tick (when you want to watch it apply in-session).** Run exactly one interactive
tick, passing the chosen answer as guidance. The skill's `WAITING FOR INPUT` branch consumes it,
records it under `## Decisions`, restores `prior_status`, and continues the tick — all under the lock,
serialized against the scheduler. Derive the plugin root from `$SUPERAGENT_SCRIPTS` and read the skill
file directly (headless `claude -p` cannot run a slash command or rely on `${CLAUDE_PLUGIN_ROOT}` —
superloop L2 Driver B):

```
cd "$primary_root"
PLUGIN_ROOT="$(cd "$SUPERAGENT_SCRIPTS/.." && pwd)"
claude -p "Read ${PLUGIN_ROOT}/skills/superagent/SKILL.md and run exactly ONE --tick on loop file <LOOP_FILE>. The pending decision is answered: <ANSWER>. Apply it and continue the tick." --allowedTools "Read,Edit,Write,Bash,Task,Skill"
```

Never call `AskUserQuestion`/`AskQuestion` on behalf of a *headless* tick — that is the driver's job to
avoid. This skill is the interactive plane, so `AskQuestion` here (to the human at the console) is correct.

## Step 3 — Lifecycle actions (confirm destructive ones first)

All wrap the existing driver scripts; run them from `primary_root` via `$SUPERAGENT_SCRIPTS`. **Ask the
user before any stop / uninstall / purge.**

- **Drain (graceful stop):** `$SUPERAGENT_SCRIPTS/uninstall-timer.sh <slug>` — disables the timer so no
  new ticks fire; a **running tick finishes on its own** (it is not killed). Leaves the loop file + env
  so it can be re-armed.
- **Hard stop (halt an in-flight tick):** after confirming, `systemctl --user stop
  superagent-tick@<slug>.service`. Abrupt — leaves a stale lock (auto-stolen on the next tick: at once
  when its recorded owner PID is dead, else after `SUPER_LOCK_STEAL_MIN` minutes, default 90) and a
  persisted `PLANNING`/`RUNNING` state, both self-healed by crash-recovery on
  the next run. May interrupt a git/PR/CI op. Prefer drain unless an immediate halt is needed.
- **Force-stop a HUNG tick (halt + reap the lock now):** when a tick is wedged (transient status + held
  lock + no progress) and you don't want to wait out the `SUPER_LOCK_STEAL_MIN`-minute (default 90)
  lock-steal, use the `superagent:superagent-force-stop` skill
  (`$SUPERAGENT_SCRIPTS/force-stop.sh (<PLAN.md> | --slug <slug>) [--apply]`). It halts the tick,
  removes the stale `.lockd`, and kicks a recovery tick so the loop self-heals immediately (dry-run first;
  confirm before `--apply`). This is the recover-a-stuck-loop path; plain hard stop above just halts.
- **Uninstall a DONE loop:** `$SUPERAGENT_SCRIPTS/uninstall-timer.sh <slug>` (add `--purge` to also drop
  `<slug>.env`) — confirm `--purge`.
- **Re-arm a stopped loop:** `$SUPERAGENT_SCRIPTS/install-timer.sh <slug> <LOOP_FILE>`
  (re-pass `--interval`/`--timeout`/`--model` — `install-timer.sh` rewrites the env file and drop-in
  from scratch). No `bootstrap.sh` needed when the loop file still exists.
- **Tail output:** `journalctl --user -u superagent-tick@<slug>.service -f` or
  `tail -f /tmp/superagent-<loop-basename>.log`. Verbatim per-tick reports land here.

## Safety invariants

- **Read-only enumeration (Step 1) is always safe** and never affects loop progress — start/stop this
  monitor freely.
- **Locks are load-bearing.** `answer.sh` (Path A) takes the lock for you; if hand-editing a loop-status
  file directly, hold that loop's `.<loop>.lockd` yourself. Never touch a loop whose `LOCK=yes`/`TICK=yes`
  without the lock.
- **Confirm before destructive actions** (hard stop, `--purge`). Drain and re-arm are reversible.
- **Operate per `primary_root`.** The loop files and locks exist only at the vault root (the primary
  checkout for an internal vault, the vault repo for an external one); a `<slug>` with a missing
  loop file is a resume-via-bootstrap situation, not an error to paper over.
