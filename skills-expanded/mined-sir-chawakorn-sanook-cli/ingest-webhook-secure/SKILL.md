---
name: ingest-webhook-secure
description: Builds secure inbound webhook receivers that verify HMAC/asymmetric signatures over the raw body, reject replays via signed-timestamp windows and seen-id stores, dedup idempotently on provider event id, and fast-ack within timeout before processing async. Use when receiving callbacks from an external service that must be authentic, non-replayed, and handled exactly once.
when_to_use: When standing up or debugging an inbound webhook/callback endpoint that must reject spoofed, replayed, or duplicate events and survive retry storms. Distinct from auth-jwt-session (verifies your own users' identity, not a provider's request signature), message-queue-jobs (the async worker you hand off to), and rate-limiting (caps request rate, not authenticity).
---

## When to Use

Reach for this skill when an **external service POSTs to you** and you must trust, deduplicate, and reliably process those events:

- "Stripe/GitHub/Slack/Twilio/Shopify webhook — verify the signature before acting"
- "We're getting duplicate webhook deliveries / charged twice / sent the email twice"
- "Provider says our endpoint timed out and they're hammering us with retries"
- "Someone is POSTing fake events to our `/webhooks` URL"
- "Signature verification fails intermittently" (almost always raw-body mangling)
- Designing one intake endpoint for several providers with different header/encoding quirks

NOT this skill:
- Verifying *your own* logged-in user (session/JWT/cookie) → auth-jwt-session
- The background worker/queue that does the slow processing → message-queue-jobs
- Capping how many requests a caller may send → rate-limiting
- Where the signing secret is stored/rotated at rest → secrets-management
- Metrics/traces/dashboards for the endpoint → observability-instrument

## Steps

1. **Verify BEFORE parsing — over the RAW bytes, not re-serialized JSON.** Capture the exact body as received (`bytes`/`Buffer`) and sign *that*. Any JSON round-trip (`json.loads`→`json.dumps`, framework body-parser, pretty-printer, key reorder, trailing-newline strip) changes the bytes and breaks HMAC. Disable the framework's auto JSON parse for this route and read the raw stream first.

   | Provider style | Signature scheme | What is signed |
   |---|---|---|
   | Stripe | HMAC-SHA256, header `Stripe-Signature: t=…,v1=…` | `"{t}.{rawbody}"` |
   | GitHub | HMAC-SHA256, header `X-Hub-Signature-256: sha256=…` | raw body |
   | Slack | HMAC-SHA256, header `X-Slack-Signature: v0=…` | `"v0:{ts}:{rawbody}"` |
   | Shopify | HMAC-SHA256, **base64**, header `X-Shopify-Hmac-Sha256` | raw body |
   | Svix/Standard Webhooks | HMAC-SHA256 base64, `webhook-signature` | `"{id}.{ts}.{rawbody}"` |
   | GitHub App / Apple / some payment rails | **asymmetric** Ed25519 or RSA-SHA256, public key | raw body (you hold only the public key) |

2. **Constant-time compare, support multiple/rotating secrets.** Never `==` on signatures — that leaks timing. Compute the digest and use a constant-time check. Iterate over *all* currently-valid secrets so rotation has zero-downtime overlap (old + new accepted during the window).

   ```python
   import hmac, hashlib, time
   # header_sig MUST already be the parsed hex digest, NOT the raw header:
   #   GitHub "sha256=<hex>" -> strip "sha256="; Stripe "t=..,v1=<hex>" -> the v1 value.
   def verify(raw: bytes, header_sig: str, ts: str, secrets: list[bytes], tol=300) -> bool:
       try:                                          # malformed/missing ts -> reject, never 500
           skew = abs(time.time() - int(ts))
       except (TypeError, ValueError):
           return False
       if skew > tol:                                # replay window FIRST (cheap reject)
           return False
       signed = f"{ts}.".encode() + raw              # STRIPE-SHAPED ("{ts}.{rawbody}"); swap per Step 1:
                                                     #   GitHub -> signed = raw
                                                     #   Slack  -> signed = b"v0:" + ts.encode() + b":" + raw
                                                     #   Svix   -> signed = id.encode() + b"." + ts.encode() + b"." + raw
       for secret in secrets:                        # accept any active secret (rotation overlap)
           expected = hmac.new(secret, signed, hashlib.sha256).hexdigest()
           if hmac.compare_digest(expected, header_sig):
               return True
       return False
   ```
   For asymmetric schemes, swap the body for `nacl.signing.VerifyKey(pub).verify(...)` (Ed25519) or `cryptography` `public_key.verify(...)` (RSA-PSS/PKCS1v15) — you never hold a shared secret. For base64 providers (Shopify, Svix) compare base64 digests, not hex.

3. **Reject replays — two layers.** (a) Tolerance window on the **signed** timestamp (default **±300 s**); a captured-but-stale request fails the window even with a valid signature. (b) Store the provider event id with a TTL ≥ the window and reject a second sighting. The timestamp must be the one *inside the signature*, not a client header you didn't authenticate.

4. **Idempotency — dedup on the provider's event id, atomically.** Use `SETNX webhook:{provider}:{event_id} 1 EX 86400` (or a UNIQUE column + `INSERT … ON CONFLICT DO NOTHING`). First writer proceeds; a `0`/conflict means already-seen → return `200` immediately (acknowledge, do nothing). TTL/retention ≥ the provider's max retry horizon (Stripe ~3 days, others up to weeks — check the table in step 7).

5. **Respond 2xx fast, then process async — never do slow work inline.** The handler's only inline job: verify → persist the verified raw event → enqueue → return `200`. Hand the actual processing (DB writes, emails, downstream calls) to a worker/queue (→ message-queue-jobs). Most providers retry on >~5–10 s; slow inline work causes a retry storm that multiplies load. Return `200`/`202` within ~2 s.

   | Outcome | Status | Why |
   |---|---|---|
   | Verified + enqueued (or duplicate) | `200`/`202` | Ack; stops retries |
   | Bad/missing signature, failed asymmetric verify | `401` | Not authentic — do **not** 200 |
   | Replay outside window / malformed timestamp | `400` | Authentic-looking but stale/garbage |
   | Body too large / not the expected content-type | `413` / `415` | Reject before reading fully |
   | Your DB/queue down (verified but can't persist) | `500`/`503` | Let the provider retry — do NOT 200 and drop |

6. **Handle out-of-order delivery by resource version, not arrival order.** Retries and parallel deliveries mean `updated` can land before `created`. Reconcile on a monotonic field the provider gives (`sequence`, resource `version`, `updated_at`, Stripe object `created`): apply an event only if its version > the version you've stored; otherwise drop it as stale. When in doubt, treat the webhook as a *signal to re-fetch* the resource from the provider's API and use that as truth.

7. **Lock down the surface + ship a safe replay tool.** Cap body size (`413` past e.g. 1 MB) before reading the whole stream. Reject unsigned/missing-header requests with `401` — never fall through to processing. Optionally pin source IPs to the provider's published CIDR allowlist (defense in depth, not a substitute for the signature). Some providers require a one-time **handshake/challenge** (Slack `url_verification` echo, Stripe/Meta GET with a `hub.challenge`, EventSub `webhook_callback_verification`) — answer it verbatim or you'll never receive events. Store the verified raw payload so you can re-drive processing later; the replay tool must re-run the *worker*, never re-accept an unverified HTTP request.

   | Provider | Signature header | Encoding | Handshake | Notes |
   |---|---|---|---|---|
   | Stripe | `Stripe-Signature` | hex, `t=`/`v1=` | none | tolerance 300 s; secret per-endpoint (`whsec_…`) |
   | GitHub | `X-Hub-Signature-256` | hex | ping event | also legacy SHA-1 header — ignore it, use 256 |
   | Slack | `X-Slack-Signature` + `X-Slack-Request-Timestamp` | hex, `v0=` | `url_verification` echo | reject ts older than 5 min |
   | Shopify | `X-Shopify-Hmac-Sha256` | **base64** | none | sign raw body, compare base64 not hex |
   | Twilio | `X-Twilio-Signature` | base64 over **URL + sorted POST params** | none | not raw-body — concat full URL + params |
   | Svix/Standard Webhooks | `webhook-id`/`webhook-timestamp`/`webhook-signature` | base64, `v1,` | none | id+ts+body signed; multiple space-sep sigs |

## Common Errors

- **Signing re-serialized JSON instead of raw bytes.** The #1 "works in Postman, fails in prod" bug. Read and sign the exact received bytes; never let a body-parser touch the route before verification.
- **Plain `==` / string compare on signatures.** Timing oracle. Use `hmac.compare_digest` / `crypto.timingSafeEqual` (and length-check first since it throws on mismatched length).
- **Comparing against the raw header instead of the parsed digest.** `X-Hub-Signature-256` is `sha256=<hex>`; `Stripe-Signature` is `t=…,v1=<hex>`. Extract the digest field first, then constant-time compare — comparing the whole header always fails.
- **Reconstructing the signed string wrong (right secret, still rejects).** Each provider signs a different preimage (raw body vs `"{ts}.{body}"` vs `"v0:{ts}:{body}"`). Build it byte-for-byte from the Step 1 table; a generic `"{ts}.{body}"` silently works only for Stripe-shaped schemes.
- **Crashing on a malformed/missing timestamp.** `int(ts)` on a non-numeric or absent header throws → `500` (provider retries forever). Catch and treat a bad timestamp as a hard reject (`400`/`401`), not an exception.
- **Parsing the JSON before verifying.** Hands attacker-controlled bytes to your parser and downstream logic pre-trust. Verify first, parse second.
- **Trusting an unsigned timestamp/IP header for replay defense.** Use the timestamp *inside the signed payload*; anyone can set a raw header. IP allowlists are spoofable behind misconfigured proxies — keep them as defense in depth only.
- **No idempotency, or dedup that isn't atomic.** "Check then insert" in two steps lets two concurrent retries both pass → double processing. Use `SETNX`/`INSERT … ON CONFLICT` as one atomic op on the event id.
- **Doing the work inline, returning 200 after.** Causes timeouts → provider retries → storm. Persist + enqueue + 200 fast; process in a worker.
- **Returning 200 when persistence/enqueue failed.** Swallows the event forever — the provider thinks it's delivered and stops retrying. On internal failure return `5xx` so the retry redelivers.
- **Applying events in arrival order.** Out-of-order retries overwrite newer state with older. Gate on resource version/sequence, or re-fetch the resource.
- **One global secret, no rotation path.** Rotating means downtime or dropped events. Accept a *list* of active secrets; remove the old one after the overlap window.
- **Ignoring the handshake/challenge.** Endpoint silently never activates; you debug "missing events" that were never sent. Implement the provider's verification echo.
- **No body-size cap.** A multi-GB POST OOMs the process before you ever check the signature. Enforce a max length and `413` early.

## Verify

1. **Happy path:** Replay a captured real delivery with its original headers and raw body → `200`, event persisted once, worker ran exactly once.
2. **Tampered body:** Flip one byte of the body, keep the signature → `401`, nothing persisted, worker never invoked.
3. **Tampered/forged signature:** Random or empty signature header → `401`. Missing header entirely → `401` (not a 500, not a 200).
4. **Raw-body integrity:** Send a payload whose `json.dumps` re-serialization differs from the bytes (extra whitespace, reordered keys) → still `200`. Proves you verify the raw bytes, not a re-encode.
5. **Replay window:** Valid signature with a timestamp older than tolerance (e.g. ts−600 s) → `400`/`401`; same request within tolerance → `200`.
6. **Duplicate delivery:** POST the identical valid event twice (and concurrently, in parallel) → both return `200` but the worker side-effect happens **exactly once**. This catches non-atomic dedup.
7. **Out-of-order:** Deliver `version=2` then `version=1` for the same resource → final stored state reflects v2; the v1 arrival is dropped/ignored.
8. **Fast-ack:** Make downstream processing sleep; the HTTP response still returns 2xx within the provider timeout (assert response latency, not just status).
9. **Persistence failure:** Force the store/queue to fail on a verified event → endpoint returns `5xx` (so the provider retries), not `200`.
10. **Oversized / wrong type:** POST > size cap → `413`; wrong `Content-Type` → `415`; both reject before full read.

Done = a tampered or unsigned request gets `401`, a stale one `400`, a duplicate (including concurrent) is accepted but processed exactly once, a valid one is acked 2xx within timeout and processed via the worker, and raw-body verification survives a JSON re-serialization that would have broken a naïve implementation.
