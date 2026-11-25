---
name: idempotent-payments
description: >-
  Use when code creates, captures, refunds, transfers or pays out money, or calls a payment
  processor, bank or wallet API. Covers caller-chosen idempotency keys with request fingerprints
  and stored responses, unique indexes that make the first writer win, the unknown-outcome problem
  after a timeout, persist-before-call with a pending-intent reconciler, a guarded payment state
  machine, bounded retries on retryable errors only, and the transactional outbox for events.
  Triggers on a double charge, a duplicate refund, a retry loop, a timeout handler, a new endpoint
  that moves money. Not for the processor's own fraud or risk rules.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Idempotent payments

Networks time out, clients retry, queues redeliver and people double-click. A payment system
that is not idempotent charges twice and refunds twice, and discovers it from a customer.
Idempotency is not a header; it is a property of every money-moving path, inbound and outbound.

## When to use

- A new or changed endpoint, job or consumer that creates a charge, capture, refund, transfer,
  payout or ledger entry.
- Any call to a processor, bank, wallet or card network API.
- A bug report about a duplicate charge, a duplicate refund, a stuck "pending" payment or a
  retry storm.
- A timeout or error handler around a money call.

## Rules

1. **The caller chooses the key; the server stores the fingerprint and the response.** Each
   money-moving request carries an idempotency key. The server stores `(tenant, operation, key,
   request_fingerprint, response, status)` before doing the work. Same key and same fingerprint
   returns the stored response. Same key with a different fingerprint is an error (HTTP 422 or
   409), never a second execution.
2. **Scope the key.** Keys are unique per tenant and per operation. A key used for a capture
   cannot be reused for a refund. Keep keys at least 24 hours; for refunds and payouts keep them
   much longer, because retries come from humans days later. Processors prune their keys too
   (Stripe after 24 hours): a same-key retry after that window executes again. Bound automatic
   retries by the shorter of your window and the processor's; past it, an unknown-outcome
   operation is not resubmitted but reconciled (query the processor by your reference or
   metadata), and only then re-issued as a new operation with a new key, recorded as such.
3. **The first writer wins, in the database.** A unique index on `(tenant, operation, key)` and
   an `INSERT ... ON CONFLICT DO NOTHING` (or an equivalent) decide who executes. The loser reads
   the winner's row and returns its response, or `409 in progress` if the winner has not
   finished.
4. **Outbound calls carry a deterministic key too.** Derive the processor idempotency key
   (for example Stripe's `Idempotency-Key` header) from your internal operation id, never from
   a fresh random value per attempt. A retry after a timeout must present the same key.
5. **A timeout is an unknown outcome, not a failure.** After a timeout on a money call, never
   issue a new request with a new key. Either retry with the same key while the processor still
   holds it (rule 2), or query the processor by your reference, or leave the intent pending for
   the reconciler. Only a confirmed failure
   from the processor makes the intent failed.
6. **Persist before you call.** Write the intent as `pending` in your database, then call the
   processor, then record the outcome. A crash between steps leaves a `pending` row that a
   reconciler resolves by querying the processor. Alert on `pending` older than the SLA.
7. **The payment is a state machine with guards.** `created -> authorized -> captured ->
   settled`, with `voided`, `failed`, `refunded` and `partially_refunded` as explicit states.
   A transition checks the current state inside the same transaction that writes it. A second
   capture is rejected with the current state, not silently ignored.
8. **Exactly-once delivery does not exist; build idempotent consumers.** Events go out through
   a transactional outbox in the same transaction as the state change. Consumers dedupe by
   event id. Producers may redeliver; nothing breaks.
9. **Retries are bounded and selective.** Retry only network errors, HTTP 5xx and 429 (honor
   `Retry-After`), with exponential backoff and jitter, a maximum attempt count and a maximum
   total time. Never retry validation errors (4xx) or declines.
10. **Every attempt is observable.** Log the key, the operation, the attempt number, the
    processor reference and the outcome. Dashboards show duplicate-key hits, pending age and
    retry counts per operation.

## How to apply

1. List every path that moves money, inbound (API, job, consumer) and outbound (processor
   calls). Grep for the processor client and for `retry`, `timeout`, `except`.
2. Add the idempotency table or columns and the unique index. Write the middleware or helper
   that implements rules 1 to 3 once; every endpoint uses it.
3. Wrap the processor client so every call takes an internal operation id and derives the
   outbound key from it (rule 4). Make the wrapper the only way to call the processor.
4. Add the `pending` intent write before the call and the reconciler job after it (rule 6).
5. Write the tests in the **Tests** section. Use a fake processor that can time out, fail and
   succeed on command.
6. Add the retry policy as a named object with its limits; test that validation errors do not
   retry.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent (for example the order stays pending and the
confirmation path marks it paid). An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Same key, same payload, twice: one charge at the processor, identical responses.
- Same key, different amount: error, no second charge.
- Two concurrent requests with the same key: one charge, both get the same response.
- Processor times out, client retries with the same key: one charge.
- Processor times out and the client disappears: the intent stays `pending`; the reconciler
  resolves it from the processor's answer.
- Capture on an already captured payment: rejected with the current state.
- A 400 from the processor is not retried; a 503 is retried with backoff up to the limit.
- An event is emitted exactly once per state change through the outbox; a redelivered event is
  a no-op for the consumer.
- Reference vectors: `skills/idempotent-payments/evals/vectors/test_idempotency.py` with
  `IDEMPOTENCY_SOLUTION` pointing at your module (store, state machine, timeout, retries).
  TypeScript: `idempotency.test.ts` with `IDEMPOTENCY_SOLUTION_TS`.

## Review checklist

- Where is the unique index, and which code path inserts first?
- What happens on a timeout? Point to the line.
- Can any code call the processor without the wrapper?
- Which states exist, and where are the transition guards?
- What is the retry policy's maximum attempts and total time, and which errors qualify?
- How old can a `pending` intent get before someone is paged?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Random idempotency key per attempt | Retries double charge | Key derived from the operation id |
| Treating a timeout as a failure | Charge succeeded, record says failed, retry charges again | Unknown outcome; same key or query |
| Dedupe in memory or cache only | Lost on restart, not shared across instances | Unique index in the database |
| Check state, then update in two statements | Race between two workers | Guarded update in one statement or a row lock |
| Retry everything with no cap | Retry storm, rate limits, duplicate work | Named policy with limits and error classes |
| Publish the event after commit, outside the transaction | Event lost on crash | Transactional outbox |

## References

- Stripe documentation on idempotent requests: keys, 24-hour retention, same-key-different-parameters errors.
- The transactional outbox pattern (Chris Richardson, microservices.io).
- Two-phase and pending transfers in TigerBeetle documentation, as a model for intent then outcome.
