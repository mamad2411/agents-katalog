---
name: workdesk-doctor
description: Verifies WorkDesk OS runtime behavior (hooks, locks, latency, session-end export) that filesystem self-check cannot see. Run on first Claude Code session after bootstrap, and any time something feels off. Onboarding pauses until doctor passes.
---

# /workdesk-doctor

Bootstrap is filesystem-only. Doctor proves runtime. Run after every bootstrap, after every `config/settings.json` edit, and any time a hook seems wrong.

## When to run

- First Claude Code session after bootstrap
- After editing `config/settings.json` or any hook script
- When `/onboarding` reports an environment-check failure
- Any time a hook fires unexpectedly or doesn't fire when expected

## Phases

### 1. PreToolUse personal-lock (config inspection — never probe by writing)

`personal/` is operator-only. The doctor MUST NOT attempt to write, edit, or mutate any path under `personal/` — even probes that expect denial. The lock is for the operator's data, not Claude's diagnostics. Verify by inspecting configuration instead:

1. Read `config/settings.json`. Confirm `hooks.PreToolUse` includes an entry whose matcher covers `Write`, `Edit`, `MultiEdit`, and `Bash`, and whose command points to `config/scripts/pre-tool-use-personal-lock.sh`.
2. Confirm `config/scripts/pre-tool-use-personal-lock.sh` exists, is executable (`test -x`), and parses (`bash -n`).
3. Read the hook script and confirm it pattern-matches paths under `personal/` in tool input (covers `Write`/`Edit`/`MultiEdit` `file_path`, and `Bash` commands targeting `personal/`).

If all three pass, record `pre-tool-use-personal-lock: pass`. If any fails, record `pre-tool-use-personal-lock: fail` and name which check failed.

Runtime correctness is demonstrated when the hook fires on real operator workflows — not by synthetic probes from the doctor.

### 2. PostToolUse semantic logging

Write a synthetic atlas note (e.g., `atlas/meetings/_doctor-probe.md`) and verify:

- `system/events/{YYYY-MM}.md` gains an `object-created` line
- The line includes the timestamp, event class, target, and result

Then delete the probe and the event line.

### 3. SessionStart scan

Read `config/state/session-entry.md`. Verify it was written within the last 5 minutes (proof the hook fired this session). If absent or stale, the hook is broken or `config/settings.json` is misconfigured.

### 4. SessionEnd vs Stop fallback

Decide which raw session-log path is active. Procedure:

- Look in `system/session-log/` for `*-raw.md` files written in the last 24 hours
- Count files per `session_id`
- If multiple files share a `session_id` and any has `complete: false`, `Stop` upsert mode is active — write `config/state/doctor.md` with `stop-fallback: enabled`
- If files appear only at session end with `complete: true`, `SessionEnd` is active — write `stop-fallback: disabled`

### 5. Hook latency

Run `config/scripts/bench-hooks.sh` (always — even when invoked silently from `/onboarding` Phase 0). Capture stdout and parse the `p95: NNms` line; record the integer milliseconds. If p95 exceeds the 50ms budget, record it as a warning — do NOT fail the overall doctor run. Hook latency is a perf signal, not a correctness invariant; cold-cache first runs can exceed the budget without any user-visible problem.

Never write `unmeasured` to `hook-latency-p95-ms`. Either run the script and record a number, or record `fail` with the underlying error. Skipping is not acceptable.

### 6. Session-entry intake scan

Confirm `config/state/session-entry.md` reflects current `system/transcripts/`, `system/intake/`, and `system/session-log/` reality:

- Drop a synthetic `system/transcripts/_doctor-probe.md` with `processed: false`
- Trigger a fresh scan (re-source the script directly, since you're already in-session)
- Verify the probe shows up in `unprocessed.transcripts`
- Delete the probe

### 7. Obsidian defaults drift

Verify the operator's vault `.obsidian/*` matches the canonical `config/obsidian-defaults/*` shipped with the current release. Drift here is the most common cause of "the calendar button creates a blank note in the wrong folder."

For each file under `config/obsidian-defaults/` (excluding `README.md`):

1. Compute target path: `<vault>/.obsidian/<relative-path>`.
2. If the target is missing, record drift: `missing: <path>`.
3. If the target exists, parse both as JSON (these are all `.json` files) and compare. Record any key mismatches as `drift: <path> <key>`.

Record results as:

- `obsidian-defaults-drift: pass` — all canonical files present and matching.
- `obsidian-defaults-drift: fail` — at least one drift; list the specific paths/keys in the chat summary.

This is a soft fail — don't block the doctor's overall pass/fail on it. Surface it as a warning with the repair: "Run `/update` to refresh `.obsidian/` from the canonical defaults. Takes effect on next Obsidian launch."

## Output

Write `config/state/doctor.md`. Always run all 7 phases — invocation from `/onboarding` Phase 0 means do not narrate, but does not mean skip checks.

Compute the timestamp via `Bash date '+%Y-%m-%d %H:%M'` and use that exact string as `last-run:`. Never use placeholder strings like `session-start`, `today`, or `now`.

```yaml
---
last-run: 2026-04-30 09:30
result: pass | fail | partial
checks:
  pre-tool-use-personal-lock: pass | fail
  post-tool-use-event-log: pass | fail
  session-start-scan: pass | fail
  session-end-or-stop-fallback: SessionEnd | Stop
  hook-latency-p95-ms: 12
  session-entry-intake-scan: pass | fail
  obsidian-defaults-drift: pass | fail
stop-fallback: enabled | disabled
---
```

Then summarize in chat:
- Pass: "Runtime green." (One line. Don't suggest the next skill — `/onboarding` invokes doctor inline; standalone doctor runs are diagnostic, not handoffs.)
- Fail: list each failed check with the exact repair command. Pause until operator reruns.

## What NOT to do

- Don't proceed past a fail. Failed runtime is the whole point of this skill.
- Don't summarize without writing `config/state/doctor.md` — onboarding reads that file.
- Don't write, edit, or `Bash`-mutate any path under `personal/` — ever, for any reason. The personal-lock is verified by config inspection (Phase 1), never by attempting writes that expect denial.
- Don't skip phases when invoked from `/onboarding` Phase 0. Silent means no narration; all 6 phases still run.
- Don't write placeholder strings to `last-run:`. Real timestamp via `date` only.
