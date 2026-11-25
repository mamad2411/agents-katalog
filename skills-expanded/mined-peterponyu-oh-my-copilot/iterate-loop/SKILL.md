---
name: iterate-loop
description: "[OMCP] Persistence loop that keeps working a task until acceptance criteria pass and a reviewer signs off."
---

# [OMCP] Iterate Loop

Use this plugin skill when a task must reach a verified, reviewer-signed
endpoint, not just "best effort". The loop is the Copilot CLI session itself
iterating; there is no background daemon.

## Run

1. **Initialize the PRD** if missing:
   - Break the task into right-sized stories (one per iteration).
   - Write **task-specific** acceptance criteria. Generic placeholders like
     "Implementation is complete" are not allowed.
   - Order foundational stories first.
   - Save to `docs/plans/prd-<slug>.md`.
2. **Pick the highest-priority story** whose acceptance criteria are not yet
   passing.
3. **Implement** the story, keeping edits scoped. New sub-tasks become new
   stories rather than silent expansions.
4. **Verify with fresh evidence**: run tests, build, lint, typecheck. Read the
   actual output.
5. **Mark the story done** only when every criterion is verified. Append a
   note to `docs/plans/progress-<slug>.md`.
6. **Loop** until all stories are done.
7. **Reviewer pass** in a separate context: re-check criteria, return
   APPROVED, REVISE, or REJECT.
8. **Cleanup pass** (recommended): scan changed files for leftover debug
   code, TODOs, dead imports.
9. **Re-verify** after cleanup — tests and build must still pass.

## Goal

- guarantee a verified endpoint;
- keep authoring and review in separate passes;
- keep state repo-local so the next session can resume.

## Stop conditions

- Stop when a fundamental blocker requires user input.
- Stop when the user says "stop", "cancel", or "abort".
- If the same failure recurs across three iterations, surface it as a
  fundamental issue rather than looping further.
