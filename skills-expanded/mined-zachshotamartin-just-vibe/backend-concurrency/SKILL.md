---
name: backend-concurrency
description: "Investigate races, locking, and competing updates. Use for violated invariants under competing operations; backend-idempotency handles repeat identity."
---

# backend-concurrency

Investigate races, locking, and competing updates.

## Choose this workflow

Use for violated invariants under competing operations; backend-idempotency handles repeat identity.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **inspect**. Inspect for diagnosis; apply for an explicit fix to the violated invariant. Requires race symptom, shared resources, transaction semantics, and concurrency evidence.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Competing updates, locks, isolation, and atomicity.

Inspect/plan: inspect or propose; save requested artifacts only. Apply: edit the requested local implementation and perform relevant bounded checks while preserving unrelated work. Live data changes, remote actions and paid jobs require their resolved target and existing session authorization.

## Execute

1. Write the shared invariant and the read/decide/write interleaving that violates it. Identify every worker/process and the actual shared boundary; list durable writes, external effects and cancellation points separately.
2. Choose the narrowest supported atomicity mechanism for that boundary: a conditional write, transaction, version check or shared lock. Define who starts and ends the transaction or lease; never accidentally commit or roll back a caller-owned transaction.
3. Validate before irreversible work and keep related invariant checks inside the serialization boundary when their inputs can race. Handle lock acquisition failure, deadlock/serialization conflict and cancellation with bounded retries only when replay is safe.
4. Force contention using separate real connections or workers and deterministic coordination. Exercise success, rejection, interruption after partial work and cleanup; assert final state and number of effects, not just the number of returned responses.

## Technical method

- **Inspect:** Write the invariant and a concrete violating interleaving; inspect isolation, lock order and actual worker topology.
- **Method:** Choose supported conditional updates, version checks or transactions at the shared state boundary; retry whole units only when safe.
- **Avoid misdiagnosis:** A process mutex does not protect multiple servers, and a pre-transaction balance read can become stale.
- **Check the result:** Coordinate separate workers/connections at the contested read and verify one valid outcome, bounded retry and rollback after injected failure.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- Language/runtime semantics, concurrency or resource ownership can change the result: [Language and runtime review methods](../../references/scenarios/language-review.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When a caller already owns a transaction:** Follow the API contract: participate with documented savepoint semantics or reject before touching it. Do not use unconditional commit/rollback cleanup that can consume unrelated work.
- **When multiple processes share the resource:** A process-local mutex cannot establish the shared invariant. Verify at the storage or service boundary used by all writers.

## Deliver and verify

- Violating interleaving, invariant and ownership boundary, selected mechanism, retry/cleanup behavior, contention and interruption results.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Independent workers preserve the invariant under contention. Failed operations leave owned resources usable, preserve caller-owned work, and cannot return success for an uncommitted or duplicated effect.

## Stop and recover

- No live contention experiments implicitly. Do not solve local races with process-local locks when multiple processes share the resource.

## Example requests

- **Normal (inspect):** Investigate two concurrent reservations exceeding inventory capacity.
- **Edge (apply):** Prevent two concurrent reservations from selling the final available seat twice.
- **Blocked (inspect):** Review concurrency logic without performing live contention experiments.
