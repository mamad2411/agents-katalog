---
name: arch-modernize
description: "Plan an incremental transition to a target architecture. Use for staged architectural transition; refactor handles an internal structural change and migrate handles a version or platform transition."
---

# arch-modernize

Plan an incremental transition to a target architecture.

## Choose this workflow

Use for staged architectural transition; refactor handles an internal structural change and migrate handles a version or platform transition.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; current/target architecture, constraints, business continuity needs, and migration horizon.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Incremental modernization and transitional operation, not immediate replacement.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Inventory dependencies and identify a seam with separable traffic and data ownership.
2. Sequence compatibility layers and data movement, and define coexistence parity checks and retirement evidence before replacing the seam.

## Technical method

- **Inspect:** Inventory active consumers, supported versions, write ownership and persisted representations.
- **Method:** Define expand/coexist/switch/retire phases, reconciliation and exit criteria; identify the last point at which old readers remain safe.
- **Avoid misdiagnosis:** Dual writes without recovery can diverge; code rollback cannot recover discarded data.
- **Check the result:** Interrupt a transition with old and new clients active, resume reconciliation, and verify fallback before retiring the old path.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).


## Decision branches

- **When old and new systems write the same records:** Specify source of truth, conflict handling and reconciliation before dual operation.

## Deliver and verify

- Phased migration architecture with each phase's working state, the coexistence plan, cutover conditions, irreversible boundaries and recovery checkpoints.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Each phase leaves a working system; old components are retired only after dependent traffic and data ownership move.

## Stop and recover

- Do not assume a big-bang rewrite is necessary. Flag irreversible transitions and missing operational ownership.

## Example requests

- **Normal (plan):** Plan an incremental extraction of billing while the old app keeps running.
- **Edge (plan):** Modernize a monolith while old reports still query its database.
- **Blocked (inspect):** Plan modernization without dependency ownership; list blocking unknowns by phase.
