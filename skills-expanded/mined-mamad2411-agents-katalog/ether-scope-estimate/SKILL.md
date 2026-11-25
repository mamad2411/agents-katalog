---
name: ether-scope-estimate
description: Use before writing any implementation code, right after tasks.md exists — estimate a min/max lines-of-code range for a surgical fix to the stated problem, record it in ether's local learning store (`.ether/learning.db`), then after verify compare actual LOC changed against the estimate. Mandatory alongside ether-tdd. If actual exceeds the max, requires a recorded cause + prevention learning before the change can be considered done — the goal is surgical changes, not touching logic in more places than necessary. Fully offline — no network calls.
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Ether Scope Estimate

Local-only guardrail against scope creep, backed by ether's own
`.ether/learning.db` (no network calls — everything here is `ether learn
...` against a local sqlite file). Every agent that writes implementation
code estimates the LOC footprint *before* touching code, then reconciles
against what actually changed. This runs alongside `ether-tdd` (test-first),
not instead of it — TDD governs correctness, this governs blast radius.

## Workflow

1. **Before implementation. Search prior estimates for this kind of
   problem.** `ether learn search "<keywords from the task>"` — if a
   similar problem was solved before, its recorded actual LOC and any
   overrun learnings calibrate this estimate. Don't estimate from a blank
   slate if history exists.

2. **Estimate min/max LOC.** Read the task/prompt and (if present)
   `tasks.md`/`ac.md`. Name the smallest surgical change that satisfies the
   acceptance criteria — touching only the files/functions the problem
   actually requires, no drive-by refactors, no "while I'm here" edits.
   State:
   - **min** — the floor if the fix is exactly as contained as it looks
     (e.g. one function, one call site).
   - **max** — the ceiling if it turns out to need a couple of adjacent
     call sites or a test file, still without spreading into unrelated
     logic. If the max requires touching logic in more than 2-3 files,
     stop and reconsider — that's a signal the task is bigger than it
     looks and may need to be split, not a license to pad the estimate.
   - If the change involves editing EXISTING lines (a shared function
     signature, a set of assertions, config values) rather than adding
     new ones, count each edited line as ~2 LOC (one deletion, one
     insertion in the diff), not 1 — a single-argument signature change
     that ripples through N existing call sites costs ~2N LOC in the
     diff even though it looks trivial.

3. **Record the estimate.** From the target repo:
   `ether learn problem "<short name>" "<task description + min/max LOC
   estimate + files expected to change>" [--change <change-id>]`
   Capture the returned `problem-id` — it's needed to close the loop.

4. **Implement** (via `ether-tdd`). Keep the change scoped to what the
   estimate named. If mid-implementation it becomes clear more files need
   touching than the max allowed, stop and re-run step 2 with the new
   information rather than silently blowing past the estimate — the point
   is catching scope creep while it's still a decision, not after the fact.

5. **After verify, measure actual LOC.** `git diff --stat <base>...HEAD`
   (or `git diff --stat` against the pre-change commit) — sum insertions +
   deletions across all changed files, excluding generated files/lockfiles.

6. **Reconcile against the estimate.**
   - **Within [min, max]**: record a confirming observation —
     `ether learn observe "estimate held: <actual> LOC vs [<min>,<max>]"
     --cause <problem-id>` — this is what makes future searches in step 1
     trust the estimate pattern.
   - **Below min**: fine, no action needed beyond noting it in the report;
     being under-budget is not scope creep.
   - **Above max**: this is scope creep. Do not close the task without
     doing the next step.

7. **On overrun (actual > max): record cause + prevention, mandatory.**
   - `ether learn cause <problem-id> "<why it actually took more LOC —
     e.g. hidden coupling, missing abstraction, test scaffolding
     underestimated, logic duplicated across N call sites>"`
   - `ether learn solution <cause-id> "<name>" "<what would have kept this
     surgical>" --files <files touched beyond the original estimate>`
   - `ether learn accept <cause-id> <solution-id>` once the explanation is
     recorded (this is documentation of what happened, not asking
     permission — record it even if the overrun was justified).
   - `ether learn learning <problem-id> "<the generalizable lesson for
     future estimates of this shape>" --category <e.g. scope-creep>` — this
     is what step 1 of the *next* run finds via search, closing the loop.

8. **Report.** State: estimate (min/max), actual LOC, verdict (held/
   under/over), and if over, the cause + prevention learning id.

## Non-negotiables

- No implementation starts without a recorded estimate (step 3) — a
  `problem-id` must exist before `ether-tdd`'s red step. Enforced
  mechanically by `guard.ts`'s `validateWrite` — writes to project code
  under an active change are blocked (exit denied) until a scope-estimate
  `problem` row exists for that change id, same as the `tasks.md`/`ac.md`
  gate.
- No overrun closes silently — step 7 is not optional when actual > max.
- The prevention learning must be generalizable ("estimate call sites via
  grep before committing to a max next time"), not a one-off excuse
  ("this task was just hard") — a cause without an actionable solution
  doesn't close the loop for future estimates.
- Estimating "generously" to avoid ever triggering step 7 defeats the
  purpose — the max should reflect genuine surgical scope, not padding to
  guarantee a pass.

## Where this is invoked from

- `ether-phase-dag` — right after `tasks.md` exists, before `apply`
  begins writing code.
- Any bounded fix delegated to a builder-style subagent.
