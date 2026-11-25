---
name: spec-review-gauntlet
description: "Compatibility entrypoint for pre-implementation Spec Bundle review. Canonical readiness and review rules live in the role workflows."
user-invocable: false
---

# Spec Review Compatibility Entry

Use `core-workflow-contract`, `specification-writer-workflow`, `technical-architect-workflow`, and `quality-assurance-workflow` for the actual gate. This skill only preserves the existing route.

Before MEDIUM/LARGE implementation, confirm:

- the target-local bundle contains `requirements.md`, `design.md`, and `tasks.md` and passes the bundled validator;
- requirements, design decisions, tasks, acceptance checks, and verification are traceable;
- requirements/design/tasks agree, contain no unresolved placeholders, reuse current project boundaries, and split work into independently reviewable tasks;
- every task names an owner agent lane, independent reviewer agent lanes, write set, dependencies, and progress recovery fields;
- `tasks.md` contains the canonical Progress Ledger columns: `Task ID`, `Status`, `Owner`, `Reviewer`, `Last updated`, `Verification`, `Evidence`, `Next action`, and `Notes`;
- new behavior and fixes have a feasible RED test or reproducible check;
- public-contract, schema, auth, dependency, release, and UI risks have the required review lanes.

Classify every finding as:

- `spec_blocker`: missing or contradictory requirement, boundary, default, or traceability; revise the spec.
- `clarification_needed`: a user/product decision is required; stop for PM clarification.
- `implementation_todo`: the design is sound but implementation must track a concrete detail; may proceed.
- `risk_note`: non-blocking residual risk tracked through verification; may proceed.

Return `ready`, `ready_with_concerns`, or `not_ready`, plus blocking findings, non-blocking concerns, traceability gaps, required edits, satisfied/missing gates, and next stage (`implementation | revise_spec | clarify | split_scope`). Do not restate the complete SDD workflow.
