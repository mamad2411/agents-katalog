---
name: twilio-whatsapp-send-message
version: 1.0.0
description: Send WhatsApp messages via Twilio, honoring the 24-hour session window and using approved Content templates when it is closed.
author: matrixx0070
tags: [twilio, whatsapp, template, content, messaging]
capabilities: []
---

## When to use

Use this skill to send on the WhatsApp channel: `whatsapp:` address formatting,
deciding free-form vs template based on the 24-hour customer-care window, sending
approved templates by `ContentSid` with `ContentVariables`, attaching media, and
rendering interactive buttons/lists built through the Content API. It also covers
which conversation pricing category applies.

**Not for:** onboarding or registering a WhatsApp sender/WABA, display name, or
messaging-tier limits (use twilio-whatsapp-manage-senders), plain SMS/MMS (use
twilio-sms-send-message), or generic channel routing (use twilio-send-message).

## Method

1. Format both endpoints as `whatsapp:+E164`, e.g. `whatsapp:+15558675310`. For
   testing, send from the sandbox number `whatsapp:+14155238886` after joining.
2. Decision point — is the 24-hour window open? The window opens for 24 hours
   from the customer's most recent inbound message. If open, you may send
   free-form `Body` and/or media. If closed, you MUST send an approved template.
3. Free-form send (window open): set `Body` and optionally one `MediaUrl`.
4. Template send (window closed, or business-initiated): set `ContentSid` (an
   approved WhatsApp template) plus `ContentVariables` (JSON string mapping
   placeholder indexes to values). Do not send raw `Body` when closed — it fails
   with 63016.
5. Decision point — interactivity: quick-reply buttons, call-to-action buttons,
   and list pickers must be defined in the Content template (Content API types
   like `twilio/quick-reply`, `twilio/call-to-action`, `twilio/list-picker`) and
   sent via `ContentSid`; they cannot be injected ad hoc in `Body`.
6. Send through a `MessagingServiceSid` (WhatsApp sender attached) or a `From`
   `whatsapp:` address.
7. Set `StatusCallback` and watch for `sent`/`delivered`/`read`. WhatsApp adds a
   `read` receipt that SMS lacks.
8. Understand billing: business-initiated templates bill per conversation
   category (marketing / utility / authentication); user-initiated opens a
   service conversation.

## Example

```python
from twilio.rest import Client
client = Client(account_sid, auth_token)

# Window closed -> approved template with variables
msg = client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+15558675310",
    content_sid="HXxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
    content_variables='{"1":"Ada","2":"12345"}',
    status_callback="https://example.com/twilio/wa-status",
)
print(msg.sid, msg.status)

# Window open -> free-form with media
client.messages.create(
    from_="whatsapp:+14155238886",
    to="whatsapp:+15558675310",
    body="Here is your receipt.",
    media_url=["https://example.com/receipt.pdf"],
)
```

## Pitfalls

- Forgetting the `whatsapp:` prefix routes the message to SMS or fails; both
  `To` and `From` need it.
- Sending free-form `Body` after the 24h window closes fails with 63016; only a
  template will deliver.
- 63007 means the WhatsApp channel/sender was not found — the number is not a
  registered WhatsApp sender (see twilio-whatsapp-manage-senders).
- Templates must be pre-approved by Meta; an unapproved or paused template will
  be rejected even if the ContentSid exists.
- `ContentVariables` is a JSON string, not an object; malformed JSON drops
  substitutions and can send literal `{{1}}` placeholders.
- Rapid bursts can hit 63018 (WhatsApp rate limit) — throttle to your tier.
- Buttons/lists typed into `Body` do not render; they must live in the template.

## Output format

Returns a Message resource with `sid`, `status`, `to`/`from` (whatsapp: prefixed),
`num_segments`, `price`/`price_unit`, and `error_code`/`error_message`. Status
callbacks progress `queued` → `sent` → `delivered` → `read`, or to
`undelivered`/`failed` with a WhatsApp error code.

## Reference

- Endpoint: `POST https://api.twilio.com/2010-04-01/Accounts/{AccountSid}/Messages.json`
- Address format: `whatsapp:+E164`. Sandbox sender: `whatsapp:+14155238886`
  (recipient must first join the sandbox with the join keyword).
- Session window: 24 hours from the last inbound customer message. Inside the
  window: free-form allowed. Outside: approved template (`ContentSid` +
  `ContentVariables`) required.
- Media: single media per WhatsApp message typical; standard document/image/
  audio/video types; MMS-style 5 MB ceiling applies to media payloads.
- Interactive content via Content API: `twilio/quick-reply`,
  `twilio/call-to-action`, `twilio/list-picker`, `twilio/card`.
- Conversation pricing categories: marketing, utility, authentication, service —
  business-initiated templates bill by category; user-initiated = service.
- Error codes: 63016 message sent outside the 24h free-form window (template
  required), 63007 WhatsApp channel/sender not found, 63018 WhatsApp rate limit
  exceeded; plus generic 21211 invalid `To`, 30007 filtered.
