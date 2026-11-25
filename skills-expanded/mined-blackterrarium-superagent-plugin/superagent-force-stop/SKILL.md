---
name: superagent-force-stop
description: Use to recover a HUNG or wedged superagent EXTERNAL tick — a loop stuck at a transient status (RUNNING/PLANNING) with the L3 overlap lock held and no forward progress (e.g. a tick process that hung, or a tick killed mid-flight that orphaned its lock). Halts the in-flight tick, reaps the stale `.lockd` lock so the loop self-heals immediately instead of waiting out the 90-min lock-steal window, and (by default) kicks a fresh recovery tick. Distinct from superagent-stop (which disarms the scheduler for a healthy loop); this is the force/recover path for a stuck one. Identify the loop by its root master plan (PLAN.md) or --slug.
argument-hint: "(<PLAN.md> | --slug <goal-slug>) [--drain] [--no-kick]"
license: MIT
related skills: superagent-monitor, superagent-stop, superagent-external, superagent, superloop
---

# Superagent force-stop

Recovery path for a **hung** superagent external tick — the complement of
`superagent-stop` (which gracefully disarms the scheduler of a *healthy* loop).
It wraps the deterministic `${CLAUDE_PLUGIN_ROOT}/scripts/force-stop.sh`, which halts the
wedged tick and removes the stale **L3 overlap lock** so the loop resumes at once
instead of waiting out the `SUPER_LOCK_STEAL_MIN`-minute (default 90) lock-steal window.

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

## When to use this (vs superagent-stop)

Reach for force-stop only when a tick is genuinely **stuck**, diagnosed via the
`superagent:superagent-monitor` skill (`status.sh <slug>`):

- `STATUS` is a **transient** (`RUNNING` / `PLANNING`) **and** `LOCK=yes`, but the
  tick is making no progress — either the tick process has hung (`TICK=yes`/`activating`
  for far longer than the work should take) or a prior tick was killed and left an
  **orphaned lock** (`TICK=no` but `LOCK=yes`).
- You do **not** want to wait for the automatic `SUPER_LOCK_STEAL_MIN`-minute
  (default 90) lock-steal self-heal.

If the loop is **healthy** and you simply want to pause/stop it, use the
`superagent:superagent-stop` skill (graceful drain). If a tick is legitimately
mid-flight (e.g. driving a long CI push — ticks run uncapped by default), it is
**not** hung; leave it alone. Never force-stop a tick that is doing real work.

## Parameters

- **`<PLAN.md>` or `--slug <goal-slug>` — one is required.** Identify the loop by its
  **root** master plan (matched against the registered env files, like
  `superagent-stop`) (an absolute path when the vault is external — `stop.sh`/`force-stop.sh` match it against the loop file's absolute `master_plan:`) or directly by slug.
- **`--drain` — optional.** After cleanup, also disable the timer (stop the loop).
  Default keeps the timer armed so the loop resumes.
- **`--no-kick` — optional.** Do not immediately start a recovery tick after cleanup.
  Default kicks one (when the timer stays armed) for immediate self-heal.

The script is **DRY-RUN by default**; the steps below run the preview first, confirm
with the human, then re-run with `--apply`.

## Steps

1. Resolve the target through its per-goal registry row. `force-stop.sh --slug` loads the recorded
   physical project root/mode before project configuration, so it may run outside the project.
2. **Diagnose first with the `superagent:superagent-monitor` skill.** Confirm the
   loop is actually stuck (transient status + held lock + no progress). If it is
   healthy or a tick is doing real work, STOP — force-stop is the wrong tool.
3. **Preview (dry-run).**

   ```
   $SUPERAGENT_SCRIPTS/force-stop.sh (<PLAN.md> | --slug <slug>) [--drain] [--no-kick]
   ```

   It prints the target's status/iteration, whether the tick service is active,
   whether the lock is held (and its age), the planned post-action, and any
   worktrees to review — changing nothing.
4. **Confirm with the human** (`AskQuestion`), showing the dry-run summary. Halting a
   tick and removing its lock is destructive — get explicit consent before applying.
5. **Apply.** Re-run with `--apply` appended:

   ```
   $SUPERAGENT_SCRIPTS/force-stop.sh (<PLAN.md> | --slug <slug>) --apply [--drain] [--no-kick]
   ```

   It halts the in-flight tick (`systemctl --user stop` reaps the service cgroup,
   including the wrapped `claude` child — precise, no blind `pkill`),
   removes the stale `.lockd`, and either kicks a recovery tick (default) or drains
   the timer (`--drain`).
6. **Report** the outcome and what happens next: the next/kicked tick's
   crash-recovery (superloop L2) resets the persisted `RUNNING`/`PLANNING` →
   `WAITING FOR RUN`/`WAITING FOR PLAN` and re-dispatches. Confirm with the
   `superagent:superagent-monitor` skill after a minute.

## Safety invariants

- **The loop-status file is never edited** by this skill. The status reset is left to
  the next tick's crash-recovery (L2), which owns the `prior_status` handling — the
  script only removes the lock and halts the service, so it can never corrupt the
  state machine.
- **Precise process kill only.** `systemctl --user stop` kills exactly the tick
  service's cgroup. The script never blanket-`pkill`s `claude` (that
  would kill unrelated interactive sessions). If a tick's CLI process is wedged but
  detached from any service cgroup, the script reports it and you must identify +
  kill that PID manually.
- **Worktrees are reported, not removed.** A killed `superrun` tick may leave a
  worktree with uncommitted work; `superrun` reconciles/recreates its own on
  re-dispatch. Review listed worktrees by hand before removing any.
- **Dry-run first, confirm before `--apply`.** Preview and human consent precede any
  mutation.
- **The loop-status file is preserved**, so a `--drain`ed loop relaunches with the
  `superagent:superagent-external` skill (`$SUPERAGENT_SCRIPTS/launch.sh <PLAN.md>`).
