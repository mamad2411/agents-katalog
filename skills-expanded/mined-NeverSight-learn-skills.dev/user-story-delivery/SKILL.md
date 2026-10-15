---
name: user-story-delivery
description: 'Orchestrate uninterrupted new or resumed delivery of exactly one GitHub story through manifest, implementation, exhaustive INITIAL review, frozen ledger, bounded DELTA review, and merge gate. Continue across internal checkpoints until the story reaches a terminal state or genuine external blocker.'
metadata:
  author: eho
  version: '2.3.1'
---

# User Story Delivery

Coordinate `user-story-acceptance-manifest`, `user-story-implementer`, and `user-story-reviewer`. Persistent artifacts—not conversation history or the originating workflow—determine where work resumes.

**PREREQUISITE**: `gh` must be installed and authenticated.

## Continuity Contract

A `user-story-delivery` invocation ends only at:

- `Already completed`;
- `Merged`;
- `Approved` when repository policy requires a human to merge;
- `Blocked`;
- `Specification required`;
- `Reconciliation required`; or
- `Workflow did not converge`.

`TARGET_RESOLVED`, `MANIFEST_READY`, implementation in progress or complete, PR open, `INITIAL_REVIEW_COMPLETE`, `LEDGER_FROZEN`, `REVISION_COMPLETE`, and `DELTA_REVIEW_COMPLETE` are non-terminal. A worker handoff or persisted checkpoint at any of these states returns control to this coordinator; immediately execute `Next action` rather than yielding to the user.

Pending scoped implementation, missing tests, incomplete evidence, an open review ledger, or ordinary revision work are work to perform. They become blockers only when they cannot be completed safely within scope after reasonable recovery attempts or require external input/authority.

## Required Worker Topology

When a subagent/worker mechanism is callable, this context remains the story coordinator and spawns bounded specialist workers. It must not write implementation code or perform the independent review itself.

1. Spawn a fresh `user-story-acceptance-manifest` worker for manifest creation, validation, reuse, or replacement.
2. Spawn a fresh `user-story-implementer` worker for the story. Reuse that worker for bounded `REVISION` follow-ups when it remains available; otherwise spawn a new implementer with the complete active manifest, PR state, and frozen ledger.
3. After the implementation handoff is persisted for the current head SHA, spawn a `user-story-reviewer` worker whose context is distinct from every implementation worker.
4. Reuse the INITIAL reviewer for DELTA follow-ups when available. If it is unavailable, spawn a fresh reviewer with only the active manifest, complete frozen ledger, revision handoff, reviewed/current SHAs, and cycle count. DELTA constraints still apply.
5. Keep implementation and review sequential. A reviewer never edits; an implementer never reviews or approves.

Pass compact source packets, not the parent conversation. Record each worker/task reference in the Story Resume Checkpoint and terminal handoff. Reviewer independence is a merge-gate invariant: matching or unknown implementer/reviewer identity cannot be described as independent.

Do not select models in this skill. Spawn workers without overrides unless the user explicitly assigned them.

If no worker mechanism exists, set `Worker isolation: unavailable`. In-context implementation may proceed as a compatibility fallback, but review from the same context is `Comment only` and cannot satisfy an independent-approval requirement.

## Entry Modes

Discover rather than require the caller to choose:

- `NEW_STORY`
- `ADOPT_EXISTING_PR`
- `RESUME_FROM_MANIFEST`
- `RESUME_FROM_IMPLEMENTATION`
- `RESUME_FROM_INITIAL_REVIEW`
- `RESUME_FROM_REVISION`
- `RESUME_FROM_DELTA_REVIEW`
- `RESUME_FROM_MERGE_GATE`
- `ALREADY_COMPLETED`

## State Machine

```text
TARGET_RESOLVED
→ MANIFEST_READY
→ INITIAL_IMPLEMENTATION_COMPLETE
→ INITIAL_REVIEW_COMPLETE
→ LEDGER_FROZEN
  ├─ clean ────────────────────────────────────────→ APPROVED
  └─ blockers → REVISION_COMPLETE
                 → DELTA_REVIEW_COMPLETE
                   ├─ resolved ────────────────────→ APPROVED
                   └─ blockers → REVISION_COMPLETE
APPROVED → MERGED
```

Resume at the latest valid state. Do not repeat a valid completed state merely because its originating agent or workflow differs.

## 1. Resolve and Reconstruct

Resolve the exact story, issue, design revision, default-branch SHA, dependencies, repository instructions, matching PRs, and GitHub identity.

Inspect:

- Issue state/body/comments and managed manifest/checkpoint markers.
- Candidate PRs, head/base/merged SHAs, checks, commits, reviews, and changed files.
- Managed Review Ledger marker.
- Whether a merged commit is present on the current default branch.

Produce and persist:

```markdown
## Story Resume Checkpoint v1
- Story ID:
- Issue:
- Design revision:
- Entry mode:
- Discovered PR:
- PR state:
- Intended base branch:
- PR base branch:
- Current head SHA:
- Merged SHA:
- Manifest version/status:
- Ledger version/status:
- Last reviewed SHA:
- Open P0:
- Open P1:
- Initial review count:
- Delta review count:
- Manifest worker ref:
- Implementation worker ref:
- Reviewer worker ref:
- Worker isolation: available | unavailable
- Latest valid state:
- Next action:
- Terminal: yes/no
- Continue automatically: yes/no
- Yield reason: None | User input | New authority | External dependency | Specification | Reconciliation | Cycle cap | Human merge
- Reconciliation required:
```

Upsert this checkpoint on the stable story issue after every successful transition using marker `story-delivery-checkpoint:<story-id>:v1`. Keep the issue as the single checkpoint location even after a PR exists; manifests and review ledgers may remain on their phase-specific issue or PR comments.

For every non-terminal state, set `Terminal: no`, `Continue automatically: yes`, and `Yield reason: None`, then perform `Next action` in the same invocation.

For checkpoints created before v2.2 that lack these three fields, derive them from `Latest valid state`: treat every state outside the terminal list in the Continuity Contract as `Terminal: no` and continue automatically. Missing continuity fields are a compatibility condition, not a reconciliation blocker.

```bash
bash /absolute/path/to/scripts/upsert_comment.sh \
  "<issue-number>" \
  "story-delivery-checkpoint:<story-id>:v1" \
  "<checkpoint-body-file>"
```

## Checkpoint Validity

Use the latest state only when its prerequisites still hold:

- A merged story is complete only when the matching merge/equivalent commit is on the default branch.
- A manifest is valid only when its design revision, issue contract, and relevant base assumptions remain compatible.
- A review or approval applies only to its recorded SHA.
- A ledger remains historical evidence, but changed scope requires a new manifest version and a new INITIAL review.
- Review-cycle counts survive resume; do not reset them.
- An adopted/open PR must target the intended default branch. A different base requires explicit retargeting and renewed verification, or reconciliation; it cannot pass the merge gate as-is.
- Multiple plausible PRs, missing merged evidence, contradictory artifacts, or material design drift require reconciliation.

If the story is already validly merged:

- Return `ALREADY_COMPLETED`.
- Produce `Legacy Story Completion Record v1` when v2 artifacts are absent.
- Do not create retrospective v2 artifacts or reopen implementation.

## 2. Reuse or Create the Manifest

Call `user-story-acceptance-manifest` with the design, issue, current default branch, dependencies, discovered PR, and any existing marked manifest.

Use `Manifest Resolution Handoff v1` to accept:

- `REUSE`: existing manifest sources and assumptions are still valid.
- `CREATE`: no manifest exists.
- `REPLACE`: requirements or relevant assumptions changed; increment the manifest version and restart at implementation/INITIAL review.
- `BLOCKED`: product or architecture reconciliation is required.

For `CREATE` or `REPLACE`, upsert the complete active manifest:

```bash
bash /absolute/path/to/scripts/upsert_comment.sh \
  "<issue-number>" \
  "acceptance-manifest:<story-id>:v<version>" \
  "<manifest-body-file>"
```

For `REUSE`, use the existing immutable body byte-for-byte; do not update it with the current action, PR/head, or progress state. The separate resolution handoff records why it was reused. Do not delete prior manifest versions; they explain historical review decisions.

## 3. Implement or Adopt

Choose:

### New implementation

Call `user-story-implementer` with `Phase: INITIAL_IMPLEMENTATION`.

### Existing open PR

Call it with `Phase: ADOPT_EXISTING_PR`, passing the active manifest, PR, current head SHA, and any existing evidence. The implementer:

- Inspects the complete existing PR.
- Produces manifest-row evidence.
- Completes missing required implementation when safe.
- Pushes only when changes are needed.
- Never creates a second PR.

### Resume revision

When a frozen ledger has open P0/P1 items, call `Phase: REVISION` with the complete ledger and current PR. Require a resolution status for every open item.

In all paths require `Implementation Handoff v2`. Persist the complete handoff on the PR with the immutable marker `implementation-handoff:<story-id>:<head-sha>`:

```bash
bash /absolute/path/to/scripts/upsert_comment.sh \
  "<pr-number>" \
  "implementation-handoff:<story-id>:<head-sha>" \
  "<implementation-handoff-body-file>"
```

Do this immediately after confirming the pushed head SHA and before entering review. Resume directly to review when a valid persisted handoff covers the current head SHA. If code was pushed but the handoff is absent, rerun `ADOPT_EXISTING_PR` to reconstruct exact manifest-row and ledger-resolution evidence without gratuitous changes, then persist it.

## 4. Select Review Mode

Run `INITIAL` when:

- No complete frozen ledger exists for the active manifest, or
- The manifest version/scope changed.

Run `DELTA` when:

- A complete frozen ledger exists,
- The PR changed after its reviewed SHA, and
- Revision evidence addresses that ledger.

Skip review and enter the merge gate only when:

- The ledger has zero open P0/P1 items,
- The approval/sign-off applies to the current head SHA, and
- Required checks pass.

An old review comment without a complete v2 ledger may inform review but cannot replace the adopted PR's new INITIAL review.

## 5. Persist the Ledger

After a complete INITIAL review, freeze and upsert:

```bash
bash /absolute/path/to/scripts/upsert_comment.sh \
  "<pr-number>" \
  "review-ledger:<story-id>:v<manifest-version>" \
  "<ledger-body-file>"
```

Keep IDs and resolved history stable. DELTA reviews update statuses in coordinator/checkpoint state and upsert the current complete ledger body; never erase historical findings.

Every submitted review body must contain a deterministic attempt ID and the complete `Review Handoff v2`:

```text
review:<story-id>:<manifest-version>:INITIAL:<reviewed-sha>
review:<story-id>:<manifest-version>:DELTA:<cycle-ordinal>:<reviewed-sha>
```

GitHub's submitted review is the durable attempt record. Before invoking a reviewer, enumerate valid review bodies for the active manifest/lineage and choose the next ordinal. Derive INITIAL/DELTA counts from distinct valid attempt IDs; treat checkpoint counts as a cache. If submission succeeded but checkpoint/ledger persistence was interrupted, reconstruct from the submitted review and finish persistence without consuming another attempt.

## Cycle Limit

- Two DELTA revision cycles by default.
- A third only with a recorded exceptional reason.
- Never begin a fourth.

Counts include work performed before interruption when durable evidence exists. On exhaustion return `WORKFLOW_DID_NOT_CONVERGE` with classification and remaining ledger.

## Merge Gate

Before merge verify:

- Active manifest matches current scope.
- Required manifest rows pass or have an explicit product/repository waiver.
- No P0/P1 blocker is open.
- Required checks pass. If GitHub reports that the branch has no checks or no
  required checks, the helper proceeds to the server-enforced merge gate.
  Failed, pending, or unrecognized check states remain fail-closed.
- PR head equals the final reviewed SHA.
- PR base branch equals the intended default branch.
- Reviewer worker identity is distinct from every implementation worker identity, or repository policy explicitly accepts external human review.
- Repository policy permits agent merge.

Use:

```bash
bash /absolute/path/to/scripts/merge_pr.sh \
  "<pr-number>" \
  "<reviewed-head-sha>" \
  "<intended-base-branch>"
```

Return `Approved` when human merge is required. If the PR head moved, resume from review; do not merge or discard prior ledger history.

## Terminal Story Handoff

```markdown
## Story Delivery Handoff v2
- Story ID:
- Issue:
- PR:
- Entry mode:
- Resumed from:
- Manifest version:
- Ledger version:
- Final reviewed SHA:
- Final state: Already completed | Approved | Merged | Blocked | Specification required | Reconciliation required | Workflow did not converge
- Initial reviews:
- Delta reviews:
- Open P0:
- Open P1:

## Verification
- Required commands:
- Passed:
- Failed or not verified:
- CI/checks:
- Pre-existing failures:

## Compatibility
- Delivery protocol: v2 | legacy | mixed
- Legacy completion record:
- Existing PR adopted:

## Worker Isolation
- Story coordinator ref:
- Manifest worker ref:
- Implementation worker ref(s):
- Reviewer worker ref(s):
- Independent reviewer verified: yes/no
- Reduced-isolation fallback used: yes/no

## Follow-ups
- P2:
- P3:
- Residual risk:
- Required next action:
```

## Operating Rules

- Reconstruct before acting and persist after every transition.
- Prefer the latest valid checkpoint, not the latest timestamp.
- Never create a duplicate PR or fabricate historical artifacts.
- Keep implementation and review independent and context packets compact.
- When worker tooling exists, spawn the required specialists; do not silently collapse coordinator, implementer, and reviewer roles into one context.
- Do not send a user-facing final response for a non-terminal story checkpoint. Specialist handoffs are coordinator inputs, not permission to pause delivery.
- Accept pre-v2.2 checkpoints without continuity fields using the compatibility rule above; do not rewrite historical comments solely to normalize their schema.
- Model selection is outside this skill.
