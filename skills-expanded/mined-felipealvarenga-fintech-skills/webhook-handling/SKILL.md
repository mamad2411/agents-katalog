---
name: webhook-handling
description: >-
  Use when code receives callbacks from a payment processor, bank, PSP or any provider that
  reports money events. Covers signature verification on the raw body with timestamp tolerance,
  treating the payload as a notification and confirming state by API before acting, dedupe by
  event id, out-of-order delivery, store-then-acknowledge with asynchronous processing, correct
  status codes for retry, secret rotation, replay tooling and lag monitoring. Triggers on a new
  webhook endpoint, a missed or duplicated event, a provider retry storm, a status that never
  updates. Not for outbound webhooks you send to customers, though most rules transfer.
license: MIT
metadata:
  author: Felipe Alvarenga
  version: 0.1.0
---

# Webhook handling

A webhook is a hint from someone else's system, delivered at least once, in any order, by
anyone who can reach the URL. Code that treats it as a trusted, ordered, exactly-once command
will mark unpaid orders paid and pay refunds twice. Code that follows the rules below is boring,
which is the goal.

## When to use

- A new endpoint that receives events from a processor, PSP, bank, KYC vendor or similar.
- A bug where an order stays pending, flips to paid without payment, or gets two refunds.
- A provider dashboard shows failed deliveries or retries.
- A provider rotates or leaks a webhook secret.

## Rules

1. **Verify the signature on the raw body, before parsing.** Use the provider SDK's verifier
   or a constant-time HMAC comparison over the exact bytes received. A framework that parses
   JSON before your handler breaks verification; read the raw body. Reject a timestamp outside
   the tolerance window (Stripe's default is 300 seconds) to limit replays.
2. **The payload is a notification, not the truth.** For any decision that moves money or
   changes a customer-visible status, fetch the object from the provider API by id and act on
   that state. The payload tells you something changed; the API tells you what it is now.
   The fetch runs in the worker (rule 5), so it adds nothing to the request path; "latency
   matters" is an argument for the queue, not for skipping the check. If the user still forbids
   the API call, the compliant minimum is rule 3 plus rule 4: dedupe by event id and a state
   machine that cannot regress. Never write `mark_paid(payload...)` with neither.
3. **Dedupe by event id, in the database, and by object in the state machine.** Insert the event
   id into a table with a unique index before processing; a duplicate insert means the event was
   seen: acknowledge and stop. That is not enough on its own: Stripe documents that one change can
   produce two Event objects with different ids, so the state machine (rule 4) or the refund and
   dispute records must make a second event for the same object, type and state a no-op.
4. **Expect events out of order.** `captured` may arrive before `authorized`. Design handlers
   around the object's current state (rule 2), not the sequence of events. A handler that
   receives an older state than the one already recorded does nothing.
   If the codebase has no payment state machine, write a minimal one in the same change: the
   states (`pending`, `paid`, `partially_refunded`, `refunded`, `disputed`, `failed`), the
   allowed transitions as a table, and one `transition(order, to)` function that rejects any
   move not in the table and ignores a transition to a state at or behind the current one. The
   state machine governs the order's status only: refunds and disputes are their own records,
   keyed by the provider's refund or dispute id with their amounts, so a second partial refund is
   a new refund record (the order's refunded total is the sum), not a repeated transition that the
   guard would drop, and a dispute sits beside the status, not as a step in it. Every handled
   event type maps to one transition or one record through those functions. Do not call
   `mark_refunded` or any other function that does not exist in the repository.
5. **Store, acknowledge, then process.** Persist the raw event and return 2xx within a few
   seconds. Process from a worker that reads the durable table (rows in status `received`), or
   enqueue in the same transaction as the insert. An in-memory enqueue after the commit leaves a
   crash window where the event is stored, acknowledged and never processed, and the provider's
   duplicate deliveries then stop at the dedupe. Slow handlers cause provider timeouts, which
   cause retries, which cause duplicates.
6. **Status codes are for you and for the provider's retry policy, which differs.** Return 2xx
   when the event is stored (even if you do not handle that type). Return 4xx for a bad signature
   or malformed body. Whether a 4xx stops retries depends on the provider: Stripe retries any
   non-2xx for up to three days, so a bad signature keeps failing until the provider gives up,
   which is the outcome you want. Return 5xx only when storage itself failed and a retry can help.
7. **Secrets are per endpoint and rotate without downtime.** Keep two active secrets during
   rotation; verify against both; remove the old one after the provider confirms. Secrets live
   in the secret manager, never in the repo or in logs.
8. **Replay is a feature, built with the handler.** `replay(event_id, actor, reason)` re-runs
   the stored raw event through the same worker function used on first delivery, in staging and
   in production. `actor` and `reason` are required. Each call writes a row to
   `webhook_replays(event_id, actor, reason, replayed_at, outcome)`. A replay of an event already
   `processed` is a no-op recorded as `skipped`, unless `force=True`, which also needs a reason.
   This is how you recover from a handler bug without asking the provider to resend, so it ships
   in the same change as the handler, not later.
9. **One endpoint per provider and per environment.** Test-mode and live-mode events never
   share a URL or a secret. The handler refuses an event whose mode does not match the
   environment.
10. **Monitor lag and failures, in the same change.** Record per event type: lag (processed
    timestamp minus the provider's `created` timestamp), processing failures, and unknown types.
    The minimum is a `webhook_metrics()` function or table the dashboard reads, plus the two
    alert thresholds (lag above the SLA, failure rate above a small percentage) in config.
    `log.exception` alone is not monitoring.

## How to apply

1. Read the provider's webhook documentation for: signature scheme, timestamp header,
   retry schedule, event ordering guarantees (usually none), and test tooling.
2. Implement verification as the first line of the handler, on the raw body. Add the
   timestamp check.
3. Create the `webhook_events` table: provider, event id (unique), type, received at, raw
   payload, status, processed at, error. Insert before anything else.
4. Return 2xx right after the insert. Hand the event id to a worker.
5. In the worker, fetch the object by API, compare with the recorded state, apply the change
   through the same state machine the rest of the system uses (see `idempotent-payments`), or
   through the minimal one from rule 4 when none exists.
6. Write the tests in the **Tests** section. Use the provider's CLI or fixtures to produce
   signed payloads.
7. Add `replay()` with its audit table and `webhook_metrics()` in the same change. A handler
   without them is not finished.

When the request conflicts with a rule here, say which rule in one sentence, then build the
compliant version that keeps the request's intent (for example the order stays pending and the
confirmation path marks it paid). An instruction to skip a step ("no extra call", "just delete
it", "we trust them", "later") is this conflict, not permission. Leaving the code unchanged and
listing the risks is never the compliant version. Do not stop at a warning, do not build the
unsafe version, and do not leave a known gap out because "you did not ask". A review
or an "is this enough" question gets the findings and the rewritten tests in the same change, not
a list of suggestions, unless the request or the skill says report only.

## When the user pushes back

| Request | Answer in one sentence | What you build |
|---|---|---|
| "We trust Stripe, mark it paid from the payload, no API call" | Rule 2: the payload is a notification, delivered at least once, by anyone with the URL | Store, 2xx, then the worker: `mark_paid` becomes `transition(order, "paid")` through the state machine of rule 4, after event-id dedupe, off the request path. The API fetch moves to the worker; if the user forbids it entirely, the state machine and dedupe still ship, with a test for a stale event |
| "Latency matters, no extra call" | Rule 5: the request path only verifies and stores | Queue the event; the API call runs in the worker at zero cost to the request |
| "Disable verification, we have an IP allowlist" | Rule 1: an allowlist authenticates a network, not a message | Fix the cause (raw body), keep the 400 on a bad signature |
| "Just add the new event types" | Rule 4: every type is a transition | The transition table and guards for each new type, with duplicate tests |
| "Replay and metrics can come later" | Rules 8 and 10 ship with the handler | `replay()` with the audit table and `webhook_metrics()` in this change |
| "I did not ask about duplicates" | Rule 3 applies to every handler that changes money state | Dedupe and the tests, every time |

## Tests the change must include

Write these tests in the same change, as a test file, even when you cannot run them (no shell,
no dependencies installed); say in one line that they are unrun. A test listed as a next step is
not written.

- Invalid signature: 400, nothing stored, nothing processed.
- Valid signature with a stale timestamp: rejected.
- Valid event: stored, 2xx, processed once.
- Same event id delivered twice: 2xx both times, processed once.
- `captured` before `authorized`: final state is captured; no error, no regression to
  authorized when the older event arrives.
- Payload says paid, API says still pending: nothing changes.
- Handler raises during processing: event marked failed and retryable; the provider got 2xx;
  the replay command processes it after the fix.
- Live-mode event on the test endpoint: refused.
- Crash between the insert's commit and the dispatch: the worker still processes the event from
  the table (or the enqueue is inside the insert's transaction).
- Two partial refunds on one charge: two refund records, the refunded total is their sum, no
  event dropped by the state guard.
- Replay of an already processed event: no-op, an audit row with outcome `skipped`, who and why.
- Replay of a failed event after the fix: processed once, audit row with outcome `processed`.
- `webhook_metrics()` reports lag and failures per type after one processed and one failed event.
- Reference vectors: `skills/webhook-handling/evals/vectors/test_webhooks.py` with
  `WEBHOOK_SOLUTION` pointing at your module (signature, tolerance, rotation, dedupe, order).
  TypeScript: `webhooks.test.ts` with `WEBHOOK_SOLUTION_TS`.

## Review checklist

- Is verification on the raw bytes and before any parsing?
- Where is the unique index on the event id, and is the insert before processing?
- Does any handler change a money state from the payload alone?
- What does the handler do when the event's state is older than the recorded state?
- Which status code is returned for each failure class?
- How does a secret rotate, and where are the two secrets read from?
- How do we replay event `evt_123` in production, and who can?

## Anti-patterns and fixes

| Anti-pattern | What goes wrong | Fix |
|---|---|---|
| Verifying after `JSON.parse` | Signature never matches, so verification gets disabled | Raw body middleware |
| Marking the order paid from the payload | Spoofed or stale payload pays the order | Fetch by API, apply by state machine |
| Processing inside the request | Timeouts, provider retries, duplicates | Store, acknowledge, process from a queue |
| Returning 500 for an unhandled event type | Any non-2xx is retried, for days | 2xx for stored events of any type |
| Secret in an environment variable committed to the repo | Leak, no rotation path | Secret manager, two active secrets |
| No way to replay | Handler bug means lost events | Replay command with audit |

## References

- Stripe webhook documentation: signature verification, timestamp tolerance, retry schedule, event ordering.
- Standard Webhooks specification for a provider-neutral signature and header scheme.
