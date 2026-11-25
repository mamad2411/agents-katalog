---
name: phase-execute
description: Phase C of the solution-design workflow: execute an approved solution plan through iterative implementation, TDD, build repair, debugging, and progress tracking.
origin: ECC automation-pack
---

# Phase Execute

Use this skill when the user asks for `/phase-execute`, execute a validated plan, implement a solution plan, or run the execution stage after solution validation.

## Purpose

Carry a validated plan into implementation while preserving feedback loops and traceability.

## Workflow

1. Load the latest validated plan.
2. Create or confirm an appropriate working branch when the repo uses git.
3. Break the plan into small execution units.
4. For each unit:
   - write/update tests when practical
   - implement the smallest change
   - run targeted checks
   - debug systematically on failure
   - update progress
5. Use parallel agents only for independent units with non-overlapping files.
6. Commit intermediate units only when requested or consistent with the project workflow.
7. Mark blocked work explicitly and continue only when safe.

## Output

Include:

- units completed
- files changed
- checks run
- failures and fixes
- blocked items

End with `PHASE_EXECUTE_DONE` or `PHASE_EXECUTE_BLOCKED`.
