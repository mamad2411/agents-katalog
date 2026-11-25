---
name: sync-protocol
description: Reconcile stable repository instructions after a material contract change.
---

# Sync protocol

Use this skill when the user requests protocol synchronisation.

Use this skill when implementation materially changes a stable repository contract.

Do not invoke this skill after ordinary feature work.

## Scope

- Read accepted product intent relevant to the contract change.
- Read the current Project Specifics.
- Read the implementation evidence for the contract change.
- Edit only the Project Specifics region of `AGENTS.md`.
- Edit an existing `EXPERIENCE.md` only when interaction policy changed.
- Edit an existing `DESIGN.md` only when presentation policy changed.
- Preserve compatible human additions.
- Preserve unrelated project rules.

## Reconciliation

- Make stable instructions match verified implementation reality.
- Keep commands exact.
- Keep validation gates executable.
- Keep architecture boundaries current.
- Keep security boundaries current.
- Keep external-operation gates current.
- Keep interaction policy current when applicable.
- Keep presentation policy current when applicable.
- Remove superseded stable instructions.
- Avoid copying current task status into stable instructions.
- Avoid copying execution history into stable instructions.
- Surface contradictions that require a product decision.

## Boundaries

- Avoid editing `BUILD_STATE.md`.
- Avoid editing `GOVERNANCE.md`.
- Avoid editing `ROADMAP.md`.
- Avoid creating `EXPERIENCE.md`.
- Avoid creating `DESIGN.md`.
- Avoid inventing execution strategy.
- Avoid broadening the approved objective.
- Use `plan-implementation` when execution strategy must change materially.
- Use `shape-concept` when accepted product intent must change.

## Delivery

- Apply the reconciliation within the approved objective.
- Report every changed stable instruction.
- Report every unresolved contradiction.
- Continue the approved implementation objective after reconciliation.
