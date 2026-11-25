---
name: twilio-sendgrid-webhooks
version: 1.0.0
description: Consume the SendGrid Event Webhook — configure it, verify the ECDSA signature, handle each event type idempotently, and turn delivery/engagement events into reliable state.
author: matrixx0070
tags: [sendgrid, event-webhook, signed-webhook, ecdsa, delivery-events, engagement-events, idempotency]
capabilities: []
---

## When to use

Use this when you need to know what actually happened to mail after the API accepted it — delivered, bounced, opened, clicked, spam-reported, unsubscribed — by receiving and processing the SendGrid Event Webhook.

**Not for:** receiving replies or inbound mail (see `twilio-sendgrid-inbound-parse`) or interpreting the aggregate engagement picture (see `twilio-sendgrid-engagement-quality`).

## Method

1. Expose an HTTPS endpoint that accepts `POST` with a JSON array of event objects. SendGrid batches many events per request.
2. Enable the Event Webhook in Mail Settings / the Event Webhook config, select event categories, and point it at your URL. Enable Signed Event Webhook to get a public verification key.
3. Verify every request before trusting it. SendGrid signs with ECDSA: read `X-Twilio-Email-Event-Webhook-Signature` and `X-Twilio-Email-Event-Webhook-Timestamp`, concatenate `timestamp + raw_body`, and verify against your stored public key. Reject on mismatch.
4. Process idempotently. Each event has `sg_event_id` (unique) and `sg_message_id` (ties to the send). De-duplicate on `sg_event_id`; you will get retries and occasional duplicates.
5. Map event types to state: `processed`, `delivered`, `deferred`, `bounce`, `dropped`, `blocked`, `open`, `click`, `spamreport`, `unsubscribe`, `group_unsubscribe`, `group_resubscribe`. Bounce/dropped/spamreport should update your own suppression/reputation state.
6. Respond fast with `2xx`, then process async. Slow endpoints cause SendGrid to retry and eventually disable the webhook.
7. Preserve `category` and `custom_args` from events to attribute outcomes back to your records.

## Example

Verify the signature (Node, using the raw request body):

```js
const { EventWebhook } = require('@sendgrid/eventwebhook');
const ew = new EventWebhook();
const key = ew.convertPublicKeyToECDSA(process.env.SG_WEBHOOK_PUBKEY);

app.post('/sg/events', express.raw({ type: '*/*' }), (req, res) => {
  const sig = req.get('X-Twilio-Email-Event-Webhook-Signature');
  const ts  = req.get('X-Twilio-Email-Event-Webhook-Timestamp');
  if (!ew.verifySignature(key, req.body, sig, ts)) return res.sendStatus(403);
  const events = JSON.parse(req.body.toString());
  res.sendStatus(200);            // ack first
  for (const e of events) enqueue(e.sg_event_id, e);  // dedupe + async
});
```

## Pitfalls

- **Verifying against a parsed body.** ECDSA verification needs the exact raw bytes. If a JSON middleware reparses/reserializes first, verification fails. Capture the raw body.
- **No idempotency.** Retries and duplicates double-count opens or re-suppress addresses. De-dupe on `sg_event_id`.
- **Slow synchronous handlers.** Doing DB work before responding leads to timeouts, retries, and auto-disable. Ack `2xx`, then process.
- **Trusting unsigned events.** An open endpoint can be spoofed to forge unsubscribes/bounces. Always verify the signature.
- **Ignoring `deferred` vs `bounce`.** Deferred is temporary (retrying); bounce is terminal. Only suppress on hard bounce/dropped/spamreport.

## Output format

```
# Event Webhook: <endpoint>
CONFIG: url=<https...> events=[delivered,bounce,open,click,spamreport,unsubscribe]
SIGNED: yes  pubkey=<vault ref>
VERIFY: raw-body + timestamp -> ECDSA check -> 403 on fail
IDEMPOTENCY: dedupe key = sg_event_id
STATE MAP: bounce/dropped/spamreport -> suppress; open/click -> engagement
ACK: 2xx immediate, async processing
```

## Reference

- Event Webhook: JSON array `POST` to your URL; configured via Event Webhook settings (`/v3/user/webhooks/event/settings`).
- Signature headers: `X-Twilio-Email-Event-Webhook-Signature`, `X-Twilio-Email-Event-Webhook-Timestamp`; signed payload = `timestamp + raw_body`, verified with the ECDSA public key from settings. SDK helper: `@sendgrid/eventwebhook`.
- Event fields: `event`, `email`, `timestamp`, `sg_event_id`, `sg_message_id`, `category`, plus `reason`/`status`/`url` depending on type.
- Deliverability: bounce, dropped, and spamreport events are the ground truth that should feed your suppression lists and reputation monitoring.
