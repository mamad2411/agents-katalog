---
name: kanban-card-build
description: 'Deliver an authorized Kanban queue autonomously while preserving scope and evidence, including measurement-backed cards. Use when the owner asks to work through the board queue. RU: автономная работа по очереди, выполнить карточки.'
disable-model-invocation: true
---

# Kanban card delivery

Use when the owner requests autonomous work through a board queue, including cards whose acceptance depends on measurements.

## Autonomous queue delivery

Use when the owner requests autonomous work through a board queue. Read the actual board, scope, lifecycle, dependencies, and applicable project rules before selecting work. A request for autonomous delivery does not imply authority for `done`, merge, publication, deployment, or destructive effects.

1. Inventory the authorized queue across stages and reconcile duplicate IDs, prior child renames, related branches and actual delivered scope. Distinguish executable tasks from historical, blocked, or organizational records. Preserve unrelated worktree and index state. Select unblocked work in an order consistent with dependencies and the owner's priorities; do not reimplement work already evidenced as complete.
2. Resolve each action's authority and exact target. Continue already authorized phases without asking again; preserve stricter phase gates and explicit user approval for `done`. Treat an unanswered material decision as unresolved unless it was explicitly delegated. Record later owner answers and supersede stale pending statements without assuming broader permission.
3. Delegate only when allowed and the runtime can provide the required role. Give each worker its scope, ownership, relevant boundaries, required gates, and current baseline. Avoid parallel writers on overlapping files or shared state. Preserve continuity and partial work after a worker stops; retain a still-running process handle instead of duplicating work. A native security veto stops the denied operation; do not bypass it by changing tools or policies.
4. Make the smallest meaningful implementation and run the required checks. Bind review and gates to the actual tested candidate; report failed, skipped, deferred, historical, and unrun checks separately. Reuse unchanged accepted evidence only when its source and scope still match. A deferred batch-review schedule does not waive any stage-entry gate: retain the last eligible stage and run the required combined checks and review on the completed candidate.
5. Resolve canonical board paths and helper effects before each authorized lifecycle move. Verify the target state, applicable lint, Git index and working changes independently. Use exact owned paths and normal hooks; a routine local commit requires the task's applicable authorization, and unrelated changes remain untouched.
6. Report each task's actual endpoint, evidence, blockers, remaining decisions, active work, and next owner. A completed child, `ready` card, or scoped test is not whole-epic or production acceptance. Do not silently drop unrelated findings; map them to existing work or propose a separately authorized follow-up.

For bounded queue work use [pool checklist](references/autonomous-pool-checklist.md), [decision handoffs](references/decision-handoffs.md), [delivery safeguards](references/delivery-safeguards.md), and [finalization and blocked handoffs](references/finalization-and-blocked-handoffs.md).

## Measurement-backed delivery

Use when a card's acceptance depends on measurements or benchmark results. Preserve prior evidence and record the precise scope of new observations.

1. Capture repository, branch, baseline and relevant staged, unstaged and untracked state. Read the complete card, acceptance criteria, required source revisions, and owned paths; preserve unrelated state. Inspect the measurement harness, units, arguments, sample counts, aggregation, error handling, and cleanup before relying on its output.
2. Run only authorized measurements and checks. Record exact parameters, raw samples, units, sample count, cadence, aggregation method, and observations; distinguish a local or reduced synthetic run from historical, production, or full-scale evidence. Do not equate a fake service check with a real workload measurement. When feasible, perform a current real local harness spot-check without replacing historical multi-trial evidence.
3. Verify calculations and edge cases, including zero samples and invalid units, with focused fixtures when applicable. Ensure the test distinguishes the claimed behavior from basic reachability and fails if prerequisites fail.
4. Report actual task gates, unrelated failures, skips, and unmeasured claims without converting failure into a pass. Apply the project's authorized adjacent board transitions and lint checks before and after a move, require evidence for the selected stage, and preserve unresolved acceptance gates. Reconcile maintained status fields with the actual path; do not invent missing fields.
5. Stage and commit only when authorized, with exact owned paths and the actual message policy. A helper-staged rename may lack later evidence edits: inspect and refresh the final body when staging is authorized. Verify the resulting card, revision, message, evidence, index and excluded changes; report only the cleanliness and source ancestry that were observed. Recompute ahead/behind after the last commit or report exact refs instead.

Use [measurement evidence](references/measurement-evidence.md), [lifecycle and handoff evidence](references/lifecycle-and-handoff-evidence.md), and [read-only readiness review](references/read-only-readiness-review.md) for the relevant mode. `ready` is not `done`; explicit user approval is required for `done`.
