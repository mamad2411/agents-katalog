---
name: twilio-notifications-alerts-advisor
version: 1.0.0
description: Design reliable transactional notifications and alerts on Twilio — channel choice across SMS/WhatsApp/push/email, transactional-vs-promotional consent, delivery guarantees, and fallback chains.
author: matrixx0070
tags: [twilio, notifications, alerts, transactional, multichannel, delivery]
capabilities: []
---

## When to use

Use this when you are sending transactional notifications — OTP codes, order/shipping updates, appointment reminders, security alerts, account events — and need them to arrive reliably on the right channel. Use it when deciding between SMS, WhatsApp, push, or email, when designing a fallback if the primary channel fails, or when you must be sure a message is genuinely transactional and not sliding into marketing.

**Not for:** promotional or offer messaging and its consent rules (see `twilio-marketing-promotions-advisor`), provisioning the sending number or sender (see `twilio-numbers-senders`), or HIPAA-scoped health notifications (see `twilio-security-compliance-hipaa`).

## Method

1. Confirm the message is truly transactional: it is triggered by, and directly serves, an action the user took (a code, a receipt, a status change). Decision point: if it advertises or upsells at all, it is marketing — route it through `twilio-marketing-promotions-advisor` and its consent rules instead.
2. Choose the channel per notification, not per app. Time-critical + universal reach → SMS; rich/interactive + international where WhatsApp dominates → WhatsApp; in-app engaged users → push; long-form or receipts → email. Match urgency, richness, and where the user actually is.
3. Decide direct Messaging API vs an orchestration layer. For a single channel, call the Messaging API directly. For multi-channel with per-user preferences and fallback, use a higher-level layer (Twilio Verify for OTP specifically; Messaging Services / Notify-style patterns for broadcast and routing).
4. Design the fallback chain explicitly: e.g. push → if no delivery receipt in N seconds → SMS → if failed → email. Trigger each next hop on delivery status, not on a blind timer alone.
5. Wire delivery status callbacks. Set a `StatusCallback` URL and act on `queued`/`sent`/`delivered`/`undelivered`/`failed` to drive retries and fallback, and to alert on systemic failures.
6. Respect consent scope even for transactional. Transactional messages still require the user to have provided the number for that purpose; sending unrelated content on a transactional channel breaks trust and can violate rules. Keep transactional and marketing streams separate.
7. Set sensible reliability controls: use validity period / TTL so stale time-critical alerts do not deliver late, choose a sender that carriers trust (registered 10DLC, short code for high-volume OTP, or WhatsApp sender), and make OTP flows use Twilio Verify rather than hand-rolled codes.
8. Monitor and alert on delivery rate and error codes; if a channel degrades, fail traffic over rather than retrying into the same failure.

## Example

Send an alert with a status callback so you can drive fallback on the delivery result:

```bash
curl -sX POST "https://api.twilio.com/2010-04-01/Accounts/$ACCOUNT_SID/Messages.json" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "From=+15559876543" \
  --data-urlencode "Body=Your Acme order #1847 has shipped. Track: acme.co/t/1847" \
  --data-urlencode "StatusCallback=https://api.acme.com/twilio/status" \
  --data-urlencode "ValidityPeriod=600"
```

For OTP, prefer Verify (handles code generation, delivery, and channel fallback):

```bash
curl -sX POST "https://verify.twilio.com/v2/Services/$VERIFY_SERVICE_SID/Verifications" \
  -u "$TWILIO_API_KEY:$TWILIO_API_SECRET" \
  --data-urlencode "To=+15551234567" \
  --data-urlencode "Channel=sms"   # or whatsapp, call, email
```

## Pitfalls

- **Slipping marketing into a transactional message.** "Your order shipped — also, 20% off!" converts a low-consent transactional text into marketing and can trigger filtering and TCPA exposure. Keep them separate.
- **Fallback on a blind timer.** Falling back before you know the first channel failed doubles messages and cost. Trigger fallback on delivery status callbacks, with the timer as a backstop.
- **No status callbacks.** Without `StatusCallback` you cannot tell delivered from failed, so retries and fallback are guesswork. Wire callbacks and act on `undelivered`/`failed`.
- **Hand-rolled OTP.** Custom code generation and retry logic tends to leak codes, miss rate limits, and lack channel fallback. Use Twilio Verify.
- **No TTL on time-critical alerts.** A delayed OTP or "leaving now" alert delivered late is worse than not delivered. Set `ValidityPeriod` so stale messages expire.
- **Ignoring WhatsApp template rules.** Business-initiated WhatsApp notifications outside the 24-hour window must use a pre-approved template; sending free-form fails.

## Output format

```
# Notification Design: <event/alert>
TYPE: transactional (trigger=<user action>)
CHANNELS: primary=<sms|whatsapp|push|email> fallback=[<ch> -> <ch>]
LAYER: <direct Messaging API | Verify (OTP) | Messaging Service/orchestration>
DELIVERY: status-callback=<url> act-on=[undelivered,failed] ttl=<sec>
CONSENT: number-provided-for=<this purpose> marketing-separated=yes
RELIABILITY: sender=<10DLC|short-code|whatsapp> otp=Verify
MONITOR: delivery-rate=<%> watched-errors=[30003,30005,30008]
```

## Reference

- Twilio products: Messaging API (`POST /2010-04-01/Accounts/{AccountSid}/Messages.json`) for direct SMS/MMS/WhatsApp; Verify (`https://verify.twilio.com/v2/Services/{Sid}/Verifications`) for OTP with SMS/voice/WhatsApp/email channels and built-in fallback; Messaging Services for sender pools, routing, and sticky sender.
- Delivery status callback values: `accepted`, `queued`, `sending`, `sent`, `delivered`, `undelivered`, `failed`; set the receiver via the `StatusCallback` param.
- `ValidityPeriod` (seconds, default 14400 / max 14400) expires messages that can't deliver in time — critical for OTP and time-sensitive alerts.
- Consent: transactional/informational messages have a lower consent bar than marketing under TCPA, but the recipient must have provided the number for that purpose; never mix promotional content into a transactional stream.
- WhatsApp: business-initiated messages outside the 24-hour customer service window require a pre-approved Message Template.
- Common delivery errors: 30003 (unreachable handset), 30005 (unknown/inactive number), 30008 (unknown carrier error) — use them to drive fallback, not blind retries.
