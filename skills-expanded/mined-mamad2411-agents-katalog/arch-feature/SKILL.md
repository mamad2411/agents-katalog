---
name: arch-feature
description: "Design where a feature belongs within the existing architecture. Use to place an accepted feature within a system; spec resolves unclear product behavior."
---

# arch-feature

Design where a feature belongs within the existing architecture.

## Choose this workflow

Use to place an accepted feature within a system; spec resolves unclear product behavior.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; feature specification, current architecture, and scale/compatibility constraints.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Placement of one feature across modules, services, storage, and interfaces.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Translate acceptance criteria and quality constraints into responsibilities, data ownership and interfaces. Trace an existing normal and failure path to locate the natural owner before proposing a new component.
2. Compare extending the current module, introducing an internal boundary and deploying a separate service. Assess data consistency, latency, independent rollout and operational ownership against demonstrated requirements.
3. Specify the chosen contract, compatibility window, failure/retry behavior and observability. Define who writes each datum and who reconciles partial effects; diagrams must distinguish observed code dependencies from proposed runtime edges.
4. Plan incremental implementation with a verification and recovery condition for each phase. Identify the smallest experiment that could overturn a material assumption before committing to an expensive boundary.

## Technical method

- **Inspect:** Inspect acceptance criteria, existing data owners, extension points and deployment constraints.
- **Method:** Place each new behavior with the owner able to enforce its invariant; compare a module extension with a new runtime boundary using actual operational needs.
- **Avoid misdiagnosis:** A new service adds network failure and consistency work even when its code is small.
- **Check the result:** Walk create/read/failure paths through the proposed design and identify every consumer or schema requiring compatibility.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).


## Decision branches

- **When the feature spans two data owners:** Define consistency and failure semantics before selecting synchronous calls or events.

## Deliver and verify

- Requirement-to-owner map, alternatives and decisive evidence, target contracts/data ownership, phased implementation with checks and recovery limits.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Existing domain rules stay owned by one clear boundary; error and rollback paths are covered.

## Stop and recover

- Do not introduce a service or datastore solely for stylistic separation. Flag decisions requiring workload or ownership information.

## Example requests

- **Normal (plan):** Design where organization invitations fit in the existing architecture.
- **Edge (plan):** Design a feature that updates billing and access without a distributed transaction.
- **Blocked (inspect):** Plan placement while an external consumer contract is unavailable.
