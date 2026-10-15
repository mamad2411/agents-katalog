---
name: engagelab-otp-webhook
description: Receives, verifies, and processes EngageLab OTP webhook callbacks for message delivery events, channel fallbacks, user uplink replies, account notifications, and system audit events. Use when implementing a webhook endpoint to track message delivery status, react to delivery failures, monitor account balance, or process inbound user replies. Handles HMAC-SHA256 signature verification automatically.
license: MIT
metadata:
  author: engagelab
  version: "1.0"
  docs: https://www.engagelab.com/zh_CN/docs/otp/REST-API/Callback-Configuration
---

# EngageLab OTP — Webhook callbacks

EngageLab POSTs delivery status, account events, and inbound replies to your webhook endpoint. This skill handles signature verification and event parsing.

## Firewall whitelist (required)

Allow incoming HTTPS from these IPs:

```
119.8.170.74
114.119.180.30
```

## Signature verification (the most important thing)

Each callback has an `X-CALLBACK-ID` header with format:

```
timestamp=1701234567;nonce=abc123;username=your-user;signature=<hmac>
```

where `signature = HMAC_SHA256(secret, f"{timestamp}{nonce}{username}").hexdigest()`.

**The SDK does this for you. Always verify before trusting the body.**

## Node.js (Express)

```js
const express = require('express');
const { WebhookVerifier, MessageStatusEvent } = require('engagelab-otp');

const app = express();
app.use(express.json());

const verifier = new WebhookVerifier({
  username: process.env.ENGAGELAB_WEBHOOK_USERNAME,
  secret:   process.env.ENGAGELAB_WEBHOOK_SECRET,
});

app.post('/webhook/engagelab', verifier.middleware(async (events) => {
  for (const e of events) {
    if (e.kind !== 'message_status') continue;

    // CRITICAL: do NOT prompt the user to retry while still mid-flight.
    // Channel fallback in progress emits non-terminal events.
    if (!e.is_terminal) continue;

    if (e.status === 'delivered')        await markDelivered(e.message_id);
    else if (e.status === 'verified')    await markVerified(e.message_id);
    else                                  await handleFailure(e);
  }
}));
```

## Python (Flask)

```python
from flask import Flask
from engagelab_otp import WebhookVerifier, MessageStatusEvent

app = Flask(__name__)
verifier = WebhookVerifier(
    username=os.environ["ENGAGELAB_WEBHOOK_USERNAME"],
    secret=os.environ["ENGAGELAB_WEBHOOK_SECRET"],
)

def handle(events):
    for e in events:
        if not isinstance(e, MessageStatusEvent):
            continue
        if not e.is_terminal:
            continue   # mid-flight, wait
        if e.status == "delivered":
            mark_delivered(e.message_id)
        elif e.status == "verified":
            mark_verified(e.message_id)

app.add_url_rule(
    "/webhook/engagelab",
    "engagelab_webhook",
    verifier.flask_view(handle),
    methods=["POST"],
)
```

## Manual verification (any framework)

```js
const { WebhookVerifier, WebhookSignatureError } = require('engagelab-otp');
const verifier = new WebhookVerifier({ username, secret });

try {
  verifier.verify(req.headers['x-callback-id']);
  const events = verifier.parseEvents(req.body);
  // process events
  res.status(200).end();
} catch (err) {
  if (err instanceof WebhookSignatureError) {
    res.status(401).end();
  } else {
    // log; always return 200 to EngageLab to prevent retry storms
    res.status(200).end();
  }
}
```

## Event types — what to handle

`parseEvents()` returns one of four kinds. See [references/EVENTS.md](references/EVENTS.md) for full schema.

| `kind`           | When                                | Typical action |
|------------------|-------------------------------------|----------------|
| `message_status` | per-message lifecycle               | track delivery state |
| `notification`   | account-level alert                 | page ops team |
| `uplink`         | inbound user reply (e.g. "STOP")    | handle unsubscribe |
| `system_event`   | console audit                       | usually just log |

## Message status enum

```
plan · target_valid · target_invalid    ← validation events
sent · sent_failed                      ← submission events
delivered · delivered_failed            ← delivery events
verified · verified_failed · verified_timeout    ← verification events
```

`is_terminal === true` for: `delivered`, `delivered_failed`, `sent_failed`, `verified*`, `target_invalid`.

## The fallback trap (READ THIS)

EngageLab sends multiple callbacks per message during channel fallback. Without checking `is_terminal`, your Agent will react to the wrong event:

```
T+0s   sent on whatsapp           is_terminal=false   ← do nothing
T+8s   delivered_failed on wa     is_terminal=false   ← do nothing (fallback coming)
T+10s  sent on sms                is_terminal=false   ← do nothing
T+15s  delivered on sms           is_terminal=TRUE    ← act here
```

If you act on the first `delivered_failed` (no `is_terminal` check), you'll tell the user "send failed" while the system is mid-fallback. The user re-sends, gets two SMS, types the wrong code.

**Always check `is_terminal` before acting on a status event.**

## Always respond 200 quickly

```
EngageLab retries failed webhooks with exponential backoff:
  1 min, 10 min, 1 hour, 2 hours, 5 hours, 10 hours, 1 day, 1 day...
  Up to 24 retries.

→ Process events async. Respond 200 within 5 seconds.
→ If your handler throws, you'll get re-delivered a lot.
```

## Sandbox webhook testing

Sandbox sends webhook events with signed signatures using:

```
ENGAGELAB_WEBHOOK_USERNAME=sandbox_demo
ENGAGELAB_WEBHOOK_SECRET=sandbox_webhook_secret
```

To test locally, use `ngrok` to expose a tunnel:

```bash
ngrok http 3000
# In sandbox dashboard, set webhook URL to https://abc123.ngrok.io/webhook/engagelab
```

Or use the sandbox playground at https://playground.engagelab.com/sandbox/webhook to send canned events to your endpoint.

## When NOT to use this skill

- For sending OTPs → use `engagelab-otp-send` skill
- For verifying user input → use `engagelab-otp-verify` skill
- For account-level webhook configuration (only) → see EngageLab console
