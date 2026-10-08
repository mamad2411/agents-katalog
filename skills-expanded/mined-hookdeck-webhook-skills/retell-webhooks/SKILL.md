---
name: retell-webhooks
description: >
  Receive and verify Retell AI webhooks. Use when setting up Retell webhook
  handlers, debugging X-Retell-Signature verification, or handling voice call
  events like call_started, call_ended, call_analyzed, and transcript_updated.
license: MIT
metadata:
  author: hookdeck
  version: "0.1.0"
  repository: https://github.com/hookdeck/webhook-skills
---

# Retell AI Webhooks

## When to Use This Skill

- How do I receive Retell AI webhooks?
- How do I verify Retell webhook signatures (`X-Retell-Signature`)?
- How do I handle `call_ended` or `call_analyzed` events?
- Why is my Retell webhook signature verification failing?
- How do I handle transcript, transfer, and chat events from Retell?

## Verification (core)

Retell signs each webhook with **HMAC-SHA256** using your **Retell API key** as
the secret (only an API key with the webhook badge in the dashboard works). The
signature arrives in the `X-Retell-Signature` header formatted as
`v={unix_ms_timestamp},d={hex_digest}`, where the digest is computed over the
**raw request body concatenated with the timestamp**. Always verify against the
**raw body**, never a re-serialized JSON string.

The **Python SDK** ships a verify helper (`client.verify(body, api_key, signature)` —
positional params, so the keyword form used in the FastAPI example also works).
The **Node SDK has no verify helper**, so Node handlers verify manually.

> Verified against `retell-sdk` **5.56.0 (PyPI)** and **5.46.0 (npm)**: the Python
> package exposes `retell.lib.webhook_auth.verify`, re-exported as `client.verify`;
> the npm package has no webhook/verify export. Check your installed version — the
> helper's presence and argument order have moved between releases.

```javascript
const crypto = require('crypto');

// Reject signatures older than 5 minutes to prevent replay attacks
const FIVE_MINUTES_MS = 5 * 60 * 1000;

function verifyRetellSignature(rawBody, signatureHeader, apiKey) {
  const match = /^v=(\d+),d=(.*)$/.exec(signatureHeader || '');
  if (!match) return false;
  const [, timestamp, digest] = match;
  if (Math.abs(Date.now() - Number(timestamp)) > FIVE_MINUTES_MS) return false;

  const expected = crypto
    .createHmac('sha256', apiKey)
    .update(rawBody + timestamp) // raw body + timestamp, in that order
    .digest('hex');
  try {
    return crypto.timingSafeEqual(Buffer.from(expected), Buffer.from(digest));
  } catch {
    return false; // length mismatch = invalid
  }
}
```

Python (FastAPI) uses the official SDK instead:

```python
from retell import Retell

client = Retell(api_key=os.environ["RETELL_API_KEY"])
# client.verify enforces the ~5 min timestamp window and returns a bool
is_valid = client.verify(raw_body.decode("utf-8"),
                         api_key=os.environ["RETELL_API_KEY"],
                         signature=signature_header)
```

> **For complete handlers with tests**, see [examples/express/](examples/express/), [examples/nextjs/](examples/nextjs/), [examples/fastapi/](examples/fastapi/).

## Common Event Types

| Event | Triggered When | Common Use Cases |
|-------|----------------|------------------|
| `call_started` | A call begins | Track live calls, update dashboards |
| `call_ended` | A call finishes (audio done) | Persist call record, trigger follow-ups |
| `call_analyzed` | Post-call analysis completes | Store transcript, sentiment, summary |
| `transcript_updated` | Transcript changes mid-call | Live captions, real-time monitoring |
| `transfer_started` | An agent transfer begins | Log routing, notify agents |
| `transfer_bridged` | Transfer connected | Update call state |
| `transfer_cancelled` | Transfer cancelled | Revert routing state |
| `transfer_ended` | Transfer completed | Reconcile call legs |
| `chat_started` | A chat session begins | Track chat sessions |
| `chat_ended` | A chat session ends | Persist chat record |
| `chat_analyzed` | Post-chat analysis completes | Store chat summary, sentiment |

Payloads carry an `event` field plus a `call` object (voice/transfer events) or a
`chat` object (chat events). Dedupe on `event` + `call.call_id` (or `chat.chat_id`) —
Retell retries up to 3 times if it doesn't get a 2xx within 10 seconds.

See [references/overview.md](references/overview.md) for full payload structure.

## Environment Variables

```bash
# The Retell API key (must have the webhook badge). Used as the HMAC secret.
RETELL_API_KEY=key_xxxxxxxxxxxxxxxxxxxxxxxx
PORT=3000
```

## Local Development

For local webhook testing, run the Hookdeck CLI via `npx` — no install required:

```bash
npx hookdeck-cli listen 3000 retell --path /webhooks/retell
```

No account required — the CLI creates a guest account on first run and provides a
local tunnel + web UI for inspecting requests.

## Resources

- [Overview](references/overview.md) - What Retell webhooks are, event types, payloads
- [Setup](references/setup.md) - Configure account-level and agent-level webhooks
- [Verification](references/verification.md) - Signature verification details and gotchas
- [Express Example](examples/express/) - Complete Express.js implementation
- [Next.js Example](examples/nextjs/) - Next.js App Router implementation
- [FastAPI Example](examples/fastapi/) - Python FastAPI implementation (uses the Retell SDK)

## Recommended: webhook-handler-patterns

We recommend installing the [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) skill alongside this one for handler sequence, idempotency, error handling, and retry logic. Key references (open on GitHub):

- [Handler sequence](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/handler-sequence.md) — Verify first, parse second, handle idempotently third
- [Idempotency](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/idempotency.md) — Dedupe Retell retries on `event` + `call_id`
- [Error handling](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/error-handling.md) — Return codes, logging, dead letter queues
- [Retry logic](https://github.com/hookdeck/webhook-skills/blob/main/skills/webhook-handler-patterns/references/retry-logic.md) — Provider retry schedules, backoff patterns

## Related Skills

- [elevenlabs-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/elevenlabs-webhooks) - ElevenLabs voice AI webhook handling
- [deepgram-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/deepgram-webhooks) - Deepgram transcription callback handling
- [openai-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/openai-webhooks) - OpenAI webhook handling
- [twilio-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/twilio-webhooks) - Twilio voice and messaging webhook handling
- [stripe-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/stripe-webhooks) - Stripe payment webhook handling
- [github-webhooks](https://github.com/hookdeck/webhook-skills/tree/main/skills/github-webhooks) - GitHub repository webhook handling
- [webhook-handler-patterns](https://github.com/hookdeck/webhook-skills/tree/main/skills/webhook-handler-patterns) - Handler sequence, idempotency, error handling, retry logic
- [hookdeck-event-gateway](https://github.com/hookdeck/webhook-skills/tree/main/skills/hookdeck-event-gateway) - Webhook infrastructure that replaces your queue — guaranteed delivery, automatic retries, replay, rate limiting, and observability for your webhook handlers
