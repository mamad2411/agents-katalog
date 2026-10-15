---
name: design-doc-review-loop
description: 'Prepare or resume preparation of an existing design doc for feature delivery through one exhaustive independent review, a frozen design-finding ledger, complete revisions, and bounded delta reviews. Use when asked to review and revise a design until implementation-ready or mark it Revised for feature-delivery.'
metadata:
  author: eho
  version: '2.1.0'
---

# Design Doc Review Loop

Coordinate `design-doc-reviewer` and `design-doc` while preserving independent review, stable findings, and resumable progress.

## State Machine

```text
DRAFT
→ INITIAL_REVIEW_COMPLETE
→ DESIGN_LEDGER_FROZEN
  ├─ clean initial review ─────────────────────────→ REVISED
  └─ blockers → REVISION_COMPLETE
                 → DELTA_REVIEW_COMPLETE
                   ├─ resolved ─────────────────────→ REVISED
                   └─ blockers → REVISION_COMPLETE
```

Terminal alternatives are `SPECIFICATION_REQUIRED` and `WORKFLOW_DID_NOT_CONVERGE`.

## 1. Resolve and Reconcile

- Require an exact or unambiguous design path.
- Read the status, current revision, companion review artifact, Revision Notes, directly relevant vision/architecture context, and repository instructions.
- Confirm `design-doc` and `design-doc-reviewer` are available.
- Treat a user statement such as “the initial review is complete” as a discovery hint, not proof.
- Reconstruct the earliest valid state from the artifacts and their source revisions:
  - current complete INITIAL review with no blockers → `DESIGN_LEDGER_FROZEN`;
  - current complete INITIAL review with blockers and no corresponding revision → `DESIGN_LEDGER_FROZEN`;
  - revision after the reviewed revision with no current DELTA → `REVISION_COMPLETE`;
  - current DELTA with open blockers → `DELTA_REVIEW_COMPLETE`;
  - current clean INITIAL/DELTA and `Status: Revised` → already complete;
  - `Status: Revised` without current review evidence → resume from the earliest invalid review state.
- Preserve existing cycle counts and finding history. Never reset the loop because the caller or model changed.

Record or refresh this compact artifact in the companion review file:

```markdown
## Design Review Resume Checkpoint v1
- Design doc:
- Current design revision:
- Review file:
- Active ledger version:
- Last valid reviewed revision:
- Last completed state:
- Initial reviews completed:
- Delta cycles completed:
- Exceptional third cycle authorized: yes/no
- Next action:
- Reconciliation notes:
```

Update the checkpoint after every state transition. The review and design documents remain authoritative if a checkpoint is missing or stale. The companion review file is updated in place: every reviewer must preserve the checkpoint, complete frozen ledger, prior finding history, and cycle counts while replacing current rubric/evidence sections. If those sections cannot be merged safely, stop as `SPECIFICATION_REQUIRED`; never overwrite the file with a history-free report.

## 2. Exhaustive Initial Review

When no complete INITIAL review exists for the active design requirements, start a separate `design-doc-reviewer` with:

```text
Mode: INITIAL
Design doc: <path>
Reviewed revision: <commit-or-content-identifier>
Existing review artifact: <path-or-none>
Resume checkpoint: <checkpoint-or-none>
```

Require a complete rubric matrix, `Initial-review completeness: Complete`, `Design Review Ledger v1`, and Critical/Major blockers separated from Minor improvements.

If rows are missing, ask the same reviewer to complete them before freezing. Freeze ledger IDs and required resolutions after a complete initial review. If it finds zero open Critical and Major findings, proceed directly to `Mark Revised`; do not create a no-op revision or DELTA review.

## 3. Revise the Complete Ledger

When Critical or Major findings remain, revise using the `design-doc` Revision Workflow. Send the design path, complete frozen ledger, deferred Minor list, current checkpoint, and current cycle count.

Require every ledger item to be triaged as `Accept`, `Accept (Alt)`, `Reject`, or `Defer`. Accepted items must change the relevant sections. Rejected items need source-based rationale. Defer only Minor work or decisions that require the user; unresolved Critical/Major decisions stop as `SPECIFICATION_REQUIRED`.

Keep status `Draft` during revision. Preserve stable story, acceptance, invariant, and finding IDs, and document changes in `Revision Notes`.

## 4. Delta Review

Start an independent reviewer with:

```text
Mode: DELTA
Design doc: <path>
Previous reviewed revision: ...
Current revision: ...
Frozen Design Review Ledger v1:
<complete ledger>
Revision Notes:
<compact changed-section and disposition summary>
Resume checkpoint:
<checkpoint>
```

The reviewer verifies every open finding and revision-caused contradiction. A new blocker requires Critical/Major severity plus revision-caused or previously missed material-gap classification and a missed-in-initial-review explanation. Update ledger statuses without deleting history.

## Convergence

- Allow two revision/delta-review cycles by default.
- Allow a third only with an exceptional reason recorded before starting.
- Do not begin a fourth cycle.
- Minor improvements may remain deferred and do not block `Revised`.
- Resumption continues the persisted count; it does not grant a fresh allowance.

If the cap is reached, classify the cause as specification ambiguity, incomplete initial review, ineffective revision, or scope expansion and return `WORKFLOW_DID_NOT_CONVERGE`.

## Mark Revised

Mark the design `Revised` only when:

- No Critical or Major ledger item is open.
- Every story is implementation-ready.
- Stable criterion/invariant IDs are present.
- Deferred Minor items and residual risks are explicit.
- Either the clean INITIAL review examined the current requirements revision, or the latest DELTA examined the current revision after changes.

Add a dated changelog line, ensure `Revision Notes` references the review artifact and ledger disposition, and update the checkpoint to `REVISED`.

## Final Handoff

```markdown
## Design Review Loop Handoff v2
- Design doc:
- Review file:
- Entry state:
- Resumed: yes/no
- Resumed from:
- Final design revision:
- Ledger version:
- Initial reviews:
- Delta reviews:
- Open Critical:
- Open Major:
- Deferred Minor:
- Final state: Revised | Specification required | Workflow did not converge
- Status marked Revised: yes/no
- Residual risk:
- Required next action:
```

## Operating Rules

- Do not send full conversation history to workers.
- Reviewers remain read-only and separate from revision workers.
- Do not require zero optional improvements.
- Do not silently rewrite the frozen ledger.
- Do not start feature delivery from this skill.
- Model selection is outside this skill.
