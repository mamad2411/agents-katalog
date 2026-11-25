---
name: finish-task
description: Finish an implemented and reviewed task — README audit, final behavior proof, completion record, PR creation after approval, and cleanup of the task's retained review files after CI passes. Use manually after the task-review and review-fix-worker loop is clean. Lightweight orchestration suited to a small fast model.
---

# Finish Task

Take one implemented task whose manual review loop is complete and carry it to a CI-green PR. This
skill is lightweight orchestration: it updates the README, proves final behavior, records
completion, hands off to `create-pr` after explicit user approval, and removes the task's retained
review files after the PR is CI-green. It does not implement, review, or remediate.

## Model routing

This skill is mechanical orchestration over already-verified work. Run it on the smallest capable
fast model (router: `finish-task` maps to the luna-max route). Escalate to the user rather than
muscling through ambiguity.

## Preconditions

1. Resolve the task from a supplied path, or find the single `[~]` task in the master plan. With
   zero or multiple `[~]` tasks and no supplied path, stop and report the state.
2. Confirm the current branch matches the task's `**Branch**` value; otherwise stop.
3. Normalize the selected task to its repository-relative path. Inspect every `reviews/*.md` file
   at the repository root and select those whose `**Task:**` matches that normalized path. If any
   matching file contains a finding with `**Status:** open`,
   stop and tell the user to run `/skill:review-fix-worker` (or explicitly skip or accept the
   remaining findings) first. Absence of a matching review file for a `code` or `mixed` task means
   `task-review` never ran; stop and tell the user to run `/skill:task-review` first. Retain the
   matching file list and each review outcome for completion recording, PR evidence, and cleanup.

## Workflow

### Mandatory execution checklist

Create this checklist in working context when the skill starts and keep it current. Check an item
only after completing the corresponding workflow section with evidence. If work stops, report the
first unchecked item and its blocker.

- [ ] Preconditions confirmed: task, branch, review loop closed
- [ ] README inspected; `write-well` audit completed only when README prose changed, or no-impact reason recorded
- [ ] Highest-level automated and required manual proof passed, or reused under the freshness rule
- [ ] Task file records implementation, decisions, documentation, review, and proof
- [ ] PR opened under the fast-lane conditions or explicit approval, and the current head is CI-green
- [ ] All retained review files for this task removed; other tasks' files untouched

### 1. Update the README

Inspect the README now that the implementation has reached its reviewed
state. When the task changed current application behavior, setup, configuration, or usage, invoke
`write-well` only for the README update and audit only the affected prose. Complete the skill's full
audit loop; loading `write-well` alone does not complete this step. Describe the current application,
not a history of what changed. Record the affected sections and audit pass count in the task file.

Leave the README unchanged when the task has no documentation impact and record that conclusion in
the task file.

### 2. Prove the final behavior

#### Proof freshness

Before running anything, check whether the proof already exists. A recorded validation result is
reusable when all of these hold:

- the task file records a `**Proof head:**` SHA equal to the current `git rev-parse HEAD`;
- it records the tier that ran and the exact commands, and that tier matches the task's recorded
  tier;
- every recorded command passed;
- no `[verify]` item and no manual check for this task is still outstanding.

When all hold, reuse that evidence, state in the report that proof was reused and name the SHA, and
skip to step 3. When any fails, run the validation below and then record `**Proof head:**` with the
current SHA, the tier, the commands, and their results, so the next step in the loop can reuse it.

`task-review` and `review-fix-worker` both end at a validated commit. Re-running the same suite at
the same SHA proves nothing new and is the single most repeated cost in this workflow. Repository CI
re-runs it again on the PR head, which is the check that actually gates the merge.

#### Running the validation

Run the final validation for the task's recorded tier, once:
document/plan consistency for `documentation`, affected dependency or configuration proof for
`focused`, and the repository's canonical check for `canonical`. A documentation or focused tier
must not be promoted to the application's canonical suite without an actual diff reclassification
or explicit acceptance criterion. Run the highest-level automated proof, plus any
focused check invalidated by a later change. Prefer browser-level proof for
user-facing behavior and executable scripts or disposable local environments for CLI, API,
database, and provider workflows.

Keep `[verify]` items from the task for this step.

When automated verification is impossible, give the user exact steps, the expected result, and
the signal that indicates failure. Explain why the agent cannot perform the check, then wait for
the user to confirm it passed. Manual verification blocks completion.

### 3. Record completion

Check off the task's implementation work, human checkpoints, and acceptance criteria. Record what
was built, decisions made, relevant file paths, README disposition, review outcome (findings fixed,
skipped, or accepted as security risks, with reasons), `**Proof head:**` with automated proof, and
manual verification. Leave the master-plan pointer at `[~]`; it moves after the merge.

Write this as one commit. Do not spread completion bookkeeping across several `docs(...)` commits on
the feature branch; each one is a commit and push round trip that delivers nothing.

This final commit runs **with** the repository's commit hooks (no `HUSKY=0`): every earlier commit
on the branch skipped them, so this is the one place the full typecheck, lint, and generated-artifact
refresh (tool-schema dumps, generated theme CSS) execute. If the hook stages regenerated files, they
belong in this commit. If the hook fails, fix the cause; never bypass it here.

### 4. Open the PR

#### Fast lane

Summarize the completed task, then invoke `create-pr` without stopping when every one of these
holds:

- every review file matching this task has zero `open` findings;
- no finding was accepted as a security risk, and the review recorded no `security` axis finding;
- the task's recorded change class is not `dependencies`;
- step 2 passed or was reused, with no outstanding manual verification;
- exactly one task and one branch matched in the preconditions.

Report that the fast lane applied and name the conditions that satisfied it.

#### When to stop and ask

If any condition fails, summarize the completed task, name the failing condition, and ask the user
to approve opening the PR. Do not invoke `create-pr` without explicit approval in that case. Always
stop and ask when the user asked to review the PR before it opens.

#### Handoff

Invoke `create-pr` with the task path, the review outcome (fixed findings, skipped minors with
reasons, accepted security risks with user reasons), and verification proof. `create-pr` opens or
updates the PR and waits for CI. It does not merge and does not write the task pointer.

Treat PR creation as complete only when `create-pr` returns a CI-green current head. Leave the task
file under `plans/tasks/` and the pointer at `[~]`. If PR creation or CI does not succeed, every
review file must remain in place. The user merges and closes the task separately.

### 5. Remove the task's review files

Only after `create-pr` confirms the current PR head is CI-green,
delete every retained `reviews/*.md` file whose `**Task:**` exactly matches the selected
task's normalized repository-relative path. These files are ignored workflow state and their outcomes are already recorded in the task
file and PR evidence. Never delete a review file for another task or branch. Leave `reviews/`, its
local exclude entry, and unrelated workflow files intact.

Confirm every matching review file is gone before reporting completion.

## Rules

- Finish one task per invocation.
- Never work on `main`.
- Do not run while any review finding for the selected task is still open.
- Keep all review files until the selected task's current PR head is CI-green; then remove every
  review file matching that task and no others.
- Verify completion against the code and observable behavior, not the implementation log.
- Stop for impossible-to-automate verification, and for PR approval when the fast lane does not apply.
- Never write the master-plan pointer; it stays `[~]` until the merged task is closed.
- Never reuse proof from a different SHA, a different tier, or a failed run.
