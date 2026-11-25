---
name: sprint-execute
description: Execute planned sprints from .ai/sprints in the current session. Sister skill to sprint-plan. Use when asked to start, continue, execute, implement, finish a sprint, keep executing sprints, drain the sprint queue, or finish all remaining sprints.
---

# Sprint Execute

Run this skill directly in the current session. You are the implementation orchestrator — read the latest incomplete/planned sprint, make the changes, validate, drive review, and stop only when the sprint is genuinely implemented or blocked. This is the execution sister to `sprint-plan`; reuse its state conventions and Agent Availability check.

```
0 select → 1 orient → 2 slice → 3 implement → 4 validate → 5 review → 6 closeout → 7 persist
```

Numbers map to the stage sections below. Stage 4 failures and Stage 5 `rework` verdicts loop back to stage 3 (implement). A Stage 5 `fail`/`blocked` verdict instead routes forward to Stage 7 (persist) to record the blocker. Stage 6 gaps keep status `implementing` with continuation notes rather than transitioning stages. By default, run one selected sprint. If the user asks to "keep executing", "finish remaining sprints", "drain the queue", or equivalent, enable queue-drain mode.

## State Files

Execution state lives beside planning state and is append-only where possible:

```
.ai/sprint-execution/current.env
.ai/sprint-execution/progress.log
.ai/sprint-execution/SPRINT-<NNN>-execution.md
.scratch/verification/SPRINT-<NNN>/
```

`current.env`:
```
SPRINT_ID=<NNN>
SPRINT_TITLE=<title>
SPRINT_STATUS=implementing|implemented|blocked
SPRINT_SOURCE=.ai/sprints/SPRINT-<NNN>.md
SPRINT_STARTED_AT=<UTC ISO-8601>
SPRINT_UPDATED_AT=<UTC ISO-8601>
```

`progress.log` — append-only, tab-separated:
```
<UTC ISO-8601>	<NNN>	<event>	<detail>
```

## Stage 0: Select Sprint

Pick exactly one sprint, in priority order:

1. `.ai/sprint-execution/current.env` exists with status `implementing` → continue it.
2. Scan `.ai/sprints/SPRINT-*.md` numerically and select the first sprint not marked `implemented` in `.ai/sprint-execution/progress.log`, `.ai/sprint-state/history.log`, `.ai/sprint-execution/current.env`, or `.ai/sprint-state/current.env`.
3. If the scan is ambiguous, `.ai/sprint-state/current.env` may be used as a tie-breaker only when it points at an existing unimplemented sprint file.

`.ai/sprints/SPRINT-*.md` is the canonical queued work set. Multiple planned sprint files may exist while another sprint is executing. Do not treat `.ai/sprint-state/current.env` as the only queued sprint; it is a planning pointer and may refer to the most recently planned future sprint rather than the next execution target.

Verify the chosen `SPRINT-<NNN>.md` is self-contained (not a pointer) and carries the full template sections: Objective, Current State Evidence, Coding Agent Availability, Scope, Non-Goals, Implementation Plan, File and Module Map, Validation Plan, Risks and Fallbacks, Definition of Done, Closeout Checklist. If none can be selected, say so and stop.

In queue-drain mode, Stage 0 is repeated after each completed sprint. Rescan the filesystem and logs fresh each time; do not cache the queue from the beginning of the run. This allows newly planned sprints that appear while execution is in progress to be picked up in the same session.

## Stage 1: Orient

Read the selected sprint completely, then inspect the repo before editing: `git status --short`, files in the File and Module Map, tests/scripts in the Validation Plan, and relevant docs/config. Respect dirty worktrees — never revert unrelated user changes; work with existing changes in sprint-targeted files.

Create or update `SPRINT-<NNN>-execution.md` with: sprint path and objective, repo evidence that changes the plan, implementation slices, validation commands, risks/blockers, and a running closeout checklist.

## Stage 2: Slice

Break the Implementation Plan into small slices, each independently reviewable and testable where practical. Per slice record goal, files touched, intended tests, done condition, and dependencies. Prefer dependency order over plan order. If the sprint is too large for one session, do the earliest unlocking slice and leave precise continuation notes.

## Stage 3: Implement

Implement slices directly. Rules:

- Stay within the File and Module Map; follow existing style, helpers, and test patterns.
- Add abstractions only where the sprint requires repeated behavior or a clear contract.
- Keep security-sensitive behavior server-authoritative — UI hiding is never enforcement.
- Don't count fake/mock/demo data as acceptance unless the sprint explicitly calls for test fixtures.
- Preserve local-dev compatibility unless the sprint removes it.
- Briefly state the edit direction before touching files.

Use subagents for parallel read-only inspection. Use external coding agents only for bounded artifacts you can verify locally — never outsource final judgment or merge.

## Stage 4: Validate

Validate early and often, in order: narrow tests for the changed slice → relevant Validation Plan commands → broader workspace checks before closeout. Save evidence (transcripts, smoke logs, screenshots, curl output, deploy URLs/status) under `.scratch/verification/SPRINT-<NNN>/`. If a command can't run, record why. On failure, return to Stage 3.

## Stage 5: Review

When external agents are available (see Agent Availability in `sprint-plan`), run a multi-agent review of the implementation against the sprint's Definition of Done. Otherwise the orchestrator performs the review directly and notes the single-lane fallback. If the user asks you to skip the review, skip it and move on to Stage 6.

1. **Reviews** — each available agent independently returns a PASS/FAIL verdict with reasoning and required fixes, covering checklist completion, implementation correctness, regression risk, and validation evidence.
2. **Cross-critiques** — each agent critiques the other agents' reviews for missing checks, weak evidence, or wrong conclusions.
3. **Synthesis** — the orchestrator merges reviews and critiques into one verdict:
   - **pass** → Stage 6
   - **rework** → back to Stage 3 with the required fixes treated as mandatory
   - **fail/blocked** → record the blocker and go to Stage 7

Use the sprint-plan invocation commands and wait policy for every external agent. Keep review/critique artifacts under `.scratch/verification/SPRINT-<NNN>/`.

## Stage 6: Closeout Gate

Before marking implemented:

- Re-read the Definition of Done and Closeout Checklist.
- Review every touched file with `git diff`.
- Run final validation or document an approved fallback.
- Confirm no fake/mock/demo path counts as real product behavior.
- Confirm docs/runbooks/config examples match the implementation.
- Confirm no secrets, tokens, keys, or sensitive diagnostics are logged, persisted, or committed.

If required items remain but real progress was made, keep status `implementing` with precise continuation notes. Use `blocked` only when the same blocker survives genuine workarounds and the next step needs user input or external change.

## Stage 7: Persist

On start/continue: write execution `current.env` as `implementing`, set planning `current.env` to `implementing` only if it already points at this sprint, and append `implementing` to both logs. If planning `current.env` points at a different queued sprint, leave it untouched. If `.ai/sprint-state/queue.tsv` exists and has a row for this sprint, update it to `implementing`.

On completion: set execution `current.env` to `implemented` and append `implemented` to both logs. Set planning `current.env` to `implemented` only if it points at this same sprint; otherwise leave it untouched because it may be tracking a queued future sprint. If `.ai/sprint-state/queue.tsv` has a row for this sprint, update it to `implemented`.

On block: set execution `current.env` to `blocked` and append `blocked` with the concrete blocker and required external action to both logs. Set planning `current.env` to `blocked` only if it points at this same sprint (`SPRINT_STATUS` on the planning pointer includes `blocked` — see sprint-plan); otherwise leave it untouched. If `.ai/sprint-state/queue.tsv` has a row for this sprint, update it to `blocked`.

Never remove or rewrite `.ai/sprints/SPRINT-*.md` files merely because they were not selected. Queued future sprints are valid repository state. If an external review agent creates sprint-plan artifacts for an unrelated ID during execution, record them in `.scratch/verification/SPRINT-<NNN>/UNEXPECTED_ARTIFACTS.md` and ask before deleting, merging, or changing sprint-state pointers for that unrelated sprint.

Never mark a sprint implemented just because code was committed, tests were partially run, or time ran out.

## Queue-Drain Mode

When queue-drain mode is enabled, after Stage 7 completes a sprint as `implemented`, immediately rescan `.ai/sprints/SPRINT-*.md` using Stage 0 selection rules. If another self-contained unimplemented sprint exists, announce the next selected sprint briefly and loop back to Stage 1 for that sprint.

Continue until one of these stop conditions occurs:

- No self-contained unimplemented `.ai/sprints/SPRINT-*.md` files remain.
- The selected sprint is blocked, ambiguous, or fails validation/review without a local fix.
- The user redirects, pauses, or asks for status only.
- The next available artifact is only a draft or unexpected sprint-plan artifact, not a persisted final sprint.

Do not execute `SPRINT_<NNN>_*` draft files. Newly appeared persisted sprint files are valid queue items, but unexpected drafts or unrelated review artifacts must be recorded under the current sprint's verification directory and left untouched unless the user instructs otherwise.

## Final Response

Report: selected sprint or sprint range and current status, slices completed, files changed, validations run and results, review verdict, remaining work or blocker, whether queue-drain mode stopped because the queue is empty or blocked, and commit/push/PR status only if actually requested and completed.
