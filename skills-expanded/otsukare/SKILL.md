---
name: otsukare
description: Use when starting a long or token-heavy task that could exhaust the Claude Code 5-hour or 7-day usage limit mid-run, or any long unattended run that must survive a usage-limit pause and pick the work back up afterward. Triggers on "otsukare", "watch my usage", "pause if I hit the limit".
---

# otsukare — usage-limit guardrail

お疲れ — "good work, go rest," then pick the work back up. Invoke this at the **start** of a long or token-heavy task. otsukare does **not** do the work itself; it wraps it in a guardrail that watches the 5h/7d rate limits, pauses safely before a limit is exhausted, and auto-resumes just after the limit resets. Its first job is **never letting usage cross 100% mid-turn** — the one state no scheduled resume can punch through (see *Dispatch gate*); the safety-net cron backstops everything else.

> **Prerequisite:** otsukare can only see your usage if your statusline mirrors it to the
> data file — `last-statusline-input.json` in your Claude config directory. See the project
> README ("Expose your limits to your local agent"). If that file is missing, tell the user
> and stop — otsukare is blind without it.

## Constants (edit to taste)

- Helper: `<HELPER>` — the absolute `otsukare_usage.py` path you pin at preflight (see *Resolve your tools once* below)
- Data file (read-only): the `mirror` path returned by `--resolve-paths` (the statusline rewrites it on every render)
- State dir: the `state_dir` returned by `--resolve-paths` — holds the checkpoint, the `<session_id>.heartbeat`, and the `<session_id>.state.json` run-metrics file
- `SOFT=90`/`HARD=97` for the 5h window; `SOFT_7D=95`/`HARD_7D=98` for the 7-day window (laxer on purpose — 5% of a week is 8+ hours of runway, where 10% of 5h is ~30 min)
- `STALE_BUFFER=8`, `STALE_AGE=120s`, `RESUME_OFFSET_MIN=10`, retry tick `every 5 min`, `HEARTBEAT_STALE=15min`

The helper already applies `SOFT`/`HARD`/`STALE_BUFFER`/`STALE_AGE`/`RESUME_OFFSET_MIN`; override via `--soft`, `--stale-buffer`, etc. or `OTSUKARE_*` env vars if needed.

## Hard constraint on the wrapped work

**Do not dispatch `run_in_background` subagents during an otsukare run.** Background agents return control immediately and finish later, so you cannot block on them at a seam — their output could land after the checkpoint and be lost. Use **foreground/blocking** subagents only, so "let in-flight subagents finish" is actually enforceable. If a background agent is unavoidable, record its task ID in the checkpoint and reconcile it in resume mode.

## Dispatch gate — size every subagent wave by headroom

Seam checks only run **between** waves, so a parallel batch is one unmonitored token commitment: dispatch 8 agents at 80% and nothing can stop the run crossing 100% mid-batch. At 100% mid-turn Claude Code shows the interactive "limit reached — wait or upgrade" picker; while it is up the REPL is not idle, **no scheduled prompt can fire**, and even the armed safety net is blocked until a human presses *Wait*. The gate exists to make that state unreachable.

**Before every subagent dispatch** — not only at seams — take `max_wave` from the helper's decision JSON (reuse the seam check you just ran; run `<PY> <HELPER>` fresh only if the last reading predates this seam) and dispatch **at most `max_wave`** subagents, holding the rest for later waves. `max_wave: 0` means dispatch nothing — act on `decision` instead. The helper derives it from the soft-threshold headroom in tested code (tighter usage → narrower waves: margin >20 pts → 4, >10 → 2, >0 → 1, else 0), honoring any `--soft`/env overrides.

A wave already in flight cannot be checked, drained early, or stopped safely — the gate runs **before** dispatch, never after. Splitting one wide wave into several narrow ones barely costs wall-clock (each wave still runs in parallel internally) and converts an unmonitored bet into checkpoints.

## At start (preflight, refresh, then arm the safety net)

**Resolve your tools once, reuse them below.** Different OSes expose Python under different names and PowerShell does not expand `~`, so pin these tokens before running anything else and reuse them verbatim:

- `<PY>` — your Python launcher. Try `py` (the Windows launcher), then `python3`, then `python`; keep the FIRST whose `--version` exits 0. Never run a bare interpreter with no script — it opens a REPL or, on Windows, hits the dead Microsoft Store stub.
- `<HELPER>` — the absolute path to `otsukare_usage.py`, i.e. `<skills-dir>/otsukare/scripts/otsukare_usage.py` with any `~` already expanded.
- `<state>` / `<heartbeat>` / `<checkpoint>` — once Step 0 confirms otsukare applies, run `<PY> <HELPER> --resolve-paths --session-id <session_id> --task-slug <task-slug>` **once** and keep the returned absolute paths (the call also emits `home`, `state_dir`, and `mirror`). Take `<session_id>` from the statusline mirror blob and `<task-slug>` from a short kebab of the task. Use these tokens everywhere below — never write a `~/...` path by hand.

**Step 0 — confirm otsukare even applies here.** It only guards subscription 5h/7d limits:
```
<PY> <HELPER> --preflight
```
- `applicable: true` → continue.
- `applicable: false` → **show the user the `message` verbatim and STOP** — do not arm, checkpoint, or wrap anything. Reasons: `no_rate_limits` = an API / usage-billed plan (metered per token, no rolling windows) — otsukare has nothing to guard; `no_mirror` = the statusline mirror isn't wired (see README); `stale` = the mirror isn't updating.

Once applicable, set up the dead-man's switch so a sudden usage spike that hard-cuts the session still auto-resumes:

1. **Block until usage is fresh** — do this FIRST. It is the guard against reading a stale reset/usage left by a previous session or window:
   ```
   <PY> <HELPER> --wait-fresh
   ```
   This blocks (up to 30s) until the statusline has re-rendered the mirror file with a **current 5h window** (reset in the future), then returns `{"fresh": true, "resets_at": <epoch>, ...}`. The statusline re-renders every few seconds while the session is active, so this normally returns in under a second.
   - `fresh: true` → proceed; the subsequent `--arm` and decision reads now see current data.
   - `timed_out: true` / `fresh: false` → the mirror isn't updating (statusline not wired, or the session is idle). **Tell the user** usage couldn't be refreshed, then proceed on the conservative path (`--arm` will return `provisional: true` and the first seam will re-point it).

   Never read the plain decision/`--arm` for the initial reset time without clearing this barrier first.
2. **Write the initial checkpoint** to `<checkpoint>` (the path you resolved above). Use the template in *Pause protocol* step 3, filling Goal / Session ID / Task slug / cwd / branch and leaving Done/Next to be updated at each seam.
3. **Bump the heartbeat:** `<PY> <HELPER> --touch-heartbeat <heartbeat>`
4. **Initialize run metrics** (baselines for the end-of-task summary):
   ```
   <PY> <HELPER> --state <state> --state-action init --task "<task name>"
   ```
5. **Arm the safety-net cron.** Get the target + cron string:
   ```
   <PY> <HELPER> --arm
   ```
   This prints `{"safety_target": epoch, "cron": "<minute-list> H D M *", "provisional": bool, ...}`. Call the **`CronCreate`** tool with `cron` = that string, `recurring: true`, and `prompt` = the resume prompt (see *Schedule the resume*). Record the returned job ID in the checkpoint. If `provisional: true`, note that the first seam will re-point it.

   The job is session-only — do not pass `durable`, it has no effect (see *Notes & guards* for what in-memory scheduling means for quits and reboots).

Then begin the work.

## Run loop

Do the wrapped work in steps, sizing every subagent wave with the **Dispatch gate** above. After each **natural seam** — a foreground subagent wave returns, a plan/todo step completes, or you make a commit (never mid-edit) — do a seam check:

1. **Emit a one-line seam note** to the user, e.g. `✓ step 3/8 done — checking usage`. This is required, not cosmetic: emitting text triggers a statusline render, which refreshes the data file so the next read is fresh.
2. **Update progress + heartbeat:** rewrite the checkpoint's `## Done` / `## Next`, then bump the heartbeat — `<PY> <HELPER> --touch-heartbeat <heartbeat>`.
3. **Run the helper:**
   ```
   <PY> <HELPER>
   ```
   It prints JSON: `{"decision": "...", "now": epoch, "stale": bool, "stale_window": bool, "margin": pts|null, "max_wave": 0-4, "limits": {...}, "binding_resets_at": epoch|null, "resume_target": epoch|null}`.
4. **If `stale_window` is `true`, the reading is from an already-reset window — refresh before trusting it.** A `resets_at` at or before `now` means the mirror still holds a *previous* window's blob (its usage % is pre-reset and no longer applies), so the helper has flagged that limit `rolled` and ignored its percentage. This is exactly the "it paused at 97% right after the limit reset" failure. Block for a fresh render and re-read, then act on the refreshed decision:
   ```
   <PY> <HELPER> --wait-fresh
   <PY> <HELPER>
   ```
   If `--wait-fresh` still times out (`fresh: false`), the statusline isn't updating — **do not pause on the stale numbers**; keep working and re-check at the next seam.
5. **Re-point the safety net if the 5h window rolled.** If `limits.five_hour.resets_at` is later than the currently-armed target minus the offset (or the armed target was provisional), `CronDelete` the old job and re-arm via `--arm` so the net always points at the next reset. Update the job ID in the checkpoint.
6. **Act on `decision`:**
   - `continue` → keep working.
   - `soft` → if the remaining work is **near a finish line** (last step, or one more small foreground batch), push through to finish — but re-check at every seam and **never** cross `hard`. If **substantial work remains**, run the **Pause protocol**.
   - `hard` → run the **Pause protocol** at this seam, no exceptions.

If `stale` is `true` (file is old but the window is still current), the helper has already added `STALE_BUFFER` to the effective usage (it rounds against you). Trust the decision. `stale_window` is the *different* case above — an expired window whose percentage is discarded, not buffered.

## Pause protocol

When otsukare decides to pause proactively:

1. **Drain, never hard-kill.** Stop dispatching new subagents; let the current foreground subagent finish (control returns naturally). Do **not** `TaskStop` mid-work.
2. **Reach a clean seam.**
3. **Finalize the checkpoint** `<checkpoint>`:
   ```markdown
   # otsukare checkpoint — <task-slug>

   - Goal: <original request, 1-2 sentences>
   - Session ID: <session_id>
   - Task slug: <task-slug>
   - Absolute cwd: <`git rev-parse --show-toplevel`; or the session's known absolute cwd if not in a git repo — absolute, forward-slash form>
   - Branch: <output of `git rev-parse --abbrev-ref HEAD`>
   - WIP SHA: <filled in step 4, after the commit>
   - Binding limit: <five_hour|seven_day>, resets_at <epoch> (<local time>)
   - Resume target: <resume_target epoch> (<local time>)
   - Safety-net cron job ID: <id>
   - Outstanding background agents: <task IDs, or "none">

   ## Done
   - <completed steps>

   ## Next
   - <remaining steps, in order>
   ```
4. **Commit WIP** and record the SHA into the checkpoint:
   ```
   git add -A
   git commit -m "wip(otsukare): checkpoint before usage pause"
   git rev-parse HEAD   # paste into the checkpoint's "WIP SHA" line
   ```
5. **Re-point the safety net to the binding reset** if it differs from the armed target (e.g. the 7d limit binds, days later): `CronDelete` the old job, then `CronCreate` with the cron from `--cron-for <resume_target>`. Update the job ID in the checkpoint.
6. **Record the pause in run metrics:**
   ```
   <PY> <HELPER> --state <state> --state-action pause --pct <current 5h used %>
   ```
7. **Notify** (single message): current used %, where you stopped, the checkpoint path, the binding limit, and the resume target as **local time**.

### Schedule the resume

The resume prompt used by both the safety-net cron and the proactive re-point:

> `otsukare resume mode. Checkpoint: <checkpoint>. Binding reset epoch: <binding_resets_at>. Invoke the otsukare skill and follow its Resume mode section.`

Embed the **absolute** checkpoint path (the resolved `<checkpoint>`) directly in the prompt — by fire time the context may have been compacted, so the prompt must carry everything needed to re-load the skill and find the checkpoint on its own.

For the proactive re-point, get the cron string with:
```
<PY> <HELPER> --cron-for <resume_target>
```
It prints a bounded retry window (e.g. `10,15,...,55 H D M *`) — every 5 min, but only **at or after the target** on the target date, rolling to the next hour when the target lands late in its own hour. Ticks never fire before the reset: each fired prompt re-reads the whole session context, and doing that at 97%+ in the not-yet-reset window could itself push usage to 100%.

## Resume mode

When a scheduled prompt fires (either the safety net or a proactive re-point):

**First, re-pin your tools and paths.** The prompt fires back into this same session, but hours may have passed: the context may have been compacted away and the cwd/branch may have drifted — trust only the checkpoint, not memory. Re-resolve `<PY>` and `<HELPER>` exactly as at preflight, then recover the original run's paths: the prompt carries the checkpoint's absolute path, so open it and read its `Session ID` and `Task slug` fields, then run `<PY> <HELPER> --resolve-paths --session-id <session_id> --task-slug <task-slug>` to get back `<heartbeat>` / `<state>` / `<checkpoint>`.

1. **Is the work still alive?** Check the heartbeat:
   ```
   <PY> <HELPER> --heartbeat <heartbeat>
   ```
   It prints `{"alive": bool, "age_seconds": ...}`.
   - `alive: true` → the main run is still going; **exit quietly** (it will handle its own pausing). Let the next tick re-check.
   - `alive: false` (or checkpoint missing / marked complete) → proceed to take over. If the checkpoint is missing or its `## Next` is empty, `CronDelete` the job and exit — nothing to resume.
2. **Confirm the limit actually cleared.** First block for a fresh render so you don't read a pre-reset file, then run the clear-check:
   ```
   <PY> <HELPER> --wait-fresh --wait-timeout 20
   <PY> <HELPER> --resume-check <binding_reset_epoch>
   ```
   - `{"status":"wait","reason":"stale_pre_reset"}` or `"stale_window"` → **stop**; the stale reading self-resolves, so the next retry tick just re-checks.
   - `{"status":"wait","reason":"still_over", ...}` → usage cannot drop until the *next* reset (it only rises within a window), so the remaining ticks this hour are pure waste: `CronDelete` the current job, `CronCreate` at the returned `resume_target` via `--cron-for` (fall back to `--arm` in the rare case it is null), update the checkpoint's job ID, and **stop**.
   - `{"status":"clear", ...}` → **take over.** First `CronDelete` the job that fired (ID in the checkpoint) so leftover ticks don't queue wasted turns behind the resumed work — a fresh net is re-armed in the last step.
3. **Re-establish context** (a cron prompt fires in whatever cwd/branch the REPL holds):
   - `cd` to the checkpoint's recorded **absolute cwd**.
   - `git checkout <branch>`. If the working tree has uncommitted WIP from a hard cut, commit it with `git add -A` followed by `git commit -m "wip(otsukare): recovered uncommitted work"` (two separate commands; PowerShell rejects `&&`). Then verify the base is sane; if the recorded **WIP SHA** is set, confirm `git rev-parse HEAD` is that SHA or a descendant of it. If the branch/state is clearly wrong, **abort and report** — do not continue on the wrong base.
   - If the checkpoint lists **outstanding background agents**, reconcile them now: `TaskOutput` each ID, fold finished results into `## Done`, and put lost or unfinished ones back on `## Next`.
4. **Reload** the `## Next` list from the checkpoint.
5. **Record the resume in run metrics.** `<state>` is keyed by the **original** `session_id` (re-resolved above from the checkpoint), so a dead-man's-switch takeover still updates the same metrics:
   ```
   <PY> <HELPER> --state <state> --state-action resume
   ```
6. **Notify** (one line): `resuming <task>, 5h now at X%`.
7. **Re-arm** a fresh safety net for the new window (`--arm` + `CronCreate`, recording the new job ID in the checkpoint) and **continue** the work from `## Next`, re-entering this run loop.

## On completion (summary + cleanup)

When the wrapped work finishes:

1. **Print the run summary** — continues, run time, tokens, and cost, all measured as the delta over the otsukare span:
   ```
   <PY> <HELPER> --state <state> --state-action summary
   ```
   Show its output to the user verbatim, e.g.:
   ```
   お疲れ! otsukare summary — <task>
     Continued:  2× (91%, 96%)
     Run time:   4h 18m total · 1h 51m active · 2h 27m waiting
     Tokens:     412K in/out · 4.1M cache (4.5M total)
     Cost:       $3.84
   ```
   (If the run never paused, `Continued: 0×` — still a tidy receipt of time/tokens/cost.)
2. `CronDelete` the safety-net job (using the ID in the checkpoint).
3. Mark the checkpoint done — delete `<checkpoint>` or write `STATUS: complete` at the top.
4. Remove the heartbeat and state file: `<PY> <HELPER> --cleanup --heartbeat <heartbeat> --state <state>`.

A run that never hits a limit thus creates the safety-net job at start and deletes it at the end — **net zero lingering jobs.**

## Notes & guards

- The data file updates only when the statusline renders; in practice that is every few seconds while the session is active. The **`--wait-fresh` barrier** at start and resume blocks until a render lands with a current 5h window, so the initial reset time is never read from a stale file. For mid-run seam reads, the helper guards itself: usage within a window only rises, so an *old-but-current-window* file (`stale: true`) is handled by the stale buffer, while an *expired-window* file (`stale_window: true`, `resets_at` ≤ now) has its pre-reset percentage discarded rather than buffered — so a read taken right after a reset can never force a false pause. When `stale_window` is true, refresh via `--wait-fresh` and re-read to get the new window's real usage.
- Usage is **account-global** — it reflects whichever session rendered last. That is why resume mode requires the file to be fresher than the reset before trusting "cleared."
- If both 5h and 7d are over threshold, the helper binds to the **later** reset (you must wait for both).
- The **safety net** is the failsafe for a sudden swarm-to-100% that hard-cuts the session before a seam: it is armed up front, so a resume is scheduled even if the pause protocol never runs. The **heartbeat** ensures it only takes over when the main run is actually dead, never duplicating a live session.
- **If the user ever sees the "limit reached — wait or upgrade" picker** (usage crossed 100% mid-turn despite the *Dispatch gate*), they should choose **Wait**: the session survives, and once the REPL is idle again the armed net fires on its next tick or re-points itself via the still-over path.
- Scheduled jobs are **session-only and in-memory**: quitting Claude Code, a reboot, or sleeping past the fire time silently kills them — keep the terminal open and the machine awake for unattended runs. The checkpoint file survives regardless; pasting the resume prompt (checkpoint path + binding epoch, both recorded in it) into a new session recovers the run by hand — and with the optional **SessionStart hook** wired (README, `scripts/session_hook.py`), the next launch detects the orphaned checkpoint and offers the resume automatically.
- `session_id` comes from the mirror, which is written by whichever session rendered last — with two concurrently-active sessions it can be the other session's. Do not run two otsukare-wrapped sessions at once.
- If there is no work left when a pause would trigger, just finish normally — run the cleanup, no resume scheduled.
