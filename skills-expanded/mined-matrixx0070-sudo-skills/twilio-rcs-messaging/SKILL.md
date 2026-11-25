---
name: twilio-rcs-messaging
version: 1.0.0
description: Send RCS Business Messages through Twilio with rich cards, carousels, and suggested actions, falling back to SMS when RCS is unavailable.
author: matrixx0070
tags: [twilio, rcs, messaging, rbm, fallback]
capabilities: []
---

## When to use

Use this when you need to deliver Rich Communication Services (RCS) messages to Android
handsets through Twilio's RCS Business Messaging (RBM): branded sender, verified logo,
rich cards, horizontal carousels, and tappable suggested replies/actions (dial, open URL,
share location, calendar). RCS gives read receipts and typing indicators that SMS cannot.
You also use it when you want a single send that gracefully degrades: if the destination
handset or carrier does not support RCS, Twilio falls back to SMS/MMS on the same
Messaging Service.

**Not for:** authoring or approving the reusable templates themselves (see
twilio-content-template-builder); WhatsApp interactive templates (see
twilio-whatsapp-messaging); plain SMS/MMS-only campaigns where no RCS sender exists.

## Method

1. Register and verify an RBM agent with Google through the Twilio Console (RCS sender).
   Provide brand name, logo, colors, description, and contact info. Verification is a
   Google-side review and can take days to weeks. Test devices can be allow-listed for
   pre-launch testing before full verification.
2. Create a Messaging Service and add your RCS sender to its sender pool. Add an SMS
   number to the same pool so fallback has a route.
3. Decision point: rich content or plain text? For plain text, send a normal message body
   through the Messaging Service. For rich cards/carousels/suggested actions, author a
   Content template (twilio/card, twilio/carousel, twilio/quick-reply,
   twilio/call-to-action) and send by ContentSid.
4. Decision point: SMS fallback required? If yes, ensure the Messaging Service has an SMS
   sender; Twilio auto-falls-back when the handset is not RCS-capable. RCS-only content
   (carousels) degrades to text/media on SMS.
5. Send: POST to Messages with MessagingServiceSid + To + ContentSid (+ ContentVariables).
   Do not set From when using a Messaging Service.
6. Handle inbound: configure the Messaging Service inbound webhook to receive user taps
   on suggested replies (postback data) and free-text replies.
7. Track delivery via StatusCallback: queued, sent, delivered, read (RCS only), failed,
   undelivered. A `read` status confirms RCS delivery; its absence implies SMS fallback.

## Example

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

# Send an RCS card template; auto-falls back to SMS if handset is not RCS-capable.
msg = client.messages.create(
    messaging_service_sid="MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    to="+15551234567",
    content_sid="HXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",  # twilio/card content
    content_variables='{"1": "Ada", "2": "ORD-4417"}',
)
print(msg.sid, msg.status)
```

## Pitfalls

- RBM agent verification is gated by Google, not Twilio; nothing sends to real users until
  verified. Use test devices during build.
- Do not pass both `From` and `MessagingServiceSid`; RCS + fallback routing requires the
  Messaging Service to pick the sender.
- `read` status is RCS-only. SMS never reports `read`; do not treat missing read as failure.
- Carousels require 2-10 cards; a 1-card carousel is rejected. Suggested actions cap at 4
  per card / 11 per standalone message (Google RBM limits).
- Media in RCS cards must be publicly reachable HTTPS URLs; Twilio fetches them at send.
- RCS is Android-centric. iMessage/iOS RCS interop varies by carrier and region; assume
  SMS fallback for iOS unless verified.

## Output format

A Message resource (SID starting `SM`/`MM`) with a `status` that transitions through
queued → sent → delivered → (read for RCS). Inbound taps arrive at your webhook as
postback payloads; delivery transitions arrive at your StatusCallback URL.

## Reference

- Send endpoint: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
  with `MessagingServiceSid`, `To`, and either `Body` or `ContentSid` (+ `ContentVariables`).
- RCS sender + RBM agent are configured under Messaging in the Twilio Console; the agent is
  registered/verified with Google RBM.
- Content types usable over RCS: `twilio/text`, `twilio/media`, `twilio/quick-reply`,
  `twilio/call-to-action`, `twilio/list-picker`, `twilio/card`, `twilio/carousel`.
- Google RBM limits: carousel 2-10 cards; up to 11 suggestions per message, 4 per card;
  card media served over HTTPS.
- Status values: `queued`, `sending`, `sent`, `delivered`, `read` (RCS), `undelivered`,
  `failed`. Fallback to SMS is automatic when the handset is not RCS-capable.
- RCS Business Messaging is billed per RBM message (basic vs single/conversational rates
  vary by region and Google's RBM pricing); SMS-fallback segments bill at standard SMS
  rates. Confirm current per-message pricing in the Twilio Console before volume sends.
