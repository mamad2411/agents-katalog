---
name: twilio-send-message
version: 1.0.0
description: Send a message over any channel through the Twilio Messages API or a Messaging Service, choosing between raw Body and Content templates.
author: matrixx0070
tags: [twilio, messaging, api, omnichannel, content]
capabilities: []
---

## When to use

Use this skill when you need to send an outbound message and the channel is either
generic or not yet decided: SMS, MMS, WhatsApp, RCS, or Facebook Messenger all
flow through the same `Messages` resource. This is the right entry point when you
are choosing between a raw `Body` and a reusable Content template, deciding
between a single `From` number and a `MessagingServiceSid` pool, attaching media,
scheduling a future send, or wiring delivery status callbacks.

**Not for:** deep SMS encoding and A2P 10DLC registration mechanics (use
twilio-sms-send-message), WhatsApp session-window and template send rules (use
twilio-whatsapp-send-message), or onboarding a WhatsApp sender/WABA (use
twilio-whatsapp-manage-senders).

## Method

1. Confirm credentials: `AccountSid` and `AuthToken` (or an API Key SID/Secret).
   All calls authenticate with HTTP Basic auth over TLS.
2. Format every phone address as E.164 (`+<countrycode><number>`, no spaces or
   dashes). WhatsApp addresses are prefixed `whatsapp:+E164`.
3. Decision point — sender identity: use `MessagingServiceSid` when you want a
   number pool, sticky sender, geomatch, sender rotation, or scheduled send.
   Use a single `From` when you need one deterministic, known sender.
4. Decision point — content: use `Body` for free-form UTF-8 text on session
   channels. Use `ContentSid` + `ContentVariables` (JSON string) when sending an
   approved template (mandatory for WhatsApp outside the 24h window and for RCS
   rich cards).
5. Attach media with one or more `MediaUrl` params (publicly reachable HTTPS,
   max 10 media, each fetched by Twilio). This promotes SMS to MMS automatically.
6. Decision point — timing: to schedule, set `ScheduleType=fixed` plus `SendAt`
   (ISO-8601 UTC, 15 minutes to 7 days ahead). Scheduling requires
   `MessagingServiceSid`; `From` alone will be rejected.
7. Set `StatusCallback` to an HTTPS URL to receive delivery events
   (`queued` → `sent` → `delivered`/`undelivered`/`failed`).
8. Optionally set `ValidityPeriod` (seconds a message may live in the queue),
   `ShortenUrls=true` (Messaging Service link shortening), and `SmartEncoded`.
9. POST the form-encoded params and capture the returned Message SID (`SM...`
   for SMS/MMS, `MM...` legacy, `WA...`/`SM...` prefixes vary by channel).

## Example

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Content-template send via a Messaging Service, scheduled, with status callback
msg = client.messages.create(
    messaging_service_sid="MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    to="+15558675310",
    content_sid="HXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    content_variables='{"1":"Ada","2":"Fri 3pm"}',
    schedule_type="fixed",
    send_at="2026-07-12T15:00:00Z",
    status_callback="https://example.com/twilio/status",
)
print(msg.sid, msg.status)
```

## Pitfalls

- `Body` and `ContentSid` are mutually exclusive intents; if you pass a
  ContentSid, variable substitution comes only from `ContentVariables`.
- `ScheduleType=fixed` without a `MessagingServiceSid` fails — scheduling is a
  Messaging Service feature, not a bare-number feature.
- `MediaUrl` must be publicly fetchable at send time; Twilio pulls the asset, it
  does not accept binary upload on this endpoint.
- The initial API response returns `queued`/`accepted`, not delivery. Only the
  `StatusCallback` (or a later GET) tells you `delivered`.
- Mixing `From` and `MessagingServiceSid` in one request is ambiguous; send one.
- A `201` HTTP status means Twilio accepted the request, not that the carrier
  accepted the message — check `error_code` on later status events.

## Output format

Returns a Message resource: `sid`, `status`, `to`, `from`/`messaging_service_sid`,
`body`, `num_segments`, `num_media`, `price`, `price_unit`, `date_created`, and
`error_code`/`error_message` (null until a failure event). Scheduled messages
return `status="scheduled"` and can be canceled by updating the message to
`status=canceled` before `SendAt`.

## Reference

- Endpoint: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
- Auth: HTTP Basic (AccountSid:AuthToken, or APIKeySid:APISecret).
- Key params: `To`, `From` **or** `MessagingServiceSid`, `Body`, `MediaUrl`
  (repeatable), `StatusCallback`, `ContentSid`, `ContentVariables`,
  `ScheduleType=fixed`, `SendAt`, `ValidityPeriod`, `ShortenUrls`, `SmartEncoded`.
- Media limits: max 10 `MediaUrl` per message; MMS payload ≤ 5 MB.
- Scheduling window: 15 minutes to 7 days ahead; requires MessagingServiceSid.
- Common error codes: 21211 invalid `To`, 21606 `From` not SMS-capable,
  21408 permission not enabled for region, 21610 recipient unsubscribed (STOP),
  30003 unreachable destination, 30006 landline/unreachable, 30007 carrier
  filtered, 63007 channel not found, 63016 WhatsApp outside 24h free-form window.
- Pricing is per-segment/per-message and channel/destination dependent; check
  the returned `price` (populated asynchronously) rather than assuming.
