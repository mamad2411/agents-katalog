---
name: monitor-loop
description: |
  Periodically monitor background jobs, services, and processes; if everything is fine
  leave it alone, and the moment something errors or stalls, investigate, diagnose the
  root cause from the logs, fix it within a defined scope, and report. Use this skill when
  the user says "/monitor-loop", "keep an eye on my services", "check every N hours",
  "watch my background jobs", "restart it automatically if it dies", "monitor and self-heal",
  or asks to keep something running and managed over time. Two ways to run it: (1) a live
  session loop that self-wakes on a timer, or (2) a headless daemon (scripts/daemon.py)
  under launchd/systemd/cron for 24/7 watching without a session. On failure it uses the
  agent to read logs and fix the cause — guarded by a circuit breaker and a fix scope.
---

# monitor-loop — autonomous monitoring & self-healing

## Core principle

**If it's green, don't touch it. If it's red, dig until it's fixed.**

Every check has exactly two branches:
- **GREEN** → log one line, schedule the next check, stay quiet. Never poke a healthy system.
- **RED** → stop, switch to diagnosis mode, find the root cause, fix within scope, report.

What makes this different from `supervisor` / `monit` / `pm2`: those can only restart.
monitor-loop hands a RED incident to the agent, which **reads the logs, reasons about
*why* it broke, and fixes the actual cause** — then verifies green is restored.

## Two run modes

| Mode | How | Best for |
|------|-----|----------|
| **Session loop** | A live agent session that re-checks on a timer (self-wake / `/loop`) | While you're working, ad-hoc watches |
| **Headless daemon** | `scripts/daemon.py <name>` under launchd / systemd / cron | 24/7, session-free, the real watchdog |

The daemon is the production path. The session loop is convenient but dies when the
session ends — say so to the user and offer the daemon for anything that must survive.

**Trust level — diagnose-only is the default, on purpose.** A 24/7 agent editing files is
scary and must be opt-in. By default the daemon runs *diagnose-only*: on RED it reads the
logs read-only, reports the root cause + suggested fix, and changes nothing. Actually
applying fixes requires `--auto-fix` (or `auto_fix: true` in the monitor), and when a
`git_repo` is set, auto-fix snapshots it first and rolls back if the fix fails. Recommend
diagnose-only first; suggest `--auto-fix` only once the user trusts the fix_scope.

---

## Phase 0 — define the monitor

Pin these down before looping. If unclear, ask — don't guess.

| Field | Meaning |
|-------|---------|
| **targets** | What to watch — process / service / port / HTTP / log freshness / log errors / disk / cron output |
| **GREEN criteria** | What "healthy" means for each target |
| **interval** | How often to check (seconds) |
| **fix_scope** | The boundary of what may be auto-fixed. Outside it → report only, never act |
| **git_repo** | *(optional)* repo that auto-fix may edit — snapshotted + rolled back on failure |
| **auto_fix** | *(optional)* `true` lets the daemon apply fixes; default false = diagnose-only |
| **notify_cmd** | Any shell command to send a notification (Telegram, Slack, ntfy, mail…). The message is the last arg |

Targets live in `~/.monitor-loop/<name>.json`. Scaffold one with:

```bash
python scripts/check.py --monitor <name> --init
```

Then edit `targets` and `fix_scope`. Target recipes (every type + remote-over-SSH)
are in `references/check-recipes.md`.

### Discovering targets

If the user is vague ("the stuff running in the background"), scan first and agree on a list:

```bash
ps aux | grep -iE "python|node|server|worker|bot" | grep -v grep   # processes
systemctl --user list-units --type=service --state=running          # Linux services
launchctl list | grep -v '^-'                                       # macOS services
```

---

## Phase 1 — check (every cycle)

When the timer fires, run the engine first:

```bash
python scripts/check.py --monitor <name>
# stdout JSON: {"status":"green|red","failed":[...],"circuit":"closed|open|half-open",
#               "can_attempt_recovery":true|false,"fix_scope":"..."}
# exit code: 0 = green, 2 = red
```

- **green** → log it, go to Phase 3 (reschedule). Don't notify (avoid alert fatigue).
- **red** → go to Phase 2 (diagnose & fix).

**Transient guard:** if a target is red for the first time, re-check once after a short
pause before any heavy action — a single blip isn't an incident. An outright "process
gone" can skip the wait.

---

## Phase 2 — diagnose & fix (RED only)

No fire-fighting hacks. Fix the cause, not the symptom.

1. **Respect the circuit breaker first.** If `can_attempt_recovery` is `false` (the breaker
   is open — too many consecutive failures or too many recovery attempts this hour), do
   **not** attempt another fix. Send one notification asking for a human and stop. This is
   what prevents an infinite fix-loop and runaway token cost.

2. **Record the attempt** before fixing, so the breaker can count it:
   ```bash
   python scripts/check.py --monitor <name> --record-recovery
   ```

3. **Diagnose.** Read the actual logs for the failed target. Quote the real error. Identify
   the most recent change (deploy / config / disk / network / expired credential). Form a
   hypothesis and test it. For recurring structural faults, escalate to a deeper redesign
   rather than restarting forever — restarting every time is a patch, not a fix.

4. **Fix — within `fix_scope` only.** Outside the scope, report and stop. Prefer reversible
   actions (restart / retry). Back up anything you edit. The most common correct fix is a
   restart; if that's enough, do only that.

5. **Verify.** Re-run the check. If green: `--resolve "<what you did>"` (records the incident,
   resets the breaker). If still red and scope is exhausted: notify for human help.

The headless daemon automates this exact sequence (`scripts/daemon.py`), delegating step 3–4
to `claude -p`. In a live session, you *are* the recovery agent — do it directly, optionally
leaning on systematic-debugging / a second-opinion model / a sandbox test before applying.

---

## Phase 3 — report & reschedule

- **Report only after handling a RED** — on a successful auto-fix (what broke / root cause /
  what you did, in ~3 lines) or when human help is needed. Green cycles stay silent.
  ```bash
  python scripts/check.py --monitor <name> --notify "<message>"
  ```
- **Reschedule** the next check so the loop continues. In the headless daemon this is the
  sleep at the end of the loop; in a session loop, set the next self-wake for `interval`
  seconds. If this step is skipped, the loop dies.

To stop: stop the daemon (launchd/systemd/cron), or in a session, don't reschedule.

---

## The loop at a glance

```
[start] Phase 0 define -> Phase 1 check
                              │
              ┌───────────────┴───────────────┐
            GREEN                             RED
              │                                │
        log, stay quiet              breaker open? ── yes ─> notify, wait for human
              │                          │ no
              │                   record-recovery -> diagnose -> fix (in scope)
              │                          -> verify -> resolve / notify
              └───────────────┬───────────────┘
                              ▼
            Phase 3 reschedule -> [next check]
```

## Before you ship a monitor: self-test

Run the wiring test so you don't end up with a system that *looks* healthy but whose
recovery chain never actually fires:

```bash
python scripts/selftest.py            # verifies check / notifier / breaker / resolve
python scripts/selftest.py --check-claude   # also confirms the claude CLI answers
```

## Safety (read before enabling autonomous fixes)

Autonomous fixing is genuinely risky: a wrong fix propagates fast, and an agent can even
revert a security patch it misreads as drift. Keep it safe by construction:
- **Diagnose-only is the default.** The headless daemon only fixes with `--auto-fix`/`auto_fix`.
- Keep `fix_scope` tight and concrete. Reversible actions only by default.
- Set `git_repo` when auto-fix may touch code, so a failed fix rolls back instead of piling up.
- Let the **circuit breaker** and **human escalation** be the backstop — never remove them.
- For destructive / irreversible actions (DB writes, deletes, rollbacks, security config),
  report and require a human. Don't improvise.
- Run `scripts/selftest.py` before trusting a monitor — prove the recovery chain isn't silently dead.
