---
name: arch-tenancy
description: "Evaluate tenant isolation across authentication, storage, queries, and jobs. Use for system-wide tenant isolation; backend-permissions handles individual application checks and security-authz probes a concrete bypass."
---

# arch-tenancy

Evaluate tenant isolation across authentication, storage, queries, and jobs.

## Choose this workflow

Use for system-wide tenant isolation; backend-permissions handles individual application checks and security-authz probes a concrete bypass.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; tenant model, resource types, membership rules, and access boundaries.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Tenant identity propagation across APIs, storage, caches, jobs, exports, and support operations.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Map tenant ownership of each resource type, including shared resources and membership changes.
2. Follow tenant identity through API, database role, cache key, queue payload, file storage and support/admin paths, and identify missing isolation checks.

## Technical method

- **Inspect:** Trace authenticated tenant identity through queries, caches, queues, search, object storage and support access.
- **Method:** Define subject/action/resource/tenant checks at each boundary; derive identity from trusted context rather than a request body alone.
- **Avoid misdiagnosis:** An isolated HTTP route can still enqueue a job or populate a shared cache without tenant scope.
- **Check the result:** Run two synthetic tenants with overlapping resource IDs through direct, cached, exported and asynchronous paths.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).

## Decision branches

- **When an identity belongs to several organizations:** Separate membership from selected-tenant authorization at each effect boundary.

## Deliver and verify

- Resource ownership and propagation matrix with concrete bypass candidates, and proposed negative tests or migration design.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Background jobs preserve tenant identity; multi-organization users cannot access an unselected unauthorized organization.

## Stop and recover

- Do not use real cross-tenant data for probing. Policy ambiguity must be resolved before implementing access changes.

## Example requests

- **Normal (inspect):** Audit organization isolation across caches, jobs, APIs, and exports.
- **Edge (inspect):** Review multi-organization users and background exports.
- **Blocked (inspect):** Inspect tenancy without authorized test identities; use source and synthetic fixtures only.
