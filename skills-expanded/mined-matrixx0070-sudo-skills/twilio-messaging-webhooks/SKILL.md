---
name: twilio-messaging-webhooks
version: 1.0.0
description: Wire Twilio inbound-message and status-callback webhooks — configure URLs, parse the POST params, validate X-Twilio-Signature, and reply with TwiML.
author: matrixx0070
tags: [twilio, webhooks, twiml, status-callback, security]
capabilities: []
---

## When to use

Use this skill when messages come back to you: a user texts your number (inbound), or the carrier reports delivery progress (status callback). It covers where to set the URLs, exactly which POST parameters Twilio sends, how to authenticate the request with `X-Twilio-Signature`, and how to answer an inbound message with TwiML.

Reach for it whenever you need two-way conversations, delivery receipts, opt-out handling, or auto-replies.

**Not for:** deciding whether to be two-way at all (use `twilio-messaging-channel-advisor`), setting the pool-wide `InboundRequestUrl`/`StatusCallback` defaults on a Messaging Service (use `twilio-messaging-services`), or first-time orientation (use `twilio-messaging-overview`).

## Method

1. Set the inbound URL. On a phone number: `A message comes in` webhook (HTTP POST). On a Messaging Service: `InboundRequestUrl`. Decision point: if the number is in a service, the service's `UseInboundWebhookOnNumber` flag decides whether the number-level or service-level URL wins.
2. Set the status callback. Per message: pass `StatusCallback=https://...` in the `POST /Messages.json` body. Service-wide: set `StatusCallback` on the `MG` service. Message-level overrides service-level.
3. Serve HTTPS + POST. Twilio POSTs form-encoded params. Return 2xx quickly; a 4xx/5xx or timeout (>15s) triggers Twilio's retry/error behavior and may fire the Fallback URL.
4. Validate every request. Decision point: recompute the `X-Twilio-Signature` (HMAC-SHA1 of the full URL + sorted POST params, keyed by your AuthToken, base64) and reject on mismatch. Use the helper library's `RequestValidator` rather than hand-rolling.
5. Handle inbound. Read `From`, `To`, `Body`, `NumMedia`, `MediaUrl0..N`. Reply with TwiML `<Response><Message>` to send an auto-reply, or return an empty `<Response/>` to stay silent.
6. Handle status. Read `MessageSid`, `MessageStatus`, and on failure `ErrorCode`; update your records. Terminal states are `delivered`, `undelivered`, `failed`.

## Example

Inbound handler with signature validation and a TwiML auto-reply (Flask + Twilio helper lib):

```python
from flask import Flask, request, abort
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)
validator = RequestValidator(auth_token)

@app.post("/incoming")
def incoming():
    sig = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(request.url, request.form, sig):
        abort(403)
    resp = MessagingResponse()
    if request.form.get("Body", "").strip().upper() == "STOP":
        return str(MessagingResponse())          # empty <Response/>, Twilio handles opt-out
    resp.message(f"You said: {request.form['Body']}")
    return str(resp)                             # TwiML XML
```

Raw TwiML an inbound handler returns:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<Response>
  <Message>Thanks! We received your message.</Message>
</Response>
```

## Pitfalls

- Signature URL must match exactly. Compute the signature over the exact URL Twilio hit, including scheme, host, path, and query string; a proxy that rewrites the host (e.g. behind a load balancer) breaks validation — reconstruct the original URL.
- Media count is 1-based-indexed but zero-offset params. `NumMedia` gives the count; media URLs are `MediaUrl0`, `MediaUrl1`, ... starting at 0.
- Do not send from the webhook and also return TwiML for the same reply. Pick one path or you double-send.
- Status callbacks are not ordered or exactly-once. You can get `sent` after `delivered`, or duplicates; make handlers idempotent on `MessageSid`.
- Slow endpoints get retried. Return 2xx within ~15s; long work must be queued asynchronously.
- MediaUrls are authenticated and expire. Fetch them with your credentials; they are not permanently public.

## Output format

This skill produces two things: (1) a validated inbound handler that returns TwiML (`<Response>` with zero or more `<Message>`/`<Media>` children, or empty `<Response/>`), and (2) a status-callback handler that records message lifecycle transitions keyed by `MessageSid`. It rejects unsigned or mis-signed requests with HTTP 403.

## Reference

- Inbound POST params: `MessageSid`, `SmsSid`, `AccountSid`, `MessagingServiceSid` (if via service), `From`, `To`, `Body`, `NumMedia`, `NumSegments`, `MediaUrl0..N`, `MediaContentType0..N`, plus geo fields `FromCity/FromState/FromZip/FromCountry`.
- Status callback POST params: `MessageSid`, `MessageStatus` (one of `queued`, `sent`, `delivered`, `undelivered`, `failed`; also `accepted`, `sending`, `receiving`, `read` for WhatsApp), `ErrorCode` (present on `undelivered`/`failed`), `From`, `To`, `SmsStatus`.
- Signature: header `X-Twilio-Signature` = base64(HMAC-SHA1(AuthToken, fullURL + concat of alphabetically-sorted POST key+value pairs)). Validate with `twilio.request_validator.RequestValidator` (Python) or the equivalent in other helper libs.
- Configuration surfaces: phone-number "A message comes in" webhook + Fallback URL; Messaging Service `InboundRequestUrl`, `InboundMethod`, `StatusCallback`, `UseInboundWebhookOnNumber`; per-message `StatusCallback` on `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`.
- TwiML messaging verbs: `<Response>`, `<Message>` (with optional `<Body>` and `<Media>` children, `action`/`method`/`statusCallback` attributes), `<Redirect>`. An empty `<Response/>` means "no reply".
- Common failure `ErrorCode`s on callbacks: 30003 unreachable, 30005 unknown destination handset, 30006 landline/unreachable, 30007 carrier filtered, 30008 unknown error; 21610 recipient opted out; 63016 WhatsApp free-form outside 24h window.
- HTTP: Twilio expects a 2xx; non-2xx or timeout (~15s) triggers the Fallback URL and error logging.
