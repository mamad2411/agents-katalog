---
name: security-authz
description: "Test access decisions and cross-user or cross-tenant exposure. Use for permission bypass inspection; backend-permissions implements an accepted access matrix, and security-fix repairs a confirmed bypass."
---

# security-authz

Test access decisions and cross-user or cross-tenant exposure.

## Choose this workflow

Use for permission bypass inspection; backend-permissions implements an accepted access matrix, and security-fix repairs a confirmed bypass.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Security methods](../../references/packs/security.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect; access matrix, endpoints/resources, roles/tenants, and authorized test identities.

**Pack prerequisites:** Defined application boundary, authorized code/environment, relevant trust/access rules, and evidence sources. Default to defensive inspection; active tests use owned or explicitly authorized isolated targets. Minimize sensitive evidence and never print usable credentials.

- **Infer from evidence:** Resolve the requested surface, source/runtime version, reachable callers and actual trust/access boundaries.
- **Reasonable default:** Start with source analysis and bounded owned fixtures; treat scanner output as leads and preserve legitimate controls.
- **Ask only when needed:** Ask when target authorization or necessary trust semantics are unresolved before active probing; source inspection need not wait for production access.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Authorization bypass, object ownership, privilege escalation, and cross-tenant access.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Trace policy checks at server and data boundaries.
2. Design allowed and denied cases across direct IDs, alternate endpoints and methods, exports and background tasks, using synthetic identities.
3. Execute only permitted isolated probes.

## Technical method

- **Inspect:** Inspect identity derivation, subject/action/resource rules, tenant filters and indirect entry points.
- **Method:** Use the identity guide to trace object-level and function-level authorization, including mass assignment, exports and workers.
- **Avoid misdiagnosis:** Authentication middleware proves identity, not ownership; an admin test can bypass the same controls being evaluated.
- **Check the result:** Verify denied cross-user/cross-tenant requests cause no reads or writes and that legitimate access remains possible using isolated identities.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Security worked example](../../references/examples/security.md).
- Identity, ownership, tenant isolation, replay or privilege changes affect the task: [Identity and authorization](../../references/security/identity.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves bug bounty, authorized pentest, security proof; load only the matching method: [Authorized vulnerability research](../../references/methods/authorized-security-research.md).
- Choosing which access paths to test and what evidence settles a finding: [Review selection and evidence](../../references/security/review.md).
- Access is enforced through database row-level security, DRF querysets, Spring matchers or Next.js server actions: [Framework authorization pitfalls](../../references/security/frameworks.md).
- Testing cross-user or cross-tenant access with synthetic identities: [Authentication and authorization scenarios](../../references/scenarios/auth.md).

## Decision branches

- **When policy itself is unspecified:** Separate demonstrated missing enforcement from an unresolved product permission decision.

## Deliver and verify

- Subject/action/resource cases, enforcement paths, evidence-backed findings with safe reproduction, and remediation or check proposals.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Direct object references cannot bypass tenant policy; privileged and ordinary roles are tested distinctly.

## Stop and recover

- Do not use unauthorized real accounts or retrieve private records as proof. Missing policy prevents judging ambiguous access as a confirmed vulnerability.

## Example requests

- **Normal (inspect):** Audit direct API access to another organization's records using isolated identities.
- **Edge (inspect):** Audit an endpoint that hides buttons but accepts cross-tenant direct requests.
- **Blocked (inspect):** Review source without real accounts or retrieving private records as proof.
