---
name: deliver-webhooks
description: Builds the producer side of webhooks — you dispatch signed events to customers' HTTPS endpoints. Sign every payload with HMAC-SHA256 over "{timestamp}.{raw_body}" in a versioned signature header with per-endpoint secrets and rotation overlap; deliver at-least-once with exponential backoff + jitter over hours, then dead-letter with manual replay; send thin events (id, type, ts, minimal data) so consumers re-fetch the resource; isolate delivery per endpoint so one broken target can't stall everyone; ship a stable event id + sequence number so consumers can dedup and not assume order; verify endpoints on registration; and lock down the target URL against SSRF (HTTPS-only, block internal/link-local/metadata IPs, re-resolve on each send). Use when your service must reliably and verifiably push events out to third-party subscribers.
when_to_use: You are the SENDER pushing events to customers' webhook URLs (the Stripe/GitHub side) — building event dispatch, payload signing, the retry+DLQ schedule, endpoint registration, or a delivery-history/replay UI. Distinct from ingest-webhook-secure (the RECEIVER side — verifying inbound signatures and safely processing webhooks you consume) and message-queue-jobs (the general internal job system used here as the delivery substrate; this skill adds the webhook-specific signing, replay, SSRF, and consumer-ergonomics layer on top).
---

## When to Use

Reach for this skill when **your service emits events that third parties subscribe to** and you must deliver them verifiably and reliably:

- "Let customers register a webhook URL and we POST events to it when X happens"
- "How do we sign payloads so receivers can verify the request really came from us?"
- "One customer's endpoint is down/slow and it's backing up deliveries for everyone"
- "A delivery failed — retry it with backoff, then dead-letter, with a replay button in the dashboard"
- "Rotate a customer's signing secret without dropping any deliveries"
- "Add a delivery-history / attempts log to the customer dashboard"
- "Someone registered `http://169.254.169.254/...` as their webhook URL" (SSRF)

NOT this skill:
- *Receiving* and verifying inbound webhooks from a provider (Stripe→you) → ingest-webhook-secure (that's the mirror image: you verify their signature; here you produce yours)
- The underlying job queue / worker / DLQ plumbing (SQS/Kafka/BullMQ/Celery) → message-queue-jobs — used here as the substrate; this skill is the webhook policy on top
- The retry/backoff/jitter/circuit-breaker math for outbound calls → resilience-timeouts-retries (the primitive this skill's delivery schedule is built on)
- Per-endpoint request-rate caps / token bucket → rate-limiting (this skill references it for per-target throttling, doesn't reimplement it)
- Making the *consumer* safe to re-process a redelivered event → idempotency-keys (your job is to send a stable id + sequence so they *can*)
- Where the per-endpoint signing secret is stored/encrypted at rest → secrets-management
- Delivery metrics/traces/dashboards plumbing → observability-instrument

## Steps

1. **Sign every payload — HMAC-SHA256 over the exact bytes you send, with a per-endpoint secret.** Compute the signature over `"{timestamp}.{raw_body}"` (the same bytes on the wire — serialize ONCE, sign that buffer, send that buffer; never re-serialize between signing and sending or receivers' verification breaks). Put it in a versioned header so you can add schemes later without breaking verifiers:

   ```
   X-Webhook-Id: evt_01HZ...            # stable unique event id (also a dedup key for the consumer)
   X-Webhook-Timestamp: 1718409600      # unix seconds; part of the signed preimage
   X-Webhook-Signature: t=1718409600,v1=5257a8...   # v1 = hex HMAC-SHA256(secret, "{t}.{body}")
   ```
   ```python
   import hmac, hashlib, json
   raw = json.dumps(payload, separators=(",", ":"), sort_keys=True).encode()  # serialize ONCE
   t = str(int(time.time()))
   sigs = [f"v1={hmac.new(s, f'{t}.'.encode()+raw, hashlib.sha256).hexdigest()}"
           for s in active_secrets_for(endpoint)]   # one secret per endpoint; >1 during rotation
   headers = {"X-Webhook-Id": event_id, "X-Webhook-Timestamp": t,
              "X-Webhook-Signature": "t=" + t + "," + ",".join(sigs)}
   ```
   One secret **per endpoint** (never a global secret — a leak then compromises every customer). Document the verify recipe for receivers and point them at ingest-webhook-secure.

2. **Support secret rotation with an overlap window — send multiple signatures.** Rotation = generate a new secret, mark both old+new *active*, and sign with **both** during the overlap (`v1=<old>,v1=<new>`). The receiver accepts a request if *any* signature matches, so they can swap secrets at their leisure. After the documented overlap (e.g. 24–72 h, or when the customer confirms), retire the old secret. Without overlap, rotation drops every in-flight delivery. Store secrets via secrets-management; show "rotate" + "reveal once" in the dashboard.

3. **Include a signed timestamp + document a tolerance window so receivers can reject replays.** The `t` you sign lets a receiver drop a captured-and-replayed request that's older than their tolerance (recommend **±300 s**). You can't enforce it — but you must (a) put `t` *inside* the signed preimage (not just a loose header), (b) keep your senders' clocks NTP-synced so legit deliveries land inside the window, and (c) document the recommended tolerance so receivers implement it. Drift on your side = false replay rejections at every customer.

4. **Deliver at-least-once with exponential backoff + jitter over hours/days, then dead-letter.** Treat **any non-2xx, timeout, or connection error as retryable**; 2xx (any) = delivered, stop. Build the schedule on resilience-timeouts-retries (full jitter, per-attempt timeout ~10 s). Give up after N attempts (e.g. 8–15) spread across a long horizon, then move to a **dead-letter store** with a manual **replay** button.

   | Attempt | Delay (base, +jitter) | Cumulative |
   |---|---|---|
   | 1 | immediate | 0 |
   | 2 | ~30 s | ~30 s |
   | 3 | ~2 m | ~3 m |
   | 4 | ~10 m | ~13 m |
   | 5 | ~1 h | ~1 h |
   | 6 | ~3 h | ~4 h |
   | 7–N | ~6 h, capped | up to ~1–3 days |

   After exhaustion → DLQ row with last status/error; surface it in the dashboard with a one-click "replay" that re-enqueues the *same event* (same id + sequence) so consumer dedup still works. Auto-disable an endpoint that's failed for days and email the owner.

5. **Send a STABLE unique event id and a per-endpoint SEQUENCE number — you WILL re-deliver and you do NOT guarantee order.** The `event_id` is generated once at event creation and is identical across every retry of that event (it's the consumer's dedup key → idempotency-keys). Add a monotonic `sequence` (per endpoint or per resource) **and** the `timestamp` so consumers can detect/repair reordering. Explicitly document: *delivery is at-least-once and unordered — retries and parallel sends mean `updated` can arrive before `created`; dedup on `event_id`, order on `sequence`/`timestamp`, never on arrival order.* Don't pretend ordering you can't deliver.

6. **Send THIN events; let the consumer fetch the full resource.** Payload = `{ id, type, timestamp, sequence, data: { id, <a few key fields> } }` — enough to route and decide, not the whole object. Then the consumer GETs `/v1/orders/{id}` from your API for current truth. This avoids (a) **stale payloads** (the resource changed between enqueue and delivery), (b) **oversized bodies** that blow timeouts, and (c) **leaking** fields the subscriber shouldn't see / that bloat your audit logs. For events that are inherently terminal facts (`invoice.finalized` snapshot), a fuller payload is fine — but default thin.

7. **Version the event schema and keep it stable.** Give every event a `type` (`order.created`) and an explicit schema version (`"api_version": "2026-06-01"` on the event, or `v1` in the signature header). **Add fields, never repurpose/remove** within a version; breaking changes = a new version that customers opt into. Publish a typed catalog of event types + JSON schema. Stripe-style dated versions or a coarse `v1/v2` both work — pick one and document it.

8. **Verify the endpoint on registration before sending real traffic.** When a customer adds a URL, prove they control it and it works: send a **test/`ping` event** (or a challenge-response where they echo a token) and require a **2xx within timeout** before marking the endpoint active. This blocks typos, dead URLs, and registering *someone else's* endpoint to flood it. Re-verify on URL change. Keep the endpoint in `pending` until the test succeeds.

9. **Lock the target down against SSRF — your dispatcher is a server-side request to a customer-controlled URL.** This is the highest-severity bug in any webhook sender. On registration AND on **every send** (DNS rebinding defeats register-time-only checks):

   - **HTTPS only.** Reject `http://`, `file://`, `gopher://`, etc.
   - **Resolve the hostname yourself, then block** loopback/private/link-local/metadata ranges: `127.0.0.0/8`, `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`, `169.254.0.0/16` (incl. cloud metadata `169.254.169.254`), `::1`, `fc00::/7`, `fe80::/10`, `0.0.0.0`. Block by *resolved IP*, not by string-matching the hostname.
   - **Pin the connection to the IP you validated** (connect to the checked IP / re-resolve and re-check just before connect) so a TOCTOU re-resolution can't swap in an internal IP between check and connect.
   - **Disable redirect following** (or re-validate every hop) — a 302 to `http://169.254.169.254` bypasses a register-time check.
   - Egress from a **locked-down network** (no access to internal services / metadata endpoint) as defense in depth. Cap response body read and per-attempt timeout. See remediate-web-vulnerabilities for the SSRF class.

10. **Isolate delivery per endpoint/customer so one bad target can't stall the rest.** Run delivery on message-queue-jobs, but partition: a **per-endpoint queue/lane** with **bounded concurrency**, so a customer whose endpoint hangs/5xx's only backs up *their* lane. Add a **per-endpoint rate cap** (→ rate-limiting) to respect receivers' limits, and a **circuit breaker** (→ resilience-timeouts-retries) that fast-fails (straight to the retry schedule) while an endpoint is consistently down instead of burning worker time on it. Never deliver all customers off one shared FIFO — head-of-line blocking will take down delivery for everyone the moment one endpoint goes slow.

11. **Observability — per-attempt logs + a customer-facing delivery history and replay UI.** Log **every attempt** (not just final): event id, endpoint, attempt #, response status, latency, error, next-retry-at. Emit metrics per endpoint: **success rate, attempt count, p50/p95 latency, dead-letter count** (→ observability-instrument). Expose to the customer a **delivery history** showing each event, its attempts, response codes/bodies (truncated), and a **manual replay** button — this is what turns "your webhooks are broken" support tickets into self-service. Alert the owner when an endpoint's success rate craters or it gets auto-disabled.

## Common Errors

- **Re-serializing the body between signing and sending.** Sign a buffer, then a middleware/pretty-printer/key-reorder changes the bytes → every receiver's HMAC fails. Serialize ONCE, sign and send the *same* bytes.
- **One global signing secret for all endpoints.** A single leak compromises every customer and forces a flag-day rotation. Use one secret per endpoint.
- **Rotation with no overlap.** Swap the secret atomically → every in-flight and newly-signed delivery fails verification at the receiver. Send both old+new signatures during the overlap window, retire old after.
- **Timestamp not inside the signature (or unsynced clocks).** A loose `X-Timestamp` header an attacker can edit gives no replay protection; NTP-unsynced senders make legit deliveries fall outside receivers' tolerance. Sign `"{t}.{body}"`; keep clocks synced.
- **Treating 2xx-but-slow as success without a per-attempt timeout.** A hanging endpoint pins a worker forever. Bound each attempt (~10 s) and count a timeout as a retryable failure.
- **No dead-letter / no replay.** After N retries the event vanishes silently and the customer never knows. DLQ + a manual replay that re-sends the same event id.
- **Assuming/promising ordered delivery.** Retries + parallel lanes reorder events; consumers that apply in arrival order corrupt state. Send `sequence` + `timestamp`, document "unordered, at-least-once," and tell consumers to dedup + order on those fields.
- **Fat payloads with the full resource.** Stale by delivery time, oversized, and leak fields. Send thin + an `id`; let the consumer re-fetch.
- **SSRF: validating the URL string but not the resolved IP, or only at registration.** `http://internal.svc`, a hostname that resolves to `169.254.169.254`, or DNS-rebinding after registration all hit internal services / cloud metadata. Resolve + block private/link-local/metadata ranges on **every** send, pin to the validated IP, disable redirects.
- **Following redirects blindly.** A `302 → http://169.254.169.254/latest/meta-data/` turns a clean external URL into an SSRF. Don't follow, or re-validate each hop.
- **Shared global delivery queue.** One slow endpoint head-of-line-blocks everyone. Partition per endpoint with bounded concurrency + a breaker.
- **No endpoint verification on registration.** Typo'd/dead/hijacked URLs accepted; you send real events into the void or at a victim. Require a challenge / test event returning 2xx before activating.
- **Per-attempt logs missing.** Only logging final outcome makes "why did delivery 5 fail at 14:03" undebuggable. Log every attempt with status/latency/error and expose it to the customer.

## Verify

1. **Signature round-trips:** an independent verifier (the ingest-webhook-secure recipe) recomputes `HMAC("{t}.{body}")` over the received raw bytes and matches `v1` exactly; flipping one body byte fails verification.
2. **Per-endpoint secrets:** two endpoints get different signatures for the same event; a secret leaked from one does not verify the other.
3. **Rotation overlap:** during rotation the request carries two `v1` signatures; a receiver holding the old secret AND one holding the new secret both verify; after overlap, only the new verifies.
4. **Replay window honored:** delivered `t` is inside ±tolerance of real time (clock-sync check); a receiver rejecting `t` older than tolerance still accepts your live deliveries.
5. **Retry schedule + DLQ:** point an event at an endpoint that returns 500 → it retries with growing, jittered delays, stops after N attempts, lands in the DLQ; the replay button re-sends the **same** event id and a now-healthy endpoint accepts it once.
6. **Stable id + sequence:** every retry of one event carries the identical `event_id`; `sequence` is monotonic per endpoint; deliver two events out of order and confirm the consumer can reorder via `sequence`/`timestamp`.
7. **Thin payload:** body contains id/type/timestamp/sequence + minimal data only; the documented re-fetch returns current truth even after the resource changed post-enqueue.
8. **Endpoint isolation:** make endpoint A hang/timeout; endpoint B keeps receiving on time (assert B's delivery latency is unaffected) — proves no head-of-line blocking.
9. **SSRF blocked:** registering/sending to `http://x` (non-HTTPS), `https://127.0.0.1`, `https://169.254.169.254`, a `10.x`/`::1` address, or a hostname that resolves into a private range is rejected — at registration AND on send (test DNS-rebinding: hostname resolves public at register, private at send → still blocked); a 302 to a metadata IP is not followed.
10. **Registration verification:** a URL that never returns 2xx to the test event stays `pending`/inactive and receives no real events.
11. **Observability:** every attempt produces a log row (event id, endpoint, attempt #, status, latency); the customer dashboard lists deliveries + attempts and the replay button works.

Done = each event is HMAC-signed per-endpoint over the exact bytes with a signed timestamp and rotation overlap, delivery is at-least-once with jittered backoff → DLQ → manual replay, events are thin and carry a stable id + sequence so consumers dedup and reorder, the target URL is HTTPS-only and SSRF-blocked (private/link-local/metadata ranges, re-checked on every send), endpoints are verified before activation, delivery is isolated per endpoint, and every attempt is logged and visible to the customer with a working replay — all proven by checks 1–11.
