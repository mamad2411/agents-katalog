---
name: twilio-numbers-senders
version: 1.0.0
description: Choose and provision the right Twilio sender — long code, toll-free, short code, alphanumeric sender ID, or WhatsApp — and pool them in a Messaging Service.
author: matrixx0070
tags: [twilio, messaging, phone-numbers, sender-id, messaging-service, whatsapp]
capabilities: []
---

## When to use

Use this when you are deciding *what kind of number or sender* to send from, and then provisioning it. Reach for it when picking between a US long code, toll-free, short code, an international alphanumeric sender ID, or a WhatsApp sender — and when you want Twilio to load-balance across many numbers via a Messaging Service with sticky sender and scaling. Use it whenever "which sender type fits this country, volume, and use case" is the question.

**Not for:** the A2P 10DLC / TCR brand + campaign registration that a US long code requires before it can send at scale — that is `twilio-compliance-traffic` and, for the vendor path, `twilio-sms-isv-setup`. Not for API credentials — that is `twilio-iam-auth-setup`. This skill picks and provisions the sender; the compliance skills make it deliverable.

## Method

1. State destination country(ies), monthly volume, and traffic type (2FA/OTP, alerts, marketing, conversational). Decision point: two-way conversation rules out one-way-only senders like short codes for replies and alphanumeric sender IDs (which cannot receive).
2. Pick the sender type per market:
   - **US/Canada A2P** → **10DLC long code** (register brand+campaign) for most app traffic; **toll-free** for quick-start medium volume (requires toll-free verification); **short code** for very high throughput / premium marketing.
   - **International** → **alphanumeric sender ID** where supported (one-way, branded), or local long codes.
   - **WhatsApp** → a **WhatsApp sender** (business number approved through Twilio/Meta with message templates).
   Decision point: alphanumeric sender ID is one-way and country-dependent — confirm the destination country supports it and doesn't require registration/local number.
3. Search and buy numbers via the IncomingPhoneNumbers API with the capabilities you need (SMS, MMS, voice), or request a short code / toll-free / sender ID through the Console.
4. Create a **Messaging Service** and add your numbers to its **sender pool**. This is the recommended abstraction — you send from the service, not a single number.
5. Configure sender-pool behavior: **Sticky Sender** keeps one recipient mapped to one number for conversation continuity; the **Scaler** (number pooling) spreads volume across numbers to respect per-number throughput limits.
6. Set the inbound webhook and status-callback URLs on the Messaging Service so replies and delivery receipts reach your app.
7. Attach compliance objects: link the Messaging Service to the registered A2P 10DLC campaign (US) or verified toll-free profile before high-volume sending.
8. Send a test message through the Messaging Service SID and confirm delivery status via the status callback.

## Example

```javascript
const client = require('twilio')(process.env.TWILIO_API_KEY_SID, process.env.TWILIO_API_KEY_SECRET, {
  accountSid: process.env.TWILIO_ACCOUNT_SID,
});

// Buy an SMS-capable US long code.
const num = await client.incomingPhoneNumbers.create({ phoneNumber: '+14155550123' });

// Create a Messaging Service and add the number to its sender pool.
const svc = await client.messaging.v1.services.create({
  friendlyName: 'txn-alerts',
  stickySender: true,          // one recipient stays on one number
});
await client.messaging.v1.services(svc.sid).phoneNumbers.create({ phoneNumberSid: num.sid });

// Send FROM the Messaging Service (MG...), not a single number.
await client.messages.create({
  messagingServiceSid: svc.sid,   // MG...
  to: '+14155559999',
  body: 'Your code is 123456',
});
```

## Pitfalls

- **Alphanumeric sender ID cannot receive.** It is one-way and unsupported in many countries (including the US). Don't pick it for 2FA flows that need reply handling or for US traffic.
- **Sending from a raw long code without 10DLC.** Unregistered US long-code A2P traffic gets heavily filtered or blocked by carriers. Register the brand+campaign (see compliance skills) and link it to the Messaging Service.
- **Ignoring per-number throughput (TPS).** A single 10DLC number has a low message-per-second cap tied to your campaign tier. Pool numbers and let the Scaler distribute, or you'll queue and delay.
- **Sticky Sender vs. Scaler confusion.** Sticky keeps conversations coherent; the Scaler maximizes throughput. High-volume one-way blasts want scaling; two-way support threads want stickiness.
- **WhatsApp needs approved templates.** Business-initiated WhatsApp messages outside the 24-hour session window must use pre-approved message templates, or they are rejected.
- **Missing status callback.** Without a status-callback URL you can't see `delivered`/`undelivered`/`failed`, so failures look like successes.

## Output format

```
# Twilio Sender Provisioning
USE CASE: <2FA|alerts|marketing|conversational>  MARKETS: <countries>  VOLUME: <msgs/mo>
SENDER TYPE: <10DLC long code|toll-free|short code|alphanumeric sender ID|WhatsApp>
NUMBERS:
- +1************ (PN********) caps=<SMS,MMS,voice>
MESSAGING SERVICE: MG******************************** stickySender=<on/off> scaler=<on/off>
COMPLIANCE LINK: <A2P campaign SID | toll-free profile | WhatsApp sender> 
WEBHOOKS: inbound=<url> status=<url>
```

## Reference

- **Sender types:** 10DLC long code (US/CA A2P; needs TCR brand+campaign), toll-free (needs toll-free verification), short code (5-6 digit, highest throughput, longest lead time), alphanumeric sender ID (one-way, international, cannot receive), WhatsApp sender (Meta-approved, template-gated).
- **Messaging Service SID** = `MG...`; phone number SID = `PN...`. Sending via `messagingServiceSid` engages the sender pool.
- **Sticky Sender** = consistent number per recipient; **Scaler / number pooling** = spread volume across numbers to respect throughput.
- **Throughput (TPS/MPS)** on 10DLC is governed by your A2P campaign registration tier and brand vetting score; toll-free and short code have their own limits.
- WhatsApp business-initiated messages require **pre-approved templates** and follow Meta's 24-hour customer-service window rules.
- Numbers are provisioned through the **IncomingPhoneNumbers** REST resource; short codes, toll-free verification, and sender IDs are requested/approved via Console flows.
