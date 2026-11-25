---
name: planning-artifact-lifecycle
description: Lifecycle management for planning artifacts — versioning triggers, CAM §7.1 enforcement, presentation protocol, and deletion rules.
category: General
---

# Planning Artifact Lifecycle (v1)

> **Skill ID:** `planning-artifact-lifecycle`<br>
> **Version:** 1.0.0<br>
> **Standard:** [Agent Skills (agentskills.io)](https://agentskills.io)<br>
> **Layer:** Base

## Composition Rationale

This is a **base skill** — it owns the lifecycle protocol for planning
artifacts: when to version up, how to enforce CAM §7.1 continuity, how
to present artifacts for approval, and when/how to delete them. It
complements the naming convention in
[`planning-artifact-naming`](../planning-artifact-naming/SKILL.md)
(which covers *how to name* artifacts) by covering *how to manage*
them over time.

Step 3 delegates the deterministic construction of a new version to the
[`versioned-artifact-superset-build`](../versioned-artifact-superset-build/SKILL.md)
base skill (vN verbatim + deltas appended), and the post-hoc coverage
verification gate to the audit skill in this folder (see Related Skills).

## Environment & Dependencies

| Requirement | Notes |
| --- | --- |
| Read/write access to `docs/` in the main repository | All artifacts live under `docs/` per [Traceability Mandate](../../../../../ai-agent-rules/ai-agent-planning-rules.md#10-task-artifact-synchronization) |
| Python 3.12+ | For `versioned-artifact-superset-build` construction script (Step 3) |
| `git` | For diff-based CAM §7.1 comparison |
| A text editor or diff tool | For line-by-line comparison between versions |

## When to Use

- When creating a new planning artifact (task.md, implementation-plan,
  commit-preview, walkthrough, sub-plan, audit-log, summary).
- When updating an existing versioned artifact (incrementing to vN+1).
- When user asks to delete or clean up planning artifacts.
- When CAM §7.1 enforcement is required before creating a new version.

## Artifact Types

This skill applies to ALL planning artifact types registered in
[`planning-artifact-naming` §2.1](../planning-artifact-naming/SKILL.md#21-registered-types):
task, implementation-plan, commit-preview, walkthrough,
skill-creation-plan, skill-documentation-plan, audit-log, summary.

### Task.md vs Versioned Artifacts

`task.md` is a **live checklist** — it is edited in place, NOT
versioned. All other artifact types are **versioned** — old versions are
NEVER overwritten by edits; a superseded version MAY be retired through
the ONE authorized path: coverage audit FULL + explicit user consent via
the `planning-superseded-version-retirement` composer (Step 5b).

## Step-by-Step Procedure

### Step 1 — Creation

1. Determine the artifact type per the task at hand.
2. Name the file per the formula in
   [`planning-artifact-naming` §1](../planning-artifact-naming/SKILL.md#1-formula):
   `docs/<date>_<session-id>_<session-name-slug>_<artifact-type>_v<version>.md`.
3. Start versioning at `v1`.
4. Write the artifact to `docs/` in the **main repository** (NOT in a
   Git submodule — planning history must not scatter into a submodule's
   commit graph).
5. Present the artifact to the user for review.

### Step 2 — Versioning Triggers

Create a new version (vN → vN+1) when ANY of the following occurs:

1. **Content change**: The scope, steps, or details of the plan change.
2. **Structural change**: The organization or sections are reordered,
   added, or removed.
3. **User-requested revision**: The user asks for a different approach.
4. **CAM §7.1 violation detected**: A line-by-line comparison against
   the previous version reveals dropped content without documented
   rationale (see Step 3).

NEVER edit a versioned artifact in place. Always create vN+1 alongside
vN.

### Step 3 — CAM §7.1 Enforcement (Verbatim-Superset Construction + Verification)

The Verbatim-Superset Construction mandate (CAM §7.1) is STRICTER than
the historical restore-or-rationalize rule: vN+1 MUST be vN's text kept
verbatim with vN+1's deltas appended — never rewritten, reworded,
reordered, or selectively dropped (even with a Change History rationale).
The construction is deterministic; the audit is post-hoc verification.

**BEFORE** presenting vN+1, do BOTH:

1. **CONSTRUCT** vN+1 via the
   [`versioned-artifact-superset-build`](../versioned-artifact-superset-build/SKILL.md)
   base skill:
   `scripts/build-version-superset.py --old <vN> --new <vN+1> --deltas <deltas.md>`
   — this guarantees vN's text is byte-verbatim in vN+1 (optionally
   `--change-history-row` to stamp the vN+1 row in the Change History
   table, then run `--verify` before any manual edits). Author the
   vN+1 deltas block yourself (judgement tier) and pass it as `--deltas`.
2. **VERIFY** the result — run the deterministic `--verify` mode of the
   builder immediately after the build; then (optional cross-check)
   the [`planning-version-coverage-audit`](../planning-version-coverage-audit/SKILL.md)
   gate returns FULL mechanically when the construction was followed.

Manual fallback (NO script available, e.g. a runtime without Python 3.12):
perform a literal line-by-line comparison against vN:

1. Read vN and vN+1 side by side (or diff them).
2. For every block of text present in vN but absent in vN+1:
   - If the content is still valid → restore it verbatim in vN+1.
   - If the content is intentionally removed → document the rationale
     in the Change History table of vN+1 (this is the ONLY path, and it
     does NOT license removal — the construction mandate forbids
     dropping previous content even with rationale).
3. Any dropped task, alert, or requirement MUST be either restored or
   explicitly listed in the Change History with a rationale for its
   removal.
4. Summarizing integrated logic from sub-plans is a violation of CAM
   §7.1 — all literal detail must be preserved.

**Violation example**: v3 drops a "Gap Analysis" table that v2 had,
without mentioning the removal in Change History. This is a CAM §7.1
violation — the table must be restored or its removal rationalized.

### Step 4 — Presentation & Approval

1. Present the artifact to the user in the conversation.
2. Explicitly ask for confirmation or adjustments.
3. Do NOT act on the artifact's content (execute steps, make changes)
   until the user explicitly approves (e.g., "start", "go ahead",
   "looks good").
4. If the user requests changes: create vN+1 and repeat from Step 2.

### Step 5 — Deletion & Retirement

Planning artifacts MAY be deleted after their content has been executed
or superseded. Choose the branch that matches the situation:

- **a) Content executed, nothing else needs the files** → apply the
  generic deletion rules below (batch, keep-current, task-last) on user
  confirmation.
- **b) A superseded version (vN) is fully covered by a surviving
  version (vN+1)** → DELEGATE to the
  [`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md)
  composer: coverage audit MUST be FULL and explicit user consent is
  REQUIRED before any deletion.
- **c) Both versions still needed** → keep both; do not delete.
- **d) macOS retirement NEVER uses `rm`** → always `trash`
  (recoverable); `rm` is forbidden per AGENTS.md rule 7.

Generic deletion rules (branch a):

1. **User must initiate or explicitly confirm**: Never delete artifacts
   without the user saying "yes", "delete", or "clean up".
2. **Batch deletions**: When user confirms cleanup, delete ALL stale
   artifacts in a single batch (not one at a time).
3. **Keep current version**: The latest version of each artifact type
   SHOULD be retained until its content is fully executed and confirmed.
4. **`task.md` retention**: The live task tracker should be the last
   artifact deleted, after all tasks are confirmed complete.

### Step 6 — Fresh Start Protocol

When a "Fresh Start" version (vN) is declared per
[planning rules §9](../../../../../ai-agent-rules/ai-agent-planning-rules.md#9-plan-versioning--ssot-integrity-history-
mandate):

1. All subsequent plans (vN+1, vN+2, etc.) MUST reset the Change
   History and User Questions & Answers sections to only include items
   from vN onwards.
2. This is a strict exception to the full history mandate.
3. The Fresh Start declaration MUST be explicitly communicated to and
   approved by the user.

A planning artifact is retired ONLY per branch b above, whose gates are
owned by the composer. Note §2: "old versions are NEVER overwritten by
edits; a superseded version MAY be retired through the ONE authorized
path — coverage audit FULL + explicit user consent — via the
`planning-superseded-version-retirement` composer (macOS: `trash`,
never `rm`)."

## SSOT Compliance

- The **naming convention** is owned by
  [`planning-artifact-naming`](../planning-artifact-naming/SKILL.md).
- The **CAM §7.1 mandate** and **plan versioning rules** are owned by
  [`ai-agent-planning-rules.md`](../../../../../ai-agent-rules/ai-agent-planning-rules.md)
  (§7.1, §9).
- The **artifact storage location** is owned by
[`ai-agent-planning-rules.md` §10](../../../../../ai-agent-rules/ai-agent-planning-rules.md#10-task-artifact-
  synchronization).
- This skill does NOT redefine any of them — it operationalizes them
  into a step-by-step lifecycle procedure.

## Related Skills

- [`pre-commit-verification-protocol`](../../pre-commit-verification-protocol/SKILL.md)
  — verification pipeline to run before staging any artifact-related
  changes.
- [`git-atomic-commit-construction`](../../../git-atomic-commit-construction/SKILL.md)
  — consumed when a commit-preview artifact is approved and commits
  need execution.
- [`skill-factory`](../../../skill-factory/SKILL.md) — consumed when
  creating skill-creation-plan or skill-documentation-plan artifacts.
- [`planning-version-coverage-audit`](../planning-version-coverage-audit/SKILL.md)
  — the mandatory coverage gate used before retiring a superseded
  version (Step 5b).
- [`planning-superseded-version-retirement`](../planning-superseded-version-retirement/SKILL.md)
  — the composer that owns the authorized retirement path (Step 5b).

## Traceability

- Created: 2026-07-03
- Source: OpenCode config versioning & preservation session. The
  lifecycle was practiced across 5 commit-preview versions (v1→v5),
  7 implementation-plan versions, and a final cleanup phase where
  all stale artifacts were batch-deleted on user confirmation.
