---
name: twilio-reliability-patterns
version: 1.0.0
description: Build resilient Twilio integrations with idempotency, backoff, error-code handling, Messaging Services, and status reconciliation.
author: matrixx0070
tags: [twilio, reliability, retries, idempotency, messaging-services, error-codes]
capabilities: []
---

## When to use

Use this when outbound messages or calls must survive rate limits, transient 5xx, and network faults without duplicating or losing sends. Use it when you need to interpret Twilio error codes, pick between direct-number and Messaging Service sends, or reconcile "did it actually deliver?" from status callbacks. Use it when designing graceful degradation for an integration that must not fall over under load.

**Not for:** inbound webhook/TwiML design and signature validation — use twilio-webhook-architecture. Post-incident log/alert forensics — use twilio-debugging-observability. Email sending/deliverability — use twilio-email-send and twilio-email-deliverability-advisor.

## Method

1. Assign an idempotency key per logical send. Twilio's create-message API is not natively idempotent, so store your own key → resulting `MessageSid` mapping and short-circuit retries that already succeeded. Decision point: only retry a create if you have no recorded SID for that key.
2. Classify failures before retrying. Retry on 429 (too many requests), 500/503, and network timeouts; do NOT retry on 4xx validation errors like 21211 (invalid `To`) or 20003 (authentication) — those will fail identically forever.
3. Apply exponential backoff with jitter: e.g. base 500ms, factor 2, cap ~30s, plus random jitter; honor any `Retry-After` header on 429. Bound total attempts (3–5) then dead-letter.
4. Prefer a Messaging Service for scale. It gives you a sender pool, sticky sender, geo-matching, and built-in rate/throughput smoothing and queueing, so bursts are absorbed rather than rejected. Send with `MessagingServiceSid` instead of `From`.
5. Configure fallback. On a Messaging Service, set a fallback URL / secondary sender strategy; for critical flows, fall back across channels (SMS → voice, or SMS → email) when delivery status is `failed`/`undelivered`.
6. Reconcile delivery from status callbacks, not the create response. A 201 from create only means "queued". Treat `delivered` as success and `undelivered`/`failed` (with `ErrorCode` 30xxx) as terminal failure to trigger fallback.
7. Queue and shape load. Buffer sends in your own queue and drain at or below your account/number throughput (e.g. ~1 msg/s per long code, higher for toll-free/short code/Messaging Service) to avoid 429 storms.
8. Select region/edge for latency and residency: set `region`/`edge` on the client (e.g. `au1`, `ie1`) close to your infrastructure and to meet data-residency needs.
9. Degrade gracefully. On sustained upstream failure, stop hammering the API (circuit breaker), surface a user-visible "delayed" state, and replay from the dead-letter queue once healthy.

## Example

```javascript
import twilio from 'twilio';
const client = twilio(process.env.TWILIO_API_KEY, process.env.TWILIO_API_SECRET, {
  accountSid: process.env.TWILIO_ACCOUNT_SID,
  region: 'us1', edge: 'ashburn',
});

const RETRYABLE = new Set([429, 500, 503]);
const sent = new Map(); // idempotencyKey -> MessageSid (persist this for real)

async function sendResilient(key, to, body, attempt = 0) {
  if (sent.has(key)) return sent.get(key);           // idempotent short-circuit
  try {
    const msg = await client.messages.create({
      messagingServiceSid: process.env.TWILIO_MG_SID, // pool + queueing + fallback
      to, body,
      statusCallback: 'https://app.example.com/status',
    });
    sent.set(key, msg.sid);
    return msg.sid;                                    // status is "queued", not delivered
  } catch (err) {
    const retryable = RETRYABLE.has(err.status);
    if (!retryable || attempt >= 4) throw err;         // 21211/20003 -> never retry
    const wait = Math.min(30000, 500 * 2 ** attempt) + Math.random() * 250;
    await new Promise(r => setTimeout(r, wait));
    return sendResilient(key, to, body, attempt + 1);
  }
}
```

## Pitfalls

- **Retrying non-retryable errors.** 21211 (invalid number), 21610 (recipient opted out via STOP), 20003 (auth) never recover on retry — you just burn quota and duplicate. Branch on error class first.
- **Treating create-201 as delivered.** Create returns `queued`. Carrier rejection surfaces later via status callback with a 30xxx `ErrorCode`. Wire callbacks or you will report false success.
- **No idempotency key.** A timeout after Twilio accepted the request, followed by a blind retry, double-sends. Map your key to the returned SID and check before resending.
- **Ignoring Retry-After on 429.** Fixed-interval retries against a throttle prolong the throttle. Honor `Retry-After` and add jitter to avoid thundering-herd.
- **Per-number throughput limits.** A long code sends ~1 msg/s; blasting a list from one long code triggers 429s and carrier filtering. Use a Messaging Service or toll-free/short code and queue.
- **Opt-out (21610) not handled.** Sending to a STOP'd recipient errors permanently and risks compliance violations. Persist opt-out state locally.

## Output format

```
SEND: key=<idempotency-key> channel=<sms|voice> target=<E164>
ATTEMPTS: <n>  backoff=<ms values>  retry-after-honored=<yes|no>
RESULT: sid=<MessageSid> create-status=<queued|failed>
DELIVERY: <delivered|undelivered|failed>  errorCode=<20003|21211|30xxx|none>
FALLBACK: <none | secondary-sender | cross-channel:<..>>
ACTION: <success | dead-letter | opt-out-suppress | circuit-open>
```

## Reference

- **Error codes:** 20003 authentication failure; 20429 too many requests; 21211 invalid `To` number; 21606/21408 `From` not permitted/geo not enabled; 21610 recipient unsubscribed (STOP); 21612 not reachable via this route; 30001–30008 message delivery failures (30003 unreachable handset, 30005 unknown destination, 30006 landline/unreachable carrier, 30007 carrier filtered/spam, 30008 unknown error). Full list at twilio.com/docs/api/errors.
- **HTTP semantics:** 429 = rate limited (respect `Retry-After`); 5xx = retryable server error; 4xx (except 429) = do not retry.
- **Messaging Service (`MG...`):** sender pool, sticky sender, geographic-permissions, area-code/number-pool selection, sender-ID sticky, scheduled sends, and throughput smoothing/queueing. Send with `messagingServiceSid` rather than `from`.
- **Status reconciliation:** message status `queued → sending → sent → delivered | undelivered | failed`; `undelivered`/`failed` carry an `ErrorCode`.
- **Auth:** use API Keys (`SK...` + secret) so credentials are revocable independently of the Auth Token.
- **Regions/edges:** `region` (us1, ie1, au1, …) + `edge` (ashburn, dublin, sydney, …) tune latency and data residency.
- **Compliance:** TCPA requires prior express consent; A2P 10DLC registration is required for US long-code application traffic or carriers filter it (error 30007).
