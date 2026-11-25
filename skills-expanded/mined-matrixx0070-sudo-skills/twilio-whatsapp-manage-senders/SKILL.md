---
name: twilio-whatsapp-manage-senders
version: 1.0.0
description: Onboard and manage Twilio WhatsApp senders — WABA linkage, phone registration, display name, quality rating, and messaging-tier limits.
author: matrixx0070
tags: [twilio, whatsapp, senders, waba, onboarding]
capabilities: []
---

## When to use

Use this skill to stand up and maintain the WhatsApp sender infrastructure:
linking a Meta WhatsApp Business Account (WABA) through Twilio's self-sign-up,
registering a phone number as a WhatsApp sender, setting the display name and
completing business verification, and monitoring quality rating and messaging
tier limits. Use the sandbox to prototype before a real sender exists.

**Not for:** actually sending messages, templates, or handling the 24h window
(use twilio-whatsapp-send-message), or non-WhatsApp channel setup. For general
send routing see twilio-send-message.

## Method

1. Decision point — sandbox vs production. For prototyping, use the shared
   sandbox sender `whatsapp:+14155238886`; recipients join with the sandbox
   keyword. No WABA required, but no custom display name and limited features.
2. For production, create/link a Meta WABA. Twilio's embedded self-sign-up
   (Tech Provider flow) connects your Meta Business, WABA, and phone number in
   one flow, or you register programmatically via the Senders API.
3. Register the phone number as a WhatsApp sender. The number must not already be
   active on the WhatsApp app; you supply it and verify ownership (SMS/voice
   OTP) during registration.
4. Set the display name and profile. Meta reviews the display name for policy
   compliance; complete Meta Business Verification to lift limits and unlock
   higher tiers.
5. Decision point — messaging tier. New senders start at the 1K tier (1,000
   unique business-initiated recipients per rolling 24h). Tiers scale to 10K,
   100K, and unlimited as sustained quality and volume warrant.
6. Monitor quality rating (Green/Yellow/Red). A sustained Red rating can flag
   the number for downgrade or restriction; Green with volume advances the tier.
7. Manage the sender lifecycle via the Senders API: create, fetch status
   (`CREATING` → `ONLINE`, or `OFFLINE`/error states), update profile, and
   delete/deregister when decommissioning.

## Example

```bash
# Create a WhatsApp sender (Senders API v2). Auth: AccountSid:AuthToken.
curl -X POST "https://messaging.twilio.com/v2/Channels/Senders" \
  --data-urlencode "sender_id=whatsapp:+15558675310" \
  --data-urlencode "profile[name]=Ada Robotics" \
  --data-urlencode "webhook[callback_url]=https://example.com/wa/inbound" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"

# Fetch sender status
curl -X GET "https://messaging.twilio.com/v2/Channels/Senders/XExxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" \
  -u "$TWILIO_ACCOUNT_SID:$TWILIO_AUTH_TOKEN"
```

## Pitfalls

- A phone number already registered in the consumer WhatsApp app cannot be
  onboarded until it is deleted from that app first.
- Skipping Meta Business Verification caps you at low tiers and restricts the
  number of registered senders.
- Display names that read as generic, misleading, or trademark-infringing get
  rejected by Meta review; align the name with the verified business.
- Quality rating is recipient-feedback driven (blocks/reports); high-friction
  marketing can push a Green number to Red and trigger tier downgrade.
- Sender creation is asynchronous — status transitions through `CREATING`; do
  not attempt to send until it reaches `ONLINE`.
- Sandbox behavior (opt-in keyword, shared number, no custom name) does not
  reflect production; validate flows again after real onboarding.

## Output format

The Senders API returns a Sender resource: `sid` (`XE...`), `sender_id`
(`whatsapp:+E164`), `status` (`CREATING`/`ONLINE`/`OFFLINE`/error),
`profile` (name, about, address, logos), `webhook`, quality/tier metadata, and
timestamps. Status polling reflects onboarding progress and current tier.

## Reference

- Senders API base: `https://messaging.twilio.com/v2/Channels/Senders`
  - `POST /v2/Channels/Senders` — create/register a sender.
  - `GET /v2/Channels/Senders/{Sid}` — fetch status.
  - `GET /v2/Channels/Senders` — list senders.
  - `POST /v2/Channels/Senders/{Sid}` — update profile/webhook.
  - `DELETE /v2/Channels/Senders/{Sid}` — deregister.
- Auth: HTTP Basic (AccountSid:AuthToken or API Key).
- Sandbox sender: `whatsapp:+14155238886` (join keyword required per recipient).
- Messaging tiers (unique business-initiated recipients / rolling 24h): 1K →
  10K → 100K → unlimited; advancement gated on quality rating and Meta Business
  Verification.
- Quality rating states: Green (high), Yellow (medium), Red (low); sustained Red
  risks flagged status and tier downgrade.
- Prerequisites: Meta Business Manager account, a WABA, a phone number not
  active on the consumer WhatsApp app, and a reachable OTP method for
  verification.
- Related send-time errors surfaced once live: 63007 (channel/sender not found)
  indicates an unregistered or not-yet-ONLINE sender.
