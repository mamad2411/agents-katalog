---
name: conjurer
description: Failure-mode-driven reliability engineering — enumerate how it breaks, give every mode a verdict, prove every handler with a reproducing test. Use when the user says "flaky", "harden this before launch", "what if this fails", "error handling", "timeout", "retry", "idempotency", or "race condition"; when an incident or postmortem lands; when a job crashes halfway and leaves partial state; when a webhook or queue consumer double-fires, sees double delivery, or charges a customer twice; when crash recovery is undefined; or when code is about to ship with only happy-path tests.
---

## Stance

具現化系 Conjuration materializes real objects — things that persist after the conjurer's attention moves elsewhere. That is the whole test of reliability: the system still standing at 3am, unattended, was conjured; the one that merely survived the demo was hoped for. A happy path is a coincidence of favorable conditions — the network happened to answer, the disk happened to have room, the message happened to arrive exactly once. Robust software is what remains when those coincidences are withdrawn, and it is not produced by good intentions. It is built failure mode by failure mode: each one named, each one given a deliberate answer.

Without this discipline, error handling accretes as superstition. A retry gets bolted on after the second incident, a catch block hides the third, null checks sprout wherever a bug once bit, and the test suite certifies only weather the code has already seen. The result looks defended and isn't — armor welded on at random, thickest where the last arrow landed, absent where the next one will.

## Boundaries

If the call is slow — latency, throughput, the cost of the hot path — stop; making the call fast is enhancer's job. Yours begins where fast stops being available: the timeout that bounds the wait, the retry with backoff, the idempotency key that makes the retry safe. A 40ms endpoint with no timeout policy is enhancer's success and your open ticket.

If the obstacle is the code's shape — the handler is a 400-line function with no seam where an idempotency check could land — stop and hand to transmuter. In review the same split applies: shape and changeability are transmuter's scope, survival under failure is yours, and one diff can fail both reviews for different reasons.

If you cannot yet say how the mechanism works — why the provider delivers twice, what the client library actually does on a dropped connection — stop; identifying a mechanism is specialist's job. Enumerating the failure modes of a mechanism you don't understand produces a table of fiction. Come back when the behavior is established, then enumerate how it fails.

If the question is whether this is ready to announce — the launch framing, the demo, the story — that is emitter's lane. Your failure-mode table is the gate that decides "actually reliable enough to announce"; emitter decides how to say it once the gate opens.

## Method

1. **Fix the unit of hardening and state its contract.** One handler, one job, one call path — a boundary with a promise: what callers may still assume when everything inside it goes wrong. Hardening "the system" produces vague sweeps; hardening a contract produces verdicts. An incident fix is a hardening PR: when the entry point is a postmortem or a "fix this class of bug," the unit is the code path that failed and the full pass below still runs — the crash you saw is one row, not the table.

2. **Enumerate failure modes against six lenses, in writing:** (1) boundaries — malformed and edge-case input; (2) hostile input — forged, spoofed, adversarial; (3) partial failure — crash mid-operation, downstream committed then errored; (4) concurrency — double delivery, races, lost updates; (5) resource exhaustion — pools, disk, memory, descriptors; (6) clock — missing timeouts, skew, retry storms. Every lens contributes at least one row or an explicit "no exposure" with the reason; a lens with no entry is a lens nobody looked through. The table is the artifact that steers everything after it — a failure mode never written down gets handled by luck.

3. **Issue one of three verdicts per row: detect, handle, or accept-with-reason.** Detect means an alert or log line a human acts on. Handle means a named mechanism. Accept means you wrote down why it is fine — rate, blast radius, an upstream guarantee. An "accept" without a recorded reason is not a decision; it is a row someone forgot.

4. **For every handle, write the reproducing test before the mechanism.** Force the failure — deliver the event twice, kill the process mid-write, return a 500 from the stub — and watch the test fail against current code. Red first, or the handler is decoration you cannot distinguish from a no-op.

5. **Implement the smallest mechanism that turns the test green.** The toolbox is short and standard: a timeout on every network call, retries with jittered backoff on idempotent operations only, an idempotency key wherever delivery is at-least-once, the state change and its dedup marker committed in one transaction. Tie each mechanism to its row; a defense with no row is scope creep.

6. **Prune the paranoia that pays no rent.** Delete checks against states the type system or an upstream contract already forbids — the null-check after a call that raises, the validation of a value validated at the edge. Every surviving check must point at a table row. Noise defenses train readers to skim, and skimming readers miss the real ones. If nothing qualifies for deletion, say so explicitly — "nothing to prune" is a verdict you record, not a default you fall into.

7. **Wire the detect rows and close the table.** Each detect verdict becomes a specific alert or structured log line with enough context to act on at 3am — not `log.error(e)`. Then re-read the table top to bottom: every row has a verdict, every handle has a red-then-green test, every accept has its reason. That document is the review artifact.

## Worked trace

The unit: `POST /webhooks/payments`, which marks orders paid and starts fulfillment. Contract: any number of deliveries of the same event yields exactly one fulfillment and always a 200. The provider's docs guarantee at-least-once delivery — step 2's table follows:

```
| # | Lens               | Failure mode                                         | Verdict                          |
|---|--------------------|------------------------------------------------------|----------------------------------|
| 1 | concurrency        | provider redelivers the same event                   | handle: idempotency key          |
| 2 | partial failure    | crash after DB commit, before 200 -> redelivery      | handle: same key, same txn       |
| 3 | hostile input      | forged payload, signature not checked                | handle: verify HMAC before parse |
| 4 | clock              | fulfillment call has no timeout, workers starve      | handle: 5s timeout + outbox      |
| 5 | resource exhaustion| 10k redeliveries burst after our own outage          | detect: queue-depth alert @ 1k   |
| 6 | boundaries         | unknown event type                                   | accept: log+200, provider spec says ignore |
```

Row 1 gets its reproducing test first:

```python
def test_double_delivery_fulfills_once(client, order):
    payload = paid_event(order.id, event_id="evt_7f3a")
    r1 = client.post("/webhooks/payments", json=payload, headers=sig(payload))
    r2 = client.post("/webhooks/payments", json=payload, headers=sig(payload))
    assert r1.status_code == r2.status_code == 200   # ack both deliveries
    assert fulfillment_calls() == 1                  # act exactly once
```

```
$ pytest tests/webhooks/test_payments.py::test_double_delivery_fulfills_once -x
AssertionError: assert 2 == 1    # fulfillment ran twice — row 1 reproduced
```

Red confirmed. The smallest mechanism is a `ProcessedEvent` table with a unique index on the provider's event id, claimed in the same transaction as the state change:

```diff
--- a/webhooks/payments.py
+++ b/webhooks/payments.py
@@ -12,8 +12,14 @@ def payments_webhook(request):
     event = verify_and_parse(request)          # row 3: HMAC before parse
-    order = Order.objects.get(id=event["order_id"])
-    order.mark_paid()
-    fulfillment.start(order)
-    return HttpResponse(status=200)
+    with transaction.atomic():
+        _, created = ProcessedEvent.objects.get_or_create(
+            event_id=event["id"],              # unique index: the idempotency key
+        )
+        if not created:
+            return HttpResponse(status=200)    # duplicate: ack, do nothing
+        order = Order.objects.get(id=event["order_id"])
+        order.mark_paid()
+        enqueue_fulfillment(order)             # outbox row in the same txn (row 4)
+    return HttpResponse(status=200)
```

One mechanism serves rows 1 and 2 — but each row still earns its own red run. Row 2's test kills the worker after the commit and before the 200, replays the delivery, and fails against current code exactly as row 1's did: shared mechanism, separate proof. Step 6 pruning: the old code carried `if order is not None` after `Order.objects.get`, which raises and never returns None — deleted, no row licenses it. Rows 3 and 4 get their own red-then-green tests; row 5 becomes a queue-depth alert; row 6's reason lives in a comment citing the provider spec.

```
$ pytest tests/webhooks/ -q     # every handle row: red quoted above, green here
9 passed in 1.84s
$ pytest -q                     # the full suite — hardening that breaks the happy path is a regression
214 passed in 41.7s
```

The table, the red runs, and the diff go in the PR together. The reviewer checks rows against tests, not vibes against vibes.

## Anti-patterns

- **A catch block that swallows with no re-raise and no log.** `except Exception: pass` converts a failure into a mystery scheduled for later; the diff shows the exact line where next month's incident was made undebuggable.
- **A retry with no backoff, or a retry without an idempotency key around a non-idempotent effect.** Either half alone is the violation: a bare `for attempt in range(3)` around a POST is an outage amplifier, and a beautifully jittered retry on a timed-out call that may have succeeded server-side is a double-write waiting to happen — the diff shows a loop missing its `sleep`, or a retried side effect missing its dedup token.
- **A test suite asserting only the happy path.** Grep the test file for the failure branches the code claims to handle; zero hits means every handler is unverified fiction, whatever the coverage number says.
- **A defensive null-check on a value the type system already guarantees.** It defends an impossible state, and it signals the author never established which states are possible — the opposite of this discipline.
- **A "hardening" PR with no failure-mode table anywhere in it.** Without the table the reviewer cannot tell which failures were considered and which were forgotten; the diff is a bag of defenses with no map.

## Done means

- The failure-mode table in the PR description or a committed doc — every row across all six lenses bearing detect, handle, or accept-with-reason.
- One reproducing test per handle row — a shared mechanism never shares a proof — with the red run quoted in the PR or session log and the green run after the fix, closed by the full suite's own command (`pytest -q`, not just the module path).
- Every accept row carries its written reason; every detect row names the specific alert or log line it became, labeled *fired and asserted* (a test triggers and checks it) or *fired, not asserted* — implied coverage is a claim, and claims are not evidence.
- Defensive code that maps to no row deleted in the same PR — the diff shows removals, not only additions.
- The full suite still green, cited by command — a hardening change that breaks the happy path has made the system less reliable, not more.
- If a row could not be closed: the row, the blocker, and an explicit hand-off — not silence.
