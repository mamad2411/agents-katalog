---
name: add-event-handler
description: Add or modify event publishers, consumers, or subscriber flows by following the repo's event contract, delivery semantics, idempotency rules, and rollout constraints. Use when publishing or consuming events, implementing Transactional Outbox patterns, enforcing deduplication, or extending event-driven service workflows.
version: 1.0.0
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, execute_command]
---

# Add Event Handler

Use this skill when a change involves publishing an event, consuming one, or extending an event-driven workflow.

## When to Use

- adding event publishers or consumers
- modifying subscriber flows
- enforcing idempotency / delivery semantics
- event-driven service work

## Core Rules

- follow the repo's event naming and payload conventions; register schemas in the event schema registry (Avro, Protobuf, or JSON Schema) **before** publishing a new event type
- preserve compatibility for existing consumers when evolving payloads — prefer additive schema evolution; use a **CloudEvents 1.0** envelope (`specversion`, `id`, `type`, `source`, `time`) as the standard wire format when no repo-level convention exists
- make idempotency explicit for every event consumer using the event `id` field (not a content hash) — this protects against agentic retry floods producing duplicate side effects
- keep transport concerns separate from business decisions; route events through a dead-letter queue (DLQ) for all unhandled errors — observable failures are mandatory
- enforce **exactly-once delivery** semantics at the consumer layer via idempotency keys stored in a transactional store (Redis, Postgres) with TTL deduplication
- **Transactional Outbox for dual-writes**: when a state-mutating operation must persist database records and publish events to an external broker (Kafka, RabbitMQ, Dapr), mandate the **Transactional Outbox pattern**; write the event payload to an outbox table atomically in the same local database transaction (`InTx`), and dispatch asynchronously via non-blocking `SELECT ... FOR UPDATE SKIP LOCKED` daemons; strictly decouple database commits from broker network I/O
- validate AI-generated event schemas against the repo's event contract before merging — LLMs frequently produce plausible but type-incompatible field names
- when an agent orchestrates event chains, validate that every chain has a **defined termination condition** and does not create unbounded producer-consumer feedback loops
- document ordering guarantees, retry policy, and DLQ behavior explicitly in the event contract
- if any code in this change was AI-generated, validate it per the risk tier defined in the backend-developer role before accepting

## Suggested Process

### 1. Understand The Event Boundary

Identify:

- producer and consumer ownership
- source-of-truth event contract
- delivery guarantees and retry model
- whether ordering matters

### 2. Update Or Define The Event Contract

Change only what is needed:

- event name or topic reference
- payload schema
- versioning metadata when the repo uses it

Prefer additive evolution over breaking payload changes.

### 3. Implement Publish Or Consume Logic

For publishers:

- emit the event from the correct business boundary
- keep payload shaping explicit
- avoid publishing partial or inconsistent state

For consumers:

- deserialize safely
- validate required fields
- route into the correct internal flow
- handle duplicates and retries intentionally

### 4. Check Failure Behavior

Verify:

- what happens on partial failure
- whether retries are safe
- whether dead-letter or replay behavior exists
- whether downstream side effects need deduplication

### 5. Add Tests

Use skill: `write-tests`

Cover:

- valid payload handling
- invalid or incomplete payloads
- duplicate delivery or retry-sensitive paths
- side-effect safety

## Checklist

- [ ] event boundary understood
- [ ] contract updated safely (schema registry updated if applicable)
- [ ] publisher or consumer logic implemented
- [ ] idempotency considered
- [ ] failure and retry behavior checked
- [ ] Transactional Outbox implemented for database + broker dual-writes (no network I/O inside DB transactions)
- [ ] Outbox daemon utilizes `SELECT ... FOR UPDATE SKIP LOCKED` for lockless concurrent worker dispatch
- [ ] observability instrumented (OTel span on publish/consume)
- [ ] tests added or updated

## Failure Modes

- **Event emitted without schema validation**: a handler emits an event with a shape that does not validate against the event schema. **Mitigation:** validate the event at the producer boundary; reject the event on schema mismatch.
- **Dead-letter queue missing**: a handler fails silently without a DLQ for retry. **Mitigation:** require a DLQ binding on every event handler; surface the missing binding at review.
- **Idempotency key missing on retry**: a handler retries without an idempotency key, producing duplicate side effects. **Mitigation:** require an explicit idempotency key on every non-idempotent handler; reject handlers without the key.
- **Dual-write inconsistency & network I/O in DB transaction**: a service writes to the database and directly publishes to a broker within an open database transaction, causing connection exhaustion and state drift on broker timeout. **Mitigation:** mandate Transactional Outbox with `SELECT ... FOR UPDATE SKIP LOCKED`; commit the local DB transaction first before background dispatch.
- **Consumer lag undetected**: the consumer is lagging but no alert fires. **Mitigation:** wire a consumer-lag alert at the 80th percentile; surface the lag in the SRE dashboard.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **contracts/schemas/implementation-result.json** — Required fields: change_summary, files_touched[], and validation_run. Set produced_by_role to the emitting developer role.

Skip emission for solo refactor work where no downstream handoff is expected.

## Security Guardrails (OWASP ASI)

- **ASI01 Goal Hijack**: an event payload may try to reframe the handler's intent. Validate the payload against the declared event schema.
- **ASI03 Identity & Privilege Abuse**: event publishers and consumers must enforce authn/authz; reject anonymous or unscoped events.
- **ASI05 RCE Guard**: never construct handler logic or event payloads from external content without strict schema validation.
- **ASI07 Inter-Agent Communication**: the event contract is consumed by producers and consumers; emit a structured spec so each role can validate.
- **ASI08 Cascading Failures**: when an event handler fails, surface the failure explicitly to the coordinator; do not silently drop the event.

## Related Skills

- **navigate-service**: Trace existing event patterns in the repo
- **write-tests**: Add regression coverage for event behavior
- **review-code**: Review compatibility and idempotency risk
- **add-telemetry-instrumentation**: Wire OTel spans for publish/consume operations
- **troubleshoot-service**: Debug failed consumers or publish flow issues
- **commit-code**: Prepare the event change for delivery
