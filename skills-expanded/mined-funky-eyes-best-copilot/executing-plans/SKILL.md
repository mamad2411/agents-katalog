---
name: executing-plans
description: "Compatibility entrypoint for executing approved tasks. The PM and role workflows own SDD, TDD, review, verification, and state sync."
user-invocable: false
---

# Executing Plans Compatibility Entry

Preserve this route for existing callers. Execute only an approved task from a valid Spec Bundle (or a compact approved small-work packet) using `core-workflow-contract` and the assigned role workflow.

Before execution, require `plan_revision`, matching PM-owned `execution_confirmed`, task ID/full task text, owner/reviewer lanes, write set, dependency state, and parallel readiness. Return `NEEDS_CONTEXT` or `NEEDS_USER_INPUT` instead of running an absent, stale, unresolved, or unapproved plan.

## Per-Task Contract

1. Read the task's `Owner lane`, `Reviewer lanes`, write set, dependencies, acceptance checks, RED check, verification command, and stop conditions from `spec/<feature>/tasks.md`.
2. Mark its Progress Ledger row `IN_PROGRESS` before editing; only the named owner edits the write set.
3. Run RED-GREEN-REFACTOR for behavior changes or fixes, then obtain review from the named independent reviewer lanes.
4. Record Stage 1 spec compliance, Stage 2 code/release-risk review, verification, evidence, next action, and notes in the same ledger row.
5. Update `memories/repo/current-workstreams.md` before starting another task or closing the batch; update indexes when their rows change. Standard/full batches also require a final independent whole-scope review before closeout.

`DONE` requires passing verification and required review evidence. Use `DONE_WITH_CONCERNS`, `NEEDS_CONTEXT`, `NEEDS_USER_INPUT`, or `BLOCKED` when applicable; never hide blocked or skipped work behind `DONE`.

Return the shared structured handback with changed files, verification, review, state-sync evidence, and residual risk.
