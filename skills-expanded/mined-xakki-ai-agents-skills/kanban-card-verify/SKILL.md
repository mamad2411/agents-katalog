---
name: kanban-card-verify
description: 'Record and verify acceptance evidence on a Kanban card, hand off an implemented child, verify lifecycle moves and keep helper effects, evidence and Git scope separate. Use before moving a card toward ready or done. RU: приёмка карточки, перенос карточки, доказательства.'
---

# Kanban card verification

Use when a card moves between stages, is handed off, or its acceptance depends on concrete evidence. A stage transition never grants another action; `done` requires explicit user approval.

## Acceptance evidence

Use when a card's lifecycle or handoff depends on concrete acceptance evidence. Inspect the full card, approved criteria, source revision, owned scope, and existing evidence before editing.

Locate the actual repository and card; capture branch, HEAD, index, working-tree baseline, protected inputs and their observed filesystem metadata, and an explicit allowlist of records. Verify identifier and digest syntax without silently repairing invalid input. An approval with missing required checks is not acceptance: preserve the original review, obtain a separate correction from the same reviewer session where available, and rerun only missing or invalidated gates under the applicable routing policy.

For each criterion record the exact observation, source or command, relevant target and version, result, limitations, and any required independent review. Differentiate executed checks from carried-forward evidence, skipped or failed checks, and unmeasured live behavior. Do not convert an unavailable gate, a local fixture, or a previous candidate's result into a current production pass.

Preserve decisions and historical evidence; explicitly mark a superseded claim at its point of use. Keep secrets and private payloads out of cards and reports. Update only the authorized records, preserve unrelated changes, and verify the real card and evidence after any supported move.

For an append-only evidence update, freeze the original bytes and digest first, append a dated sanitized block at an exact anchor, inspect the complete diff, and compare the current original-length prefix with the frozen digest. Repair only demonstrated damage from verified original bytes; never adopt a damaged baseline or reconstruct redacted text. Keep the receipt separate from immutable review and packet snapshots. For security or public APIs, explicitly exclude credentials, tokens, raw IPs, headers and bodies.

Promote only when the destination's actual criteria and authority are met. `ready` is not `done`, a child acceptance is not parent acceptance, and local checks do not authorize merge, push, deployment, or data deletion. Report the exact remaining conditions and owner when a criterion is unresolved.

Run the sanctioned board linter on the exact active card where supported; otherwise inspect its aggregate selection, verify the card is included and the checked count is nonzero, and report the actual scope. Separate historical-stage inventory collisions from the linter's own exit, errors and warnings; a successful active-only check does not prove historical uniqueness. If the linter excludes `done`, capture the active result before moving; if needed, validate the exact committed card and lock in an isolated temporary board and label this a copy-based check.

Preserve the index unless staging or a commit is explicitly authorized. For an authorized card-only commit, stage the final evidence body even after a mover staged its rename, inspect the entire cached diff and allowed old/new paths, and follow the repository's message policy. Verify native commit result, parent and SHA, content, history, index, and applicable post-commit checks. See [accepted evidence checklist](references/accepted-evidence-checklist.md).

## Acceptance handoff of an implemented child

Use to verify and hand off an implemented child task within the authorized lifecycle scope.

1. Capture branch, tracked and staged diffs, and untracked paths; read the complete current card, criteria, history, parent boundary, and board rules. Preserve unrelated board and repository state. Confirm the selected destination and actual helper effects before moving anything.
2. Separate completed implementation from outstanding acceptance: a project may permit a handoff to `test` while live criteria remain open, but promote to `ready` only when its actual criteria and gates are met. A handoff does not authorize production traffic, deployment, merge, push, or parent completion.
3. Discover and run the actual project-sanctioned checks relevant to the change, including required tests, build and infrastructure or supply-chain gates. A newly added script is not proof that a required wrapper exists; add a missing target only if in scope. Before carrying prior evidence forward, verify its source revision and relevant scope still match; label carried results as historical rather than newly executed. Changed pins or new destination criteria require affected checks again. Identify failures, skips, missing dependencies, and limits accurately.
4. Perform a fresh read-only independent review after the final repair when the task requires and authorizes it. Correct in-scope findings, repeat affected checks and review, and report unresolved or unrelated findings without broadening the task; follow any specified review-round limit.
5. Record sanitized evidence and concrete outstanding pass conditions, then perform only the authorized transition. Run the board's targeted lint and verify it actually checked the intended card; distinguish whole-board baseline failures from the new card. Verify the destination, any status fields maintained by the format, and staged versus working changes separately.
6. Report what was verified, what remains, and the next owner or action. Do not include secrets, raw credentials, request bodies, or unrelated private data in the card.

Use [adjacent transition and lint](references/adjacent-transition-and-lint.md) for source/destination and index verification. State actual remaining metrics and pass conditions without inventing thresholds. Do not generalize a narrow successful check into a host-wide pass or call a failed test an environment limitation without investigating the failure.

## Lifecycle moves and handoffs

Use when an authorized task requires moving cards or preparing a verified handoff. Resolve the current board, exact source and destination, task-specific authority, and applicable gate before touching state. Preserve unrelated staged, unstaged, and untracked work.

Read the complete card, decisions, source pins, current acceptance evidence, and board rules. A stage transition does not itself grant another action. Require explicit user approval for `done`; assess merge, push, deployment, worktree creation, and scope expansion separately. Honor a newer explicit owner decision without discarding independent required gates.

Determine the eligible stage from actual project criteria: local implementation may enter a QA stage with live acceptance still pending if that stage permits it, while `ready` requires its specified gates. Keep cancelled work and repairs to accepted cards historically accurate; do not invent test results or replay transitions merely for an audit trail. Bind independent review to its actual reviewer and candidate, distinguish accepted code from a failing global gate, and finish active writers before freezing the next phase.

Before a move, inspect the actual helper's board resolution, alias handling, stage validation, and index effects. Run targeted board checks when available and verify that the intended card was checked; zero checked cards is not validation. Perform only an authorized transition, then confirm one canonical destination, absence of the old source, actual maintained status fields, working content, and Git index effects. Record unavailable checks and unrelated failures honestly; report a native security veto without bypassing it.

When a scoped local commit is authorized, preserve normal hooks, use the task's message and staging contract, and verify actual committed paths, message, content, and excluded state. Report a moved card with blocked Git finalization as blocked rather than completed. Read back an authorized remote or deployed result before claiming it succeeded.

For focused procedures see [stage and acceptance](references/stage-and-acceptance.md), [helper and validator effects](references/helper-and-validator-effects.md), and [staged evidence](references/staged-evidence.md).

For cancellation, duplicate reconciliation, or epic parent handoffs, consult [exceptional lifecycle outcomes](references/exceptional-lifecycle-outcomes.md). For a staged rename or compatibility alias, consult [rename and index diagnosis](references/rename-and-index-diagnosis.md).

## Delivery integrity: helpers, evidence and Git scope

Use when board helpers, task changes, evidence, and unrelated work could be mixed during delivery.

1. Record the applicable board, repository status, and staged and unstaged paths before using a helper. Use the canonical allocator rather than inventing identifiers. Discover the helper's supported interface and inspect its actual board, allocation, and Git effects after execution; a printed card path is not a complete effects report.
2. Preserve unrelated index and worktree changes. Distinguish task implementation, its execution evidence, allocation state, and independent debt records. Do not use broad staging, discard foreign staged state, or stage a compatibility symlink.
3. Discover what each existing test target actually runs and run the relevant task and board gates; report exact failures, skipped checks, and unrelated pre-existing failures. Do not present a partially passing or unrun gate as green. Complete implementation and required gates before independent review when required and authorized.
4. Make a local commit only when the task and applicable policy authorize one. Stage the exact owned paths, follow the actual message and trailer policy, verify the resulting commit and intended paths, and preserve unrelated work. Never invent an agent trailer or bypass normal hooks.
5. Record the actual verified endpoint and remaining work on the card. Ready-for-review and out-of-scope rollout are not completed production acceptance. Map independent findings to existing cards before proposing additions; respect the owner's requested authorization for new cards.

For additional details consult [helper effects and commit scope](references/helper-staging-and-scope.md), [review and scope correction](references/review-and-scope-correction.md), and [follow-up triage](references/deferred-follow-up-card-triage.md). A `done` transition requires explicit user approval.
