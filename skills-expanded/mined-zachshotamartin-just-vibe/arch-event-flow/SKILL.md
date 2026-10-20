---
name: arch-event-flow
description: "Design event delivery, retries, ordering, and failure handling. Use for asynchronous consistency and delivery design across producers and consumers; backend-jobs implements worker mechanics and backend-idempotency implements single-effect handling for one operation or handler."
---

# arch-event-flow

Design event delivery, retries, ordering, and failure handling.

## Choose this workflow

Use for asynchronous consistency and delivery design across producers and consumers; backend-jobs implements worker mechanics and backend-idempotency implements single-effect handling for one operation or handler.

Read [shared execution](../../references/execution.md) for context/mode/authority handling and [Architecture methods](../../references/packs/architecture.md) for tool selection and operational details. Resolve these paths from this skill file; all runtime assets ship inside the plugin.

## Input and mode

Use the complete request appended to this invocation, preserving all constraints and references. Default mode: **plan**. Plan; event source, consumers, delivery guarantees, and failure requirements.

**Pack prerequisites:** Readable source, infrastructure/configuration definitions, and any supplied system documentation. Runtime telemetry is optional evidence, never assumed available. Architecture proposals remain plans until implementation is requested.

- **Infer from evidence:** Trace current entry points, data owners, deployment units and documented constraints before proposing boundaries.
- **Reasonable default:** Prefer extending an existing owner while scale or organizational evidence is absent; mark capacity estimates as assumptions.
- **Ask only when needed:** Ask for an unresolved consistency, compatibility or ownership requirement only if it changes the design; missing telemetry limits capacity claims, not source mapping.

Resolve any task-specific tools, target identity and evidence before dependent actions. No external connection is assumed.

## Scope

Event ownership, ordering, deduplication, retries, dead letters, and replay.

No source changes in inspect/plan. Save only requested planning artifacts. A separately requested repair uses the relevant implementation workflow.

## Execute

1. Draw the write/commit/publish/ack sequence across transaction boundaries.
2. Place a crash between each pair to find loss and duplicate windows; specify identifiers, schemas, replay identity and effect ownership.
3. Define recovery and observability for each failure point.

## Technical method

- **Inspect:** Locate transaction commit, publish, consumer claim, business effect and acknowledgment boundaries.
- **Method:** Draw a crash between each durable step; align outbox publication and consumer deduplication with the business transaction where supported.
- **Avoid misdiagnosis:** Delivery ordering on one partition does not order all entities, and broker acknowledgment does not prove a business effect committed.
- **Check the result:** Replay a duplicate, deliver versions out of order, and interrupt after the effect before acknowledgment; check one intended effect.

## Read when relevant

- When a concrete decision or deliverable example would clarify this workflow: [Architecture worked example](../../references/examples/architecture.md).


## Decision branches

- **When database commit and broker publish are separate:** Compare a transactional outbox or explicit reconciliation with the actual loss window.

## Deliver and verify

- Event sequence diagram, delivery contract, and a failure-point table covering loss, duplicate, reordering, poison messages and recovery, with validation scenarios.

Verify these observable conditions when applicable to the actual task; do not claim they were exercised from merely reading this file:

- Duplicate and out-of-order deliveries have defined outcomes; a producer crash between database and broker operations is addressed.

## Stop and recover

- Do not promise exactly-once effects without a concrete consistency mechanism. Avoid choosing infrastructure without throughput and operational constraints.

## Example requests

- **Normal (plan):** Plan webhook-to-ledger processing with duplicate and reordered events.
- **Edge (plan):** Design order events with duplicate delivery and a producer crash after commit.
- **Blocked (inspect):** Assess event flow when broker guarantees are unknown; keep guarantees conditional.
