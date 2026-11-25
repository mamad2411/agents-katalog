---
name: leaddocket-webhooks
description: >
  Configure and understand outbound Webhooks in LeadDocket — the event
  notifications LeadDocket sends to external URLs when lead, contact, or
  opportunity events occur. Use when setting up integrations that need to
  react to LeadDocket events in real time (new lead, status change, new
  opportunity, etc.).
---

# LeadDocket — Webhooks

LeadDocket can send outbound webhook notifications to external systems when events occur. This is a **push-based integration** — LeadDocket calls your endpoint, unlike the pull-based REST API.

> Support section: [Webhooks](https://support.leaddocket.com/hc/en-us/sections/360009496931-Webhooks)

---

## Configuration (in the LeadDocket UI)

1. Navigate to **Settings → Webhooks**
2. Click **Add Webhook**
3. Enter your endpoint URL (must be HTTPS)
4. Select the events to subscribe to
5. Optionally configure a secret for payload verification
6. Save and test with the built-in test button

---

## Common Webhook Events

| Event | Trigger |
|-------|---------|
| `lead.created` | A new lead is created |
| `lead.updated` | A lead's data is modified |
| `lead.status_changed` | A lead moves to a new status |
| `opportunity.created` | A new opportunity is received |
| `opportunity.converted` | An opportunity is converted to a lead |
| `contact.created` | A new contact is added |
| `contact.updated` | A contact record is modified |

---

## Receiving Webhooks

### Endpoint requirements

- Must be publicly accessible HTTPS
- Must respond with HTTP `200` within **10 seconds**
- Non-200 responses or timeouts cause retries

### Payload format

LeadDocket sends a `POST` request with `Content-Type: application/json`. The payload shape varies by event type but typically includes:

```json
{
  "EventType": "lead.status_changed",
  "Timestamp": "2026-07-01T14:22:00Z",
  "LeadId": 1234,
  "Data": {
    "NewStatusId": 5,
    "NewStatusName": "Active Client",
    "PreviousStatusId": 2
  }
}
```

### Verifying webhook authenticity

If a shared secret is configured, LeadDocket includes an HMAC signature header. Verify the payload:

```js
const crypto = require('crypto');

function verifySignature(payload, signature, secret) {
  const hmac = crypto.createHmac('sha256', secret);
  hmac.update(payload);
  const computed = hmac.digest('hex');
  return computed === signature;
}

// In your webhook handler:
app.post('/webhook', (req, res) => {
  const sig = req.headers['x-leaddocket-signature'];
  const rawBody = req.rawBody; // raw string before JSON parsing
  if (!verifySignature(rawBody, sig, process.env.WEBHOOK_SECRET)) {
    return res.status(401).send('Invalid signature');
  }
  // Process event...
  res.sendStatus(200);
});
```

---

## Retry Behavior

- LeadDocket retries failed deliveries with exponential backoff
- Retries stop after a configurable number of attempts
- Failed webhooks may be visible in the admin webhook log

---

## Best Practices

- **Respond fast, process async**: Return `200` immediately, then process the webhook payload in a background queue (Redis, SQS, etc.) to avoid timeouts.
- **Idempotency**: Design your handler to be safe if the same event is delivered more than once. Use the event's unique ID or `LeadId + Timestamp` as a deduplication key.
- **HTTPS only**: LeadDocket won't deliver to non-HTTPS URLs.
- **Use the test button**: Always test with LeadDocket's built-in webhook tester before going live.
- **Compare with polling**: For high-frequency data sync, webhooks are more efficient than `lastupdatedsince` polling. Use both: webhooks for real-time updates, polling as a reconciliation safety net.
