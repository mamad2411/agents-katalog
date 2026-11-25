---
name: backend-service
description: "Implement a service with clear boundaries and validation. Use for a domain service implementation; api-design defines transport-facing contracts."
---

# backend-service

Implement a service with clear boundaries and validation.

## Choose this workflow

Use for a domain service implementation; api-design defines transport-facing contracts.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; service responsibility, request/event contracts, persistence, and error requirements.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

One service boundary and necessary integration; no unrelated service decomposition.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Identify transaction ownership and domain invariants, reusing the project's domain conventions.
2. Implement the service with input validation and persistence, keeping transport parsing outside business decisions and making dependency failures observable to callers.
3. Test observable success and failure behavior.

## Technical method

- **Inspect:** Trace transport parsing, validation, domain invariants, transaction ownership and downstream effects.
- **Method:** Keep business validation at the owning boundary; represent expected failures separately from infrastructure uncertainty.
- **Avoid misdiagnosis:** Broad catch-and-success fallbacks can report an order created when its durable write failed.
- **Check the result:** Exercise valid input, invalid input, authorization failure and a dependency failure after partial progress; verify persisted state as well as response.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- The task depends on framework defaults, middleware, RLS, server/client or deployment behavior: [Framework-specific review branches](../../references/security/frameworks.md).
- Language/runtime semantics, concurrency or resource ownership can change the result: [Language and runtime review methods](../../references/scenarios/language-review.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When one operation spans local persistence and an external effect:** Define outbox/reconciliation or compensating behavior before claiming atomicity.

## Deliver and verify

- Service implementation with its contract, effect/transaction boundaries, configuration guidance and success/failure checks.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A valid operation persists the intended effect; validation/dependency failure leaves a consistent state.

## Stop and recover

- Do not invent business rules or create production infrastructure. Missing external credentials block live verification, not local contract work.

## Example requests

- **Normal (apply):** Implement a narrow invitation service using existing validation and persistence patterns.
- **Edge (apply):** Implement order creation when notification fails after persistence.
- **Blocked (inspect):** Inspect service requirements with an unavailable dependency; use a contract fixture only.
