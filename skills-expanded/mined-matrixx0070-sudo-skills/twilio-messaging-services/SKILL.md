---
name: twilio-messaging-services
version: 1.0.0
description: Configure and send through a Twilio Messaging Service (MG SID) — sender pool, sticky sender, geomatch, scaling, opt-out, and fallback.
author: matrixx0070
tags: [twilio, messaging-service, sms, a2p, scaling]
capabilities: []
---

## When to use

Use this skill when you send at volume, across multiple numbers or regions, or need Twilio to manage sender selection, opt-outs, and scaling for you. A Messaging Service (an `MG...` SID) is a container that holds a pool of senders (long codes, toll-free numbers, short codes, WhatsApp senders) plus routing and compliance settings, and you send with `MessagingServiceSid` instead of a single `From`.

Reach for it when a single number is not enough: you want sticky sender per recipient, area-code geomatch, throughput scaling across the pool, or centralized STOP/START handling.

**Not for:** one-off sends from a single number (send with `From` per `twilio-messaging-overview`), choosing whether SMS/WhatsApp/RCS is right (use `twilio-messaging-channel-advisor`), or handling the inbound/status webhooks the service triggers (use `twilio-messaging-webhooks`).

## Method

1. Create the service. `POST https://messaging.twilio.com/v1/Services` with `FriendlyName`. You get back an `MG...` SID. Set `InboundRequestUrl` and `StatusCallback` here to apply defaults to every sender in the pool.
2. Add senders to the pool. Attach phone numbers via `POST /v1/Services/{ServiceSid}/PhoneNumbers` (body `PhoneNumberSid=PN...`), short codes via `/ShortCodes`, and other channel senders via their respective sub-resources.
3. Choose sender-selection behavior. Decision point: enable Sticky Sender (`StickySender=true`) so a given recipient always sees the same number; enable Area Code Geomatch (`AreaCodeGeomatch=true`) so recipients get a local-area-code sender when one exists in the pool.
4. Configure scaling and fallback. Decision point: enable `ScaleToLongCodes` behavior / Smart Encoding, and set a fallback so that if a primary sender type is unavailable the service falls back to a long code in the pool.
5. Turn on opt-out management. Set `Usecase` and enable Advanced Opt-Out so the service auto-handles STOP/HELP/START keywords and maintains the opt-out list per sender, returning 21610 on blocked recipients.
6. Link A2P 10DLC. Decision point (US long codes): associate the service with a registered A2P campaign via TrustHub, or long-code traffic is filtered (30007). Toll-free senders need toll-free verification instead.
7. Send. Call `POST /Messages.json` with `MessagingServiceSid=MG...` and no `From`; Twilio picks the sender from the pool per your rules.
8. Sync / inspect. `GET /v1/Services/{ServiceSid}` and its sub-resources to audit pool membership and settings.

## Example

Create a service, attach a number, then send through it (Python helper lib):

```python
from twilio.rest import Client
client = Client(account_sid, auth_token)

svc = client.messaging.v1.services.create(
    friendly_name="Alerts",
    sticky_sender=True,
    area_code_geomatch=True,
    inbound_request_url="https://example.com/incoming",
    status_callback="https://example.com/status",
)

client.messaging.v1.services(svc.sid).phone_numbers.create(
    phone_number_sid="PNxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
)

msg = client.messages.create(
    to="+15558675310",
    messaging_service_sid=svc.sid,     # no from_; pool selects the sender
    body="System back online.",
)
print(msg.sid, msg.status)
```

## Pitfalls

- Do not pass both `From` and `MessagingServiceSid`. Use exactly one; `MessagingServiceSid` delegates sender choice to the pool.
- Empty pool = no send. A service with zero senders cannot deliver; add at least one number/short code first.
- Sticky Sender needs pool diversity. With one number in the pool, sticky/geomatch are no-ops.
- Opt-out is per-sender by default. A recipient who sent STOP to one number may still be reachable from another unless Advanced Opt-Out centralizes it.
- Message-level `StatusCallback` overrides the service default. If you set it per message, the service-level callback URL is ignored for that message.
- 10DLC registration is asynchronous. A newly created campaign is not active immediately; sending before approval still gets filtered.

## Output format

This skill produces a configured `MG...` Messaging Service (SID, pool membership, selection flags, opt-out and callback settings) and outbound message resources sent through it. Each send returns a `Message` resource (`SM...` SID + `status`) whose sender was chosen from the pool.

## Reference

- Service CRUD: `GET|POST https://messaging.twilio.com/v1/Services` and `.../Services/{ServiceSid}`.
- Pool sub-resources: `.../Services/{ServiceSid}/PhoneNumbers`, `/ShortCodes`, `/AlphaSenders`.
- Key service properties: `StickySender`, `AreaCodeGeomatch`, `SmartEncoding`, `InboundRequestUrl`, `InboundMethod`, `StatusCallback`, `Usecase`, `UseInboundWebhookOnNumber`.
- Send with the service: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json` with `MessagingServiceSid=MG...`.
- Throughput: US long-code A2P MPS depends on the registered campaign's trust score / Twilio number type; toll-free supports higher throughput once verified; short codes are highest (~100+ MPS). Twilio queues excess and drains at the allowed rate; a large backlog can hit the validity period and expire.
- Compliance: A2P 10DLC brand + campaign registration via TrustHub for US long codes; toll-free verification for toll-free senders. Errors: 21610 (recipient opted out), 30007 (filtered), 21408 (region not enabled).
