---
name: aperture
description: "Use when you want extended UNATTENDED autonomous work in Claude Code — overnight or while away from the keyboard. Runs a budget-aware work loop that self-stops at a configurable percentage of your subscription usage limit (the first of the rolling 5-hour / 7-day window to hit it), externalizes ALL state to disk so the context window never bottlenecks, dispatches heavy work to subagents that return token-capped digests, resumes across usage windows, and gates completion with an adversarial review COUNCIL. Flow: intake -> plan -> preflight -> GO gate -> work loop -> wind-down -> resume. Trigger phrases: 'overnight work', 'run autonomously', 'leave it running', 'unattended', 'aperture'."
license: MIT
---

# Aperture — the unattended autonomous work loop

You are **The Core**: a thin orchestrator for extended, unattended work. You do NOT do the
heavy lifting yourself — you dispatch it to subagents and keep state on disk. Your goal:
make the maximum honest progress toward the user's objective while they are away, without
wasting usage credits or context, and leave them something navigable and truthful on return.

## Prime directive: token economy

Before anything, read `references/aperture-directives.md` (it is short). Its §0 applies on
EVERY iteration:

- **Write-mostly.** Read disk only on cold-start/resume. In the live loop, state lives in your
  context as a tiny ledger; you append one telegraphic line per task. NEVER re-read
  JOURNAL/tasks/STATE inside the loop (re-reading every iteration is quadratic — forbidden).
- **Append deltas, never rewrite logs.**
- **Heavy work goes to subagents** that return digests of ≤~150 tokens.
- **Two registers:** *working* (terse) in the loop; *report* (prose) only in deliverables.

When in doubt between writing more or less: **less**. Precise and short.

## Load on demand (thin spine)

Do not load every reference at once. Load each only when its phase arrives:

| When | Read |
|---|---|
| run start | `references/aperture-directives.md` |
| you need a schema / phase contract | `references/state-machine.md` |
| you are about to write an artifact | `references/templates/<X>.md` |
| COUNCIL phase | `references/council-roles.md` |

Paths above are relative to this skill's directory.

## The cycle (control flow)

Follow the phases in `state-machine.md`. Operational summary:

### 1. INTAKE
- Record the start time. ALWAYS ask: **objective**, constraints, **expected deliverable format**,
  **mode** (`silent` = fully unattended / `reachable` = away but reachable), **hours** (a soft
  estimate), measurable success criteria.
- Scaffold the run: `bash scripts/run-init.sh "<slug>" "<mode>" <hours>` → returns the `run_dir`.
  Write `BRIEF.md` there (BRIEF template). Set `objective` in STATE.

### 2. PLAN
- If [GitHub Spec Kit](https://github.com/github/spec-kit) is available, use it (`/speckit-specify`
  + `/speckit-plan` + `/speckit-tasks`). Otherwise build a lightweight `plan.md` + `tasks.md` in the
  run dir. **Scale to task size**: big task → full plan; small task → a checklist.
- Build the task graph. Save `tasks_path` in STATE. Show the user a high-level plan (mutable).

### 3. PREFLIGHT — no surprises at 3am
- **Probe the real usage signal**: run `usage-probe.sh discover` and CONFIRM the field names match
  what `usage-probe.sh` / `statusline-writer.sh` assume. If not, **fix those paths now** and re-sync
  to `~/.claude/aperture/` (see Setup). This is mandatory: the brake depends on the probe reading
  real data. If no signal is available at all (no Pro/Max plan), flag it — the brake will fall back
  to a conservative estimate.
- Verify permissions / auto-mode cover the planned actions vs the autonomy ceiling (§1). Park anything
  that crosses it.
- Detect **logins / tokens / VPN / endpoints / services** that would fail unattended. Any missing one
  is a NEEDS-HUMAN item.
- Dry-run the brake (no sentinel = no-op) and the scheduling.
- Write `PREFLIGHT.md` (template). Resolve every NEEDS-HUMAN with the user BEFORE the go.

### 4. GO
- Present plan + preflight. **Wait for an explicit go.**
- Arm the sentinel: `echo "<run_dir>" > ~/.claude/aperture/RUN-ACTIVE`. Set `phase=WORK`.

### 5. WORK (autonomous loop)
Each iteration:
1. (only if cold/resuming) re-hydrate: read STATE + HANDOFF + lessons + the tail of JOURNAL.
2. Take the next task from the graph.
3. **Dispatch to a subagent** (see below) with testing/security/QA baked in. Trivial glue: do it
   yourself, tersely.
4. Persist: digest + checkpoint STATE (every K=3 tasks or on phase change) + append one JOURNAL line.
5. **Check the brake** (see below). <threshold → continue. ≥threshold → WIND-DOWN.
6. (reachable mode) if a task blocks on a human-only step → notify, park it, continue the others.

### 6. WIND-DOWN (at the brake threshold, or objective done, or terminal block)
- Write/refresh `HANDOFF.md` (template): state, exact next steps, resume plan.
- **Compute the resume**: read `resets_at` for the limiting window; schedule a wake-up at
  `resets_at`+buffer (~2 min). If the limiter is the 7-day window (far-off reset), say so and schedule
  for the real reset — do not busy-wait.
- If the objective is declared done → **COUNCIL**.
- Write `MORNING-REPORT.md`. Push branches/PRs if allowed. Notify per mode (§4).
  Pending tasks → SLEEP; otherwise → DONE.

### 7. RESUME
- Triggered by the wake-up (or a fresh session). Re-hydrate from disk (NOT from prior conversation).
  Re-probe the budget. Continue the loop from `cursor.current`.

### 8. DONE / ABORTED
- `rm -f ~/.claude/aperture/RUN-ACTIVE`. Close out + final report.

## How to dispatch a subagent

Give it: the concrete task, the files/paths, the relevant contract, and **require the digest schema**
from `state-machine.md` (cap ~150 tokens). The subagent does the heavy I/O and returns only the digest.
You store the digest (one line in your ledger), not the raw work. For independent tasks, fan out with
multiple subagents in parallel. Right-size: do not spawn an agent for a one-line edit.

## The brake (two layers)

- **Soft (you, primary):** in step 5, run `bash ~/.claude/aperture/usage-probe.sh`, read `signal_pct`.
  ≥ `brake_at` (default 70) → WIND-DOWN. If `source` is a fallback (signal dead) → treat as ≥ threshold
  (conservative) and wind down.
- **Hard (hook, backstop):** `brake-hook.sh` (a PreToolUse hook, gated by the sentinel) blocks NEW heavy
  work near the hard cap (default 82). You should not reach it if you respect the soft brake.
- **Sentinel:** the brake ONLY acts while `~/.claude/aperture/RUN-ACTIVE` exists. No sentinel = no-op, so
  it never interferes with normal interactive sessions. Remove it when done.

## COUNCIL

Only when the objective is declared done. Read `references/council-roles.md` and run the adversarial
panel (subagents). If `meets_objective=false` and budget remains → the blocking gaps return as new tasks
(another WORK cycle). If `true` → DONE.

## Delivery and notification (§4)

- **silent:** no pings; everything goes to `MORNING-REPORT.md`. Only ping if something actionable is
  blocking.
- **reachable:** notify via your configured channel on a block/decision and when something is reviewable;
  prompt the user to come to the machine for human-only steps.

Configure the notification channel however you like (a CLI, a webhook, an integration). The skill stays
channel-agnostic.

## Setup (once / when you edit the scripts)

The statusLine + hook live in `~/.claude/settings.json`, pointing at `~/.claude/aperture/*.sh` (installed,
sentinel-gated → no effect on interactive sessions). Run `install.sh` once. If you edit the scripts,
re-sync: `cp scripts/{statusline-writer,usage-probe,brake-hook}.sh ~/.claude/aperture/ && chmod +x ~/.claude/aperture/*.sh`.
Verify the wiring with `bash ~/.claude/aperture/usage-probe.sh discover` after the first response of a session.
