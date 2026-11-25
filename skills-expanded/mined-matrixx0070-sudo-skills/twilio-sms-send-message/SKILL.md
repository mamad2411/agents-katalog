---
name: twilio-sms-send-message
version: 1.0.0
description: Send SMS and MMS through Twilio with correct sender type, encoding-aware segmentation, and US A2P 10DLC compliance.
author: matrixx0070
tags: [twilio, sms, mms, 10dlc, encoding]
capabilities: []
---

## When to use

Use this skill for text-message-channel sends where the SMS/MMS specifics matter:
picking a 10DLC long code, toll-free, or short-code sender; predicting segment
count and cost from GSM-7 vs UCS-2 encoding; attaching MMS media; satisfying US
A2P 10DLC registration; and honoring opt-out (STOP/HELP) obligations and delivery
receipts.

**Not for:** channel-agnostic routing or Content-template mechanics (use
twilio-send-message), or any WhatsApp send which is a different channel with its
own window and template rules (use twilio-whatsapp-send-message).

## Method

1. Choose a sender type. Decision point:
   - Long code 10DLC — default US A2P sender; must be tied to a registered
     Brand + Campaign or throughput is throttled/blocked.
   - Toll-free — supports higher throughput; requires toll-free verification.
   - Short code — highest throughput, best for high-volume marketing/OTP; leased.
2. For US traffic, confirm A2P 10DLC registration is complete (Brand →
   Campaign → number attached to a Messaging Service). Unregistered US 10DLC
   traffic is heavily filtered by carriers.
3. Compose `Body`. Decision point — encoding: if every character is in GSM-7,
   segments are 160 chars (153 per part when concatenated). If any character
   forces UCS-2 (most emoji, many non-Latin scripts), segments drop to 70 chars
   (67 per part concatenated). One stray smart-quote or emoji can double cost.
4. To send MMS, add `MediaUrl` (publicly reachable HTTPS). US/Canada support MMS;
   many international destinations do not and will downgrade or fail.
5. Send via a `MessagingServiceSid` (recommended: pooling, sticky sender,
   opt-out handling) or a single `From`.
6. Ensure STOP/HELP handling: with a Messaging Service, Advanced Opt-Out manages
   STOP/START/HELP automatically. A message to a number that sent STOP fails
   with 21610.
7. Set `StatusCallback` for delivery receipts; treat `delivered` as success and
   inspect `error_code` on `undelivered`/`failed`.

## Example

```python
from twilio.rest import Client
client = Client(account_sid, auth_token)

msg = client.messages.create(
    messaging_service_sid="MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    to="+15558675310",
    body="Your code is 550913. Reply STOP to opt out.",
    status_callback="https://example.com/twilio/dlr",
)
print(msg.sid, msg.num_segments, msg.status)
```

```javascript
// Node
const msg = await client.messages.create({
  messagingServiceSid: "MGxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
  to: "+15558675310",
  body: "Cafeé 🙂",  // accented + emoji -> UCS-2, 70-char segments
});
```

## Pitfalls

- A single emoji or curly quote flips the whole message to UCS-2 (70/67-char
  segments), silently increasing segment count and cost.
- Sending unregistered US 10DLC traffic yields low deliverability and 30007
  carrier-filtered errors, not hard rejections — failures look intermittent.
- `From` numbers must be SMS-capable; a voice-only or landline number gives
  21606 (From not SMS-capable).
- Landlines and unreachable destinations surface as 30006; there is no
  pre-send guarantee a mobile check passed.
- MMS to non-US/Canada often silently degrades; do not assume media delivered.
- Ignoring STOP creates legal exposure; always route opt-out through a Messaging
  Service or your own suppression list.

## Output format

Returns a Message resource with `sid`, `status`, `num_segments` (billed unit
count), `num_media`, `price`/`price_unit` (populated after send), and
`error_code`/`error_message` on failure. Delivery receipts arrive at
`StatusCallback` as form-posts with `MessageStatus` and optional `ErrorCode`.

## Reference

- Endpoint: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
- Segmentation: GSM-7 = 160 single / 153 concatenated; UCS-2 = 70 single /
  67 concatenated. Billing is per segment.
- MMS: up to 10 `MediaUrl`, payload ≤ 5 MB; US/Canada only for reliable MMS.
- US A2P 10DLC: Brand registration + Campaign registration required; numbers
  attached to a Messaging Service. Throughput (MPS) is a function of Trust Score
  and campaign type. Toll-free requires separate verification; short codes are
  leased and provisioned separately.
- Error codes: 21211 invalid `To`, 21606 `From` not SMS-capable, 21610
  unsubscribed (STOP), 21408 region permission not enabled, 30003 unreachable,
  30006 landline/unreachable, 30007 carrier filtered.
- Opt-out keywords (default): STOP/STOPALL/UNSUBSCRIBE/CANCEL/END/QUIT to opt
  out, START/YES/UNSTOP to resume, HELP/INFO for help. Managed automatically by
  Messaging Service Advanced Opt-Out.
