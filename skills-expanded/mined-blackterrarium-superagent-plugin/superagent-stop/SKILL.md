---
name: superagent-stop
description: Use to stop a superagent EXTERNAL (unattended) loop for a goal, given only the goal's root master plan (PLAN.md). Complements superagent-external. Default is a graceful drain (disable the timer; a running tick finishes); optional --hard halts an in-flight tick immediately and --purge removes the per-goal env file. The loop-status file is always preserved so the loop can be relaunched.
argument-hint: "<PLAN.md> [--hard] [--purge]"
license: MIT
related skills: superagent-external, superagent-monitor, superagent-force-stop, superagent, superloop
---

# Superagent stop

One-step stopper for an unattended superagent loop — the complement of
`superagent-external`. It wraps the deterministic `${CLAUDE_PLUGIN_ROOT}/scripts/stop.sh`,
which identifies the installed loop from the master plan and disarms its per-goal
scheduler entry (systemd user timer on Linux, launchd LaunchAgent on macOS).

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

## Parameters

- **`<PLAN.md>` — required.** The goal's **root** master plan (the same file passed
  to `superagent-external`). This is the only compulsory argument (an absolute path when the vault is external — `stop.sh`/`force-stop.sh` match it against the loop file's absolute `master_plan:`).
- **`--hard` — optional.** Also halt an in-flight tick immediately (SIGTERM the
  service). Default is a graceful drain: the timer is disabled so no new ticks fire,
  and a tick already running finishes on its own.
- **`--purge` — optional.** Also remove the per-goal env file
  (`~/.config/superagent/<slug>.env`).

When these are absent, DO NOT pass them — default graceful drain, env kept.

## Steps

1. Set `$SUPERAGENT_SCRIPTS` to this plugin's installed `scripts/` directory. The
   stopper matches the plan against the per-goal registry first and loads that row's recorded
   physical project root/mode before project configuration, so it may be invoked outside the
   project — see [scripts/README.md](../../scripts/README.md) for the convention:

   ```
   primary_root="$REPO"
   SUPERAGENT_SCRIPTS="${CLAUDE_PLUGIN_ROOT}/scripts"   # CLAUDE_PLUGIN_ROOT is set in Claude Code sessions;
   # for cron/systemd use the absolute install path — see scripts/README.md
   ```
2. **Invoke the stopper** with the parsed arguments:

   ```
   $SUPERAGENT_SCRIPTS/stop.sh <PLAN.md> [--hard] [--purge]
   ```

   `stop.sh` finds the installed loop by matching the plan against the registered
   env files (`~/.config/superagent/*.env`) — robust even if a custom `--slug` was
   used at launch — disables + stops the timer, optionally halts the in-flight tick
   (`--hard`) and removes the env file (`--purge`). It **always preserves the
   loop-status file** so the loop can be relaunched/resumed.
3. **Report** the stopper's output: the goal slug, whether a running tick was
   drained vs halted, whether the env was kept vs purged, and the relaunch command.

## Notes

- **Graceful by default.** Without `--hard`, a tick that is mid-flight (e.g. driving
  CI) completes cleanly; only the scheduling stops. Use `--hard` only when you need
  an immediate halt (it may interrupt a git/PR/CI op; the next run self-heals via
  crash recovery).
- **Idempotent / safe.** Unknown or mismatched identities refuse before scheduler mutation; a registered stopped loop can be stopped again.
- **Relaunch** later with the `superagent:superagent-external` skill (or
  `$SUPERAGENT_SCRIPTS/launch.sh`); since the loop-status file is preserved, it
  resumes from where it left off.
- To *inspect* rather than stop (or to answer a `WAITING FOR INPUT` decision), use
  the `superagent:superagent-monitor` skill.
- **For a HUNG tick** (stuck at a transient `RUNNING`/`PLANNING` with the lock held and
  no progress) use the `superagent:superagent-force-stop` skill, not this one.
  `--hard` here only halts and leaves the stale lock to the next tick's steal (immediate
  when the recorded owner PID is dead, else the `SUPER_LOCK_STEAL_MIN`-minute (default 90)
  window); `superagent-force-stop` reaps the lock and kicks a recovery tick
  so the loop self-heals at once.
