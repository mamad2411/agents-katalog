---
name: backend-permissions
description: "Define and test authorization for roles, resources, and ownership. Use for application action/resource policy; security-authz audits suspected bypasses, db-access covers database roles and row policies, and arch-tenancy covers propagation across the whole system."
---

# backend-permissions

Define and test authorization for roles, resources, and ownership.

## Choose this workflow

Use for application action/resource policy; security-authz audits suspected bypasses, db-access covers database roles and row policies, and arch-tenancy covers propagation across the whole system.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan for policy definition; apply for explicit implementation. Requires roles, actions, ownership, tenant rules, and exceptions.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Server-side resource authorization across all relevant entry points.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Build subject/action/resource/tenant cases as an access matrix, and locate the server-side enforcement boundaries.
2. Inspect alternate read, write and export paths and ownership transfers, and implement consistent checks when requested.
3. Test cross-user, cross-tenant and indirect access with positive and negative cases.

## Technical method

- **Inspect:** Build a subject/action/resource/tenant matrix from the product policy and locate all entry points.
- **Method:** Enforce authorization using trusted identity and server-owned resource scope, including workers, downloads and bulk operations.
- **Avoid misdiagnosis:** A hidden button or unguessable identifier does not enforce permission; an admin in one tenant is not automatically a global admin.
- **Check the result:** Use two isolated users/tenants and verify denied requests leave no side effects while valid owner/admin requests still work.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When policy is ambiguous for one role/resource combination:** Isolate that decision while continuing checks for unambiguous denials and allowed paths.

## Deliver and verify

- Access matrix, enforcement locations, enforcement changes if authorized, and positive/negative isolation checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Owners can perform intended actions; direct-ID requests cannot bypass tenant restrictions.

## Stop and recover

- Ambiguous policy blocks that decision, not unrelated analysis. Never rely solely on hidden UI buttons as enforcement.

## Example requests

- **Normal (plan):** Define read/update/export access rules for organization-owned invoices.
- **Edge (apply):** Add permission checks for direct-ID access and background exports.
- **Blocked (inspect):** Audit source without real tenant accounts; use synthetic identities and state assumptions.
