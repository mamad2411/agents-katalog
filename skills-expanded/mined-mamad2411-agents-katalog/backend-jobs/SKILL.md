---
name: backend-jobs
description: "Implement background processing, scheduling, and recovery. Use for durable background work; arch-event-flow defines cross-service consistency."
---

# backend-jobs

Implement background processing, scheduling, and recovery.

## Choose this workflow

Use for durable background work; arch-event-flow defines cross-service consistency.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Backend methods](../../references/packs/backend.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **apply**. Apply; job purpose, payload, scheduling/retry policy, concurrency, and environment.

**Pack prerequisites:** Service source, data/interface contracts, framework/runtime versions, and test environment. Default apply operations target local code and isolated tests; live infrastructure/data mutations require their own requested scope.

- **Infer from evidence:** Trace service callers, request contracts, authorization, transactions, retries and existing test infrastructure.
- **Reasonable default:** Use the existing persistence and framework; isolate local tests from live services.
- **Ask only when needed:** Resolve ambiguous durability, duplication or consistency requirements before encoding them; absent production access does not prevent local implementation.

Declared evidence requirements: `project.read`. Use actual host discovery or adequate supplied artifacts; unavailable evidence remains blocked/unknown.

## Scope

Worker implementation and local/test registration; live scheduling must be requested.

Apply: only the requested local changes and relevant isolated verification. Inspect/plan requests remain inspection/planning. External actions require their exact action and target in session authorization.

## Execute

1. Specify payload version, stable job identity, lease expiry, ack timing, bounded retry and dead-letter inspection before coding the worker.
2. Implement idempotent effects and checkpoints where needed.
3. Test crash and restart before and after the effect.

## Technical method

- **Inspect:** Inspect queue delivery guarantees, claim/lease mechanism, retry policy, payload version and effect identity.
- **Method:** Couple durable progress with business-effect deduplication; define stale lease takeover, poison-message handling and resumable checkpoints.
- **Avoid misdiagnosis:** Acknowledging before durable progress loses work; assuming a timed-out worker stopped can duplicate an effect.
- **Check the result:** Interrupt before effect, after effect and before acknowledgment, then restart; verify bounded retries and no duplicate business result.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Backend worked example](../../references/examples/backend.md).
- The affected project uses Django / DRF: [Django / DRF](../../references/frameworks/django.md).
- The affected project uses FastAPI: [FastAPI](../../references/frameworks/fastapi.md).
- The affected project uses Spring Boot: [Spring Boot](../../references/frameworks/spring-boot.md).
- The task specifically involves kubernetes, readiness probe, rolling update; load only the matching method: [Kubernetes release and failure recovery](../../references/methods/kubernetes-release.md).
- The task specifically involves flox, uncloud, dev environment, reproducible environment; load only the matching method: [Flox, containers and reproducible development](../../references/methods/reproducible-environments.md).
- The task specifically involves tail latency, latency critical, p99, benchmark optimization; load only the matching method: [Latency budgets and performance experiments](../../references/methods/latency-systems.md).

## Decision branches

- **When a worker dies after the external effect but before acknowledgement:** Reconcile the effect using durable identity before replaying it.

## Deliver and verify

- Worker and configuration with its job state machine, retry/lease rules, observable failure handling and crash-before/after-effect tests.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- A worker crash can resume without duplicate irreversible effects; poison messages stop retrying after a defined bound.

## Stop and recover

- No unrequested recurring jobs. Unknown provider delivery guarantees require explicit assumptions and corresponding safeguards.

## Example requests

- **Normal (apply):** Implement a resumable worker with bounded retries and poison-message handling.
- **Edge (apply):** Implement a resumable job that might receive the same message concurrently.
- **Blocked (inspect):** Plan worker behavior with unknown broker delivery guarantees.
