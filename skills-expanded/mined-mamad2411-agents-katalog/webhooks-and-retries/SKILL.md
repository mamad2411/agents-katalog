---
name: webhooks-and-retries
description: Implement signed, idempotent webhooks and retry-safe external side effects.
version: 2.1.0
tier: core
stack: [any]
owner: integration
gates: [G2, G3]
related: [integration-contracts, observability]
---

# Skill: webhooks-and-retries

## Purpose
Make inbound webhook processing and outbound side effects reliably correct under retries,
duplicate deliveries, provider errors, and network failures. The two properties that make
this possible — *authenticity* (the payload is really from the claimed sender) and
*idempotency* (processing the same payload twice has the same effect as processing it once)
— must both be enforced at the handler boundary, not assumed at the business logic layer.

## When to use
Any inbound webhook endpoint (Stripe, GitHub, Slack, provider-of-your-choice), any outbound
operation that must not execute more than once (charge, send email, publish event, trigger
deployment), or any retry loop wrapping an external call that has side effects. Also applies
to internal queue/message-bus consumers where the broker may redeliver messages.

## Procedure

1. **Verify webhook authenticity before touching the payload.** Compute the expected HMAC
   signature from the raw request body (not a parsed copy) and the shared secret, then
   compare it with the provider-supplied signature header using a constant-time comparison
   function (e.g., `hmac.compare_digest` in Python, `crypto.timingSafeEqual` in Node.js).
   Reject with 401 if the comparison fails. Also validate the timestamp header if the
   provider includes one (typically reject events older than 5 minutes to prevent replay).
   Signature verification must happen before any deserialization or business logic.
2. **Return 2xx immediately after verification; process asynchronously.** The webhook
   handler's only synchronous job is: verify the signature, enqueue the validated payload
   (or write it to a processing table), and return 200/202. Do not run business logic
   synchronously in the handler — if processing fails or is slow, the provider will retry
   and the handler will block. Decouple receipt from processing.
3. **Design the idempotency key strategy.** Determine the key that uniquely identifies a
   logical operation. For webhook events, the provider's event ID (e.g., Stripe's `evt_xxx`,
   GitHub's `X-GitHub-Delivery` header) is the natural idempotency key. For outbound calls,
   derive the key deterministically from the business operation (e.g., `charge:{order_id}`)
   — never use `uuid()` or `random()` as an idempotency key, because a new random value
   on each retry defeats the purpose.
4. **Implement deduplication with an idempotency store.** Before executing a side effect,
   check whether the idempotency key has already been processed (lookup in a database table,
   Redis set, or the provider's idempotency endpoint). If already processed, return the
   cached result without re-executing. After successful execution, record the key with the
   result and a TTL appropriate to the provider's retry window (typically 24–72 hours).
   Use a database transaction or atomic operation to prevent TOCTOU races where two concurrent
   retries both see "not processed" and both execute.
5. **Define a bounded retry policy with backoff and jitter.** For outbound retries:
   - Retry only on transient errors (5xx, network timeout, 429 with `Retry-After`). Never
     retry 4xx errors (bad request, unauthorized) — they won't succeed on retry.
   - Use exponential backoff: start at 1s, double each attempt, cap at 30–60s.
   - Add jitter (±25% of the backoff interval) to prevent retry storms when many callers
     fail simultaneously.
   - Set a maximum attempt count (typically 3–5 for most operations). After exhausting
     attempts, transition the item to the dead-letter state; do not retry indefinitely.
6. **Implement dead-letter handling.** A message or event that cannot be processed after
   the maximum retry count must go somewhere visible: a dead-letter queue, a database table
   with status `failed`, or an alerting system. Define the recovery path: can operations
   team replay the dead-letter item manually? What information is needed to replay it safely?
   An infinite retry loop with no dead-letter path will eventually exhaust resources or
   produce unbounded lag.
7. **Expose observability for delivery health.** Emit metrics (or structured logs) for:
   events received, events processed successfully, events retried, and events dead-lettered.
   Create an alert when the dead-letter count exceeds a threshold or when processing lag
   spikes. Without these signals, a broken webhook handler is invisible until a user reports
   a missing outcome.

## Checklist
- [ ] Signature verified using constant-time comparison before any payload access
- [ ] Timestamp validated to reject replayed events beyond the acceptable window
- [ ] Handler returns 2xx immediately; business logic runs asynchronously
- [ ] Idempotency key is deterministic (not random); derived from provider event ID or
      business operation ID
- [ ] Deduplication uses an atomic check-and-record to prevent TOCTOU races
- [ ] Retry policy covers: which errors are retried, backoff+jitter formula, and max attempts
- [ ] Dead-letter path exists with a defined recovery procedure
- [ ] Metrics/alerts exist for event lag, retry rate, and dead-letter accumulation

## Anti-patterns
- Verifying the signature *after* parsing or acting on the payload — a tampered payload
  can affect the application before the signature check catches it.
- Using `==` or `===` for HMAC comparison — this leaks timing information and allows
  an attacker to forge signatures one byte at a time.
- Generating a new random UUID as the idempotency key on each retry — this registers a
  new operation with the provider on each attempt, causing duplicate charges/sends.
- Infinite retries with no dead-letter path — a poison message (one that always fails)
  will retry forever, blocking the queue and masking all subsequent events.
- Processing the webhook payload synchronously in the HTTP handler — a slow processing
  step will eventually time out and the provider will requeue and retry.

## Output
Webhook handler with synchronous signature verification and async processing, idempotency
store with atomic deduplication, bounded retry policy with dead-letter handling, and
observability metrics/alerts for delivery health. Test evidence covers: forged signature
→ 401, duplicate event → idempotent no-op, transient 503 → retry succeeds, exhausted
retries → dead-letter.
