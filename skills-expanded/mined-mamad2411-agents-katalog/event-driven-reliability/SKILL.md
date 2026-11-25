---
name: event-driven-reliability
description: "Design or review reliable event consumers, queue workers and replayable asynchronous workflows. Use for at-least-once delivery, duplicate processing, idempotency keys, durable deduplication, retry and dead-letter policy, poison messages, replay safety, ordering, backpressure, consumer crash windows, outbox or inbox patterns, and transactions that combine local state with external side effects. Produces explicit delivery assumptions, stable event and business identities, atomicity boundaries, bounded failure handling, retention horizons, replay controls and verification cases. Not for responding to a live incident (`incident-response`), adding metrics and traces (`instrumentation`), general HTTP API contracts (`api-design`), operator procedures (`runbook`), or backup and disaster-recovery architecture (`backup-recovery-design`)."
allowed-tools: Read, Write, Edit, Grep, Glob
---

# Event-Driven Reliability

Treat delivery guarantees as transport properties, not proof that a business action occurs
exactly once. Design each consumer around the points where it can crash, redeliver, reorder,
or lose the ability to retry.

## Establish the contract

Write down these facts before choosing a pattern:

| Concern | Required decision |
| --- | --- |
| Event identity | Immutable identifier assigned once by the logical event producer |
| Business identity | Domain key for the action, such as order plus transition or invoice plus period |
| Delivery | At-most-once, at-least-once, or a documented broker-specific guarantee |
| Ordering | Scope of order, reorder window, and response to a stale event |
| Completion | Durable state that proves the business outcome, not merely handler return |
| Retry horizon | Maximum useful age, attempt limit, and elapsed-time limit |
| Replay horizon | Oldest retained source event and oldest retained deduplication record |
| Side effects | Every local write, emitted event, and remote call |

Keep event identity distinct from business identity. A producer retry may repeat one event
ID, while two different events may request the same business transition. State which identity
guards transport duplicates and which invariant prevents a repeated business action.
Version the envelope and payload schema. Define how the consumer rejects an unknown envelope,
upcasts supported payloads, and preserves the original identity through conversion.

If the broker's delivery mode, acknowledgement deadline, retention, ordering scope, or
dead-letter behaviour is unknown, label it as an assumption. Do not infer it from product
terms such as “exactly once.”

## Map the crash windows

For one message, draw the ordered steps from receive through acknowledgement. At each edge,
ask what happens if the process stops immediately before and immediately after it:

1. receive and validate the envelope;
2. claim or observe the idempotency record;
3. commit local state;
4. initiate each external effect;
5. record the effect outcome;
6. publish follow-up events;
7. acknowledge the input.

Record whether recovery repeats, resumes, reconciles, or abandons the step. Acknowledge only
after the durable completion condition is true. If acknowledgement fails after completion,
redelivery must find evidence that makes repeating the action safe.

## Select an atomicity pattern

Use a database uniqueness constraint or equivalent durable conditional write on the chosen
identity, not an in-memory cache. Retain the record for at least the maximum of broker retention,
replay range, producer retry window, and operational delay, plus clock uncertainty. If that
retention is unaffordable, narrow the supported replay horizon or use a domain invariant that
remains valid longer.

When the effect is a local database change, insert the inbox or processed-event record and
apply the state transition in one transaction. A conflict should read the committed outcome
and return success only when that outcome satisfies the same request.

When publishing follows a local commit, write an outbox row in the same transaction. A relay
may publish it more than once, so downstream consumers still need idempotency. Define how the
relay claims work, retries, and marks publication without losing rows after a crash.

When the effect is a remote API or another non-transactional system, a local “processed” mark
cannot make both sides atomic:

- marking first can suppress an effect that never happened;
- calling first can repeat an effect after a crash and redelivery;
- marking last records success but does not close the call-to-record crash window.

Prefer a stable downstream idempotency key whose lifetime covers every retry and replay. If
the downstream cannot support it, persist an operation state machine before calling, attach a
stable correlation key, and reconcile uncertain outcomes through a read or provider record.
Require manual review when neither safe retry nor authoritative reconciliation exists.

Do not hold a database transaction open across an external call as a substitute for a
distributed transaction. It adds lock and timeout failure modes without making the remote
effect roll back.

## Bound retries and dead letters

Classify failures by action:

| Class | Action |
| --- | --- |
| Invalid or unsupported event | Quarantine without retry; preserve reason and identity |
| Permanent business rejection | Record the terminal outcome; acknowledge |
| Transient dependency failure | Retry with capped exponential backoff and jitter |
| Rate or capacity pressure | Reduce concurrency and honour an explicit retry time |
| Unknown external outcome | Reconcile before another attempt |
| Repeated or expired failure | Move to a dead-letter state and stop automated attempts |

Bound retries by attempts and elapsed time. Keep each attempt within the remaining processing
lease, or extend the lease through a documented mechanism under a bounded overall processing
budget. Cap backoff so the retry horizon is predictable. Define ownership, alert threshold,
retention, access controls, redrive criteria, and expiry for dead letters. Preserve enough of
the invalid payload for diagnosis without copying credentials, secrets, or unnecessary personal
data. A dead-letter queue without a disposition path is delayed data loss.

Prevent one poison message from monopolising a partition or worker. Limit concurrent retries,
separate retry traffic when it competes with fresh work, and stop pulling when dependencies or
local resource pools cross explicit limits. Resume below a lower threshold to avoid oscillation.
State the maximum in-flight messages, worker concurrency, per-key concurrency, and queue-age
objective. Preserve ordering only where the business invariant requires it.

## Design replay as a controlled change

Specify the replay source, immutable selection criteria, start and end positions, expected
count, destination, ordering policy, deduplication coverage, rate limit, owner, and audit record.
Confirm source retention still covers the requested range and that schemas, keys, and referenced
business data remain readable.

Run a dry-run that parses and classifies the selected events without producing effects. Report
events that would apply, skip, conflict, fail validation, or require reconciliation. A staging
replay is not evidence of production idempotency unless it uses equivalent identities and state.

Define stop conditions before execution: unexpected event count, duplicate or conflict rate,
dependency error rate, queue-age impact, reconciliation backlog, invariant violation, or any
effect outside the approved scope. Make pause and resume preserve a durable cursor. Replaying a
dead-letter item resets neither its history nor the original business identity.

If deduplication records expired before retained events, do not claim replay is safe. Restore
the needed evidence, reconstruct it from authoritative state, use a business invariant that
rejects repeats, or reduce the replay range.

If a historical replay intentionally recomputes results, give it a distinct consumer version,
output namespace, and effect policy. Do not clear the live idempotency ledger to make it run.

## Verify the design

Test the boundaries, not only the happy-path handler:

- deliver the same event ID concurrently and after each crash point;
- deliver different event IDs for the same business action;
- time out the remote call after it may have succeeded, then redeliver;
- fail acknowledgement after the local transaction commits;
- publish an outbox row twice and stop the relay between publish and marking;
- reorder events within and beyond the supported window;
- exhaust retries and confirm dead-letter metadata and ownership;
- saturate the dependency and confirm bounded concurrency and recovery;
- replay the oldest supported event before and after deduplication expiry;
- pause a replay at every stop condition and resume from its cursor.

Assert business invariants and durable records after each case. Broker delivery counts alone do
not prove the outcome. Include reconciliation for operations left in an unknown state and prove
that it converges or escalates within a stated deadline.

## Produce the reliability record

Deliver the event and business identities; delivery, ordering, retention, and acknowledgement
assumptions; crash-window table; local transaction, inbox, outbox, downstream idempotency, or
reconciliation choice; retry and dead-letter policy; backpressure limits; replay plan and stop
conditions; failure-injection cases; gaps, owners, and review date.

Read `references/gcp-delivery-semantics.md` when a design uses Pub/Sub or Eventarc Standard; it
scopes provider guarantees and retry behaviour to the documented source and destination. Read
`references/replay-safety.md` when reviewing seek, snapshot, historical recomputation, or a
dead-letter redrive; it turns retained-message behaviour into replay gates.
