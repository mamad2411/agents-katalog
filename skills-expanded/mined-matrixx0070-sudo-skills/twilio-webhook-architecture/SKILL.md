---
name: twilio-webhook-architecture
version: 1.0.0
description: Design incoming Twilio webhooks and status callbacks with TwiML responses, signature validation, and idempotency.
author: matrixx0070
tags: [twilio, webhooks, twiml, status-callbacks, security, signature]
capabilities: []
---

## When to use

Use this when you need to receive inbound SMS or voice from Twilio, respond with TwiML, or consume message/call status callbacks. Use it when you are standing up a public HTTPS endpoint that Twilio will POST to and you must validate that the request genuinely came from Twilio. Use it when duplicate deliveries or retries are corrupting your state and you need idempotency.

**Not for:** outbound reliability, backoff, and error-code handling — use twilio-reliability-patterns. Runtime log/alert forensics — use twilio-debugging-observability. Email webhooks (inbound parse / event webhook) — use twilio-email-deliverability-advisor.

## Method

1. Expose a public HTTPS endpoint. Twilio only calls publicly reachable URLs; for local dev tunnel with ngrok (`ngrok http 3000`) and set the resulting HTTPS URL on the number.
2. Decide the content type. Twilio sends `application/x-www-form-urlencoded` by default (params like `From`, `To`, `Body`, `MessageSid`, `CallSid`). Parse the form body before reading params.
3. Validate `X-Twilio-Signature` on every request. Compute HMAC-SHA1 with your Auth Token over the full request URL (including query string) concatenated with each POST param name+value sorted alphabetically by key, then base64-encode. Reject on mismatch with HTTP 403. Decision point: if behind a proxy/load balancer that rewrites the host or scheme, reconstruct the exact original public URL Twilio called, or validation will fail.
4. Respond fast with a 200 and valid TwiML for inbound messages/calls. Return `Content-Type: text/xml`. Do heavy work asynchronously (enqueue a job) rather than blocking the webhook. Twilio times out after ~15 seconds.
5. For inbound SMS return `<Response><Message>...</Message></Response>`; for voice return `<Response><Say>/<Dial>/<Gather>...</Response>`. Return an empty `<Response/>` to accept without replying.
6. Configure status callbacks on outbound messages/calls via `StatusCallback`. Message statuses progress `queued → sending → sent → delivered` (or `failed`/`undelivered`); call statuses `queued → ringing → in-progress → completed` (or `busy`/`no-answer`/`failed`/`canceled`).
7. Make callback handlers idempotent. Key on `MessageSid`/`CallSid` + `MessageStatus`; status callbacks can arrive out of order or more than once. Decision point: only advance state forward — never downgrade `delivered` back to `sent`.
8. Return 2xx quickly from callback handlers too. Non-2xx or timeouts cause Twilio to retry, amplifying duplicates.
9. Log the inbound SID and validation result for correlation (see twilio-debugging-observability).

## Example

```javascript
import express from 'express';
import twilio from 'twilio';

const app = express();
app.use(express.urlencoded({ extended: false }));

// Validate + reply to inbound SMS
app.post('/sms',
  twilio.webhook({ validate: true }), // uses TWILIO_AUTH_TOKEN, checks X-Twilio-Signature
  (req, res) => {
    const twiml = new twilio.twiml.MessagingResponse();
    twiml.message(`You said: ${req.body.Body}`);
    res.type('text/xml').send(twiml.toString());
  }
);

// Manual signature validation (behind a proxy: rebuild the exact public URL)
app.post('/status', (req, res) => {
  const url = 'https://app.example.com/status';
  const valid = twilio.validateRequest(
    process.env.TWILIO_AUTH_TOKEN,
    req.header('X-Twilio-Signature'),
    url,
    req.body
  );
  if (!valid) return res.sendStatus(403);
  // MessageSid + MessageStatus: queued|sent|delivered|failed|undelivered
  console.log(req.body.MessageSid, req.body.MessageStatus);
  res.sendStatus(204);
});
```

## Pitfalls

- **Signature validation fails behind a proxy.** Twilio signs the URL *it* called. If a load balancer strips HTTPS or rewrites host, rebuild the original public URL (scheme+host+path+query) before validating, or trust `X-Forwarded-Proto`/`X-Forwarded-Host` deliberately.
- **Slow webhook responses.** Blocking work inside the handler causes Twilio's ~15s timeout, error 11200, and retries. Enqueue and return 200 immediately.
- **Duplicate status callbacks corrupt state.** Callbacks are at-least-once and can arrive out of order. Dedupe on SID+status and only move state forward.
- **JSON body parser breaks validation.** Twilio posts form-urlencoded; if you parse the body as JSON the params are empty and both TwiML logic and signature validation break.
- **Non-HTTPS or private endpoints.** Twilio requires a publicly reachable URL; validation over HTTP is weaker and some features require HTTPS. Use ngrok only for dev, never prod.
- **Returning malformed TwiML.** Invalid XML yields error 12100/12200 and a failed message/call. Use the SDK TwiML builders instead of hand-writing XML.

## Output format

```
WEBHOOK: <endpoint path>  (<sms|voice|status>)
VALIDATION: X-Twilio-Signature <PASS|FAIL>
INBOUND: MessageSid/CallSid=<SID> From=<..> To=<..>
RESPONSE: <200 TwiML | 204 no-content | 403 rejected>  latency=<ms>
STATUS: <queued|sent|delivered|failed|undelivered | ringing|in-progress|completed>
IDEMPOTENCY: key=<SID+status> action=<applied|deduped-skip>
```

## Reference

- **Auth:** Account SID (`AC...`) + Auth Token identify the account; the Auth Token is also the HMAC key for `X-Twilio-Signature`. Prefer API Keys (`SK...`) for outbound API calls, but signature validation always uses the Auth Token.
- **Signature algorithm:** `X-Twilio-Signature` = base64( HMAC-SHA1( AuthToken, fullURL + sortedConcat(POSTparams) ) ). For JSON webhook bodies, Twilio appends a `bodySHA256` query param and signs the URL. Official SDKs implement both via `validateRequest`.
- **TwiML:** XML instructions returned to Twilio. Messaging verbs: `<Message>`, `<Redirect>`. Voice verbs: `<Say>`, `<Play>`, `<Gather>`, `<Dial>`, `<Record>`, `<Hangup>`, `<Reject>`.
- **Common webhook params:** `MessageSid`/`CallSid`, `AccountSid`, `From`, `To`, `Body`, `NumMedia`, `MessageStatus`/`CallStatus`, `ErrorCode`.
- **Status values:** message `accepted, queued, sending, sent, receiving, received, delivered, undelivered, failed`; call `queued, ringing, in-progress, completed, busy, no-answer, canceled, failed`.
- **Errors:** 11200 (HTTP retrieval failure), 11205 (HTTPS connection failed), 12100/12200 (TwiML/document parse errors). See twilio-debugging-observability for lookup.
- **Compliance:** for messaging you still owe consent/opt-out (TCPA, STOP/HELP keywords are auto-handled by Twilio Advanced Opt-Out on Messaging Services).
