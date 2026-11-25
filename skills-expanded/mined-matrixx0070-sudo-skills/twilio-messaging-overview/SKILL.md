---
name: twilio-messaging-overview
version: 1.0.0
description: Orient yourself in Twilio Programmable Messaging and route to the right channel, sender, and sibling skill before you send a single message.
author: matrixx0070
tags: [twilio, messaging, sms, overview, channels]
capabilities: []
---

## When to use

Use this skill first, whenever a task involves sending or receiving messages through Twilio and you are not yet sure which channel, sender type, or configuration applies. It is the map: it names every moving part of Programmable Messaging and hands you off to the skill that does the concrete work.

Reach for it when you see phrases like "send an SMS", "text my users", "WhatsApp notifications", "why is delivery failing", or "do I need 10DLC" and you need to decide the shape of the solution before writing code.

**Not for:** picking a specific channel for a concrete use-case (use `twilio-messaging-channel-advisor`), configuring an MG Messaging Service sender pool (use `twilio-messaging-services`), or wiring inbound/status callbacks (use `twilio-messaging-webhooks`).

## Method

1. Identify the direction. Outbound (you send) vs inbound (a user texts you) vs status (delivery receipts). Inbound and status both live in `twilio-messaging-webhooks`.
2. Identify the channel. SMS (text), MMS (text + media, US/Canada), WhatsApp (`whatsapp:` prefix, template-gated), RCS (rich cards, `rcs:` agent), or voice-adjacent. Each has different sender types and compliance rules.
3. Identify the sender. A single number (`From`) or a Messaging Service (`MessagingServiceSid`, an `MG...` SID that manages a sender pool). Decision point: if you send at scale, across regions, or need sticky sender / opt-out automation, use a Messaging Service and go to `twilio-messaging-services`.
4. Check compliance gates. Decision point: US long-code SMS requires A2P 10DLC brand + campaign registration via TrustHub, or messages get filtered (error 30007). WhatsApp requires approved templates outside the 24-hour window (error 63016).
5. Choose the content path. Plain `Body`, or a pre-approved Content template referenced by `ContentSid` + `ContentVariables` (required for WhatsApp templates and RCS rich content).
6. Hand off. Once channel + sender + compliance are settled, route to the sibling skill that implements the step.

## Example

Minimal outbound SMS with the Python helper library. This is the "hello world" the other skills build on:

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)  # or Client(api_key_sid, api_key_secret, account_sid)

msg = client.messages.create(
    to="+15558675310",
    from_="+15551234567",          # or messaging_service_sid="MG..."
    body="Your code is 123456",
)
print(msg.sid, msg.status)          # SMxxxxxxxx queued
```

## Pitfalls

- E.164 only. Every number must be `+<country><number>` (e.g. `+15558675310`); malformed `To` raises error 21211.
- Registered ≠ reachable. A number can exist in your account yet be unable to send SMS (error 21606) if it is not SMS-capable or not the correct type.
- 10DLC is not optional in the US. Unregistered US long-code A2P traffic is heavily filtered by carriers; you will see silent-looking 30007 failures.
- Message length changes cost. GSM-7 is 160 chars/segment; a single emoji flips the whole message to UCS-2 at 70 chars/segment, silently doubling or tripling segments and billing.
- WhatsApp is not SMS. Free-form replies are only allowed inside the 24-hour customer-service window; otherwise you must send an approved template.

## Output format

This skill produces a decision, not an API call: a short plan naming (1) the channel, (2) the sender type (single number vs `MG` Messaging Service), (3) the compliance path (10DLC / toll-free verification / WhatsApp template), and (4) the sibling skill to execute. No message is sent from here.

## Reference

- REST base for message send/read: `https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`.
- Messaging Services: `https://messaging.twilio.com/v1/Services`. Content templates: `https://content.twilio.com/v1/Content`. Conversations: `https://conversations.twilio.com/v1`.
- Auth: HTTP Basic. Username = AccountSid, password = AuthToken; or API Key `SK...` + secret (preferred, revocable).
- Message SIDs start `SM` (SMS/MMS) or `MM`; Messaging Service SIDs start `MG`; Content SIDs start `HX`.
- Segment limits: GSM-7 160 chars (153 in a concatenated/multipart message); UCS-2 (emoji/non-Latin) 70 chars (67 concatenated).
- Core error codes: 21211 invalid `To`; 21606 `From` not valid/SMS-capable; 21610 recipient replied STOP (unsubscribed); 21408 permission to send to region not enabled; 30003 unreachable handset; 30007 carrier filtered (spam/unregistered); 30008 unknown delivery error; 63016 WhatsApp free-form outside 24h window.
- Compliance: US 10DLC via TrustHub (brand + campaign); toll-free numbers require separate toll-free verification; short codes require a provisioning application. WhatsApp senders are provisioned via the WhatsApp Sender onboarding and use approved templates.
