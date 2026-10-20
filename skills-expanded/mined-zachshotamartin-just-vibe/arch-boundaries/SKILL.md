---
name: arch-boundaries
description: "Find misplaced responsibilities, dependency cycles, and leaking abstractions. Use to inspect responsibility and dependency violations; arch-feature designs a new feature's placement."
---

# arch-boundaries

Find misplaced responsibilities, dependency cycles, and leaking abstractions.

## Choose this workflow

Use to inspect responsibility and dependency violations; arch-feature designs a new feature's placement.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; modules/services and intended responsibility rules.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Coupling, cycles, ownership leaks, and misplaced responsibilities; no automatic service extraction.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Inventory current responsibilities, data owners and dependency directions from composition roots, imports, schemas, network clients and deployment definitions. Mark inferred or inaccessible edges explicitly.
2. Trace a representative change and failure across the proposed boundary. Identify shared transactions, cycles, leaked internals and callers that would need coordinated release; file count alone is not evidence of a bad boundary.
3. Propose the smallest interface or ownership correction that reduces the demonstrated coupling. Specify allowed dependencies, compatibility, error semantics and enforcement in the existing build/test architecture.
4. Verify the boundary with a consumer-facing contract check and a forbidden-dependency example when appropriate. Estimate migration impact from actual consumers and keep unmeasured organizational benefits conditional.

## Technical method

- **Inspect:** Find dependency cycles, shared mutable tables, cross-module imports and repeated business rules at actual call sites.
- **Method:** Identify which owner enforces each invariant; propose a seam that removes a specific cycle or competing writer, with transition contracts.
- **Avoid misdiagnosis:** Folder moves can conceal unchanged coupling; a shared type is not inherently a boundary violation.
- **Check the result:** Trace the affected invariant before and after the proposed boundary, including a consumer failure and ownership of rollback.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).


## Decision branches

- **When a cycle is intentional and isolated behind an interface:** Assess change coupling and failure propagation before prescribing a split.

## Deliver and verify

- Boundary findings with examples and incremental repair options.
- Concrete dependency paths, violated responsibility, demonstrated cost and incremental correction.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A dependency cycle has a concrete path; a justified shared utility is not rejected merely for having many callers.

## Stop and recover

- Distinguish organizational preference from demonstrated architectural cost. Missing ownership rules become questions, not invented mandates.

## Example requests

- **Normal (inspect):** Find responsibility leaks and dependency cycles in billing.
- **Edge (inspect):** Assess a shared utility with many callers but no ownership violation.
- **Blocked (inspect):** Review boundaries without an ownership map; identify assumptions requiring team input.
