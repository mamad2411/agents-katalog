---
name: twilio-content-template-builder
version: 1.0.0
description: Author reusable Twilio Content API templates with typed content, variable placeholders, and channel approval, then send them by ContentSid across SMS, WhatsApp, and RCS.
author: matrixx0070
tags: [twilio, content-api, templates, whatsapp, variables]
capabilities: []
---

## When to use

Use this to build channel-portable message templates once and reuse them everywhere: a
single Content resource (ContentSid) renders as SMS text, an MMS media message, a WhatsApp
interactive template, or an RCS card/carousel depending on the destination channel. Use it
whenever you need approved WhatsApp templates, variable substitution ({{1}}, {{2}}), or
rich interactive content (quick replies, call-to-action buttons, list pickers, cards,
carousels, catalogs) that the send-time APIs reference by SID.

**Not for:** the act of delivering messages (see twilio-rcs-messaging for RCS/SMS sends and
twilio-whatsapp-messaging for WhatsApp sends); free-form one-off messages that never repeat
(just pass `Body`); voice prompts (see twilio-voice-twiml).

## Method

1. Choose a content type for the primary variant. Add channel-specific variants in the same
   Content resource so one SID serves multiple channels.
2. Author variables as `{{1}}`, `{{2}}`, ... (or named). Provide sample values in `variables`
   so approval reviewers and previews render correctly.
3. Create the template: POST to the Content API. Capture the returned `sid` (starts `HX`).
4. Decision point: does the destination channel require approval? WhatsApp templates must be
   approved by Meta before use; SMS and RCS do not require Content-level approval (RCS still
   needs a verified RBM agent — see twilio-rcs-messaging).
5. For WhatsApp, submit an ApprovalRequest with category (utility/marketing/authentication)
   and name; poll approval status until `approved` or `rejected`.
6. Send by SID: pass `ContentSid` plus `ContentVariables` (JSON map of index→value) to the
   Messages API. Twilio substitutes variables and picks the right channel variant for the
   destination.
7. Decision point: variable count mismatch? Every `{{n}}` in the body must have a key in
   ContentVariables or the send errors; unused keys are ignored.

## Example

```bash
# Create a quick-reply template with one variable.
curl -X POST https://content.twilio.com/v1/Content \
  -u "$ACCOUNT_SID:$AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "friendly_name": "order_status_qr",
    "language": "en",
    "variables": {"1": "Ada"},
    "types": {
      "twilio/quick-reply": {
        "body": "Hi {{1}}, your order shipped. Track it?",
        "actions": [
          {"id": "track", "title": "Track order"},
          {"id": "help",  "title": "Talk to support"}
        ]
      },
      "twilio/text": {"body": "Hi {{1}}, your order shipped."}
    }
  }'
```

```python
# Send it later by SID with runtime variables.
client.messages.create(
    messaging_service_sid="MGxxxx",
    to="+15551234567",
    content_sid="HXxxxx",
    content_variables='{"1": "Ada"}',
)
```

## Pitfalls

- WhatsApp approval is Meta-side and can be rejected for policy/formatting; marketing
  templates face stricter review than utility. Fix and resubmit under a new ApprovalRequest.
- `ContentVariables` must be a JSON string, not a nested object, when sent as form params.
- Variable indices are 1-based and must be contiguous as authored; a body with `{{2}}` but no
  `{{1}}` confuses substitution.
- A channel that lacks a matching variant falls back to `twilio/text` if present; without a
  text variant, sends to that channel fail. Always include a text variant for SMS reach.
- Editing an approved WhatsApp template can invalidate approval; create a new template for
  substantive changes.
- Catalog/authentication types have channel-specific required fields; validate against the
  content-type schema before POST.

## Output format

A Content resource with `sid` (`HX...`), `types` map, and `variables`. WhatsApp
ApprovalRequests return a status: `received`/`pending` → `approved` or `rejected` with a
rejection reason. At send time the ContentSid + ContentVariables produce a rendered Message.

## Reference

- Create: `POST https://content.twilio.com/v1/Content`; list `GET /v1/Content`; fetch
  `GET /v1/Content/{Sid}`; delete `DELETE /v1/Content/{Sid}`.
- WhatsApp approval: `POST https://content.twilio.com/v1/Content/{Sid}/ApprovalRequests/whatsapp`;
  fetch status `GET /v1/Content/{Sid}/ApprovalRequests`.
- Content types: `twilio/text`, `twilio/media`, `twilio/quick-reply`,
  `twilio/call-to-action`, `twilio/list-picker`, `twilio/card`, `twilio/carousel`,
  `twilio/catalog`, `whatsapp/card`, `whatsapp/authentication`.
- Variables: `{{1}}`-style placeholders substituted at send via `ContentVariables` (JSON).
- WhatsApp limits: quick-reply up to 3 buttons; call-to-action up to 2 buttons (1 URL +
  1 phone); list-picker up to 10 items; body text limits per WhatsApp template policy.
- Content template creation/storage has no per-template fee; delivery bills at the
  destination channel's message rate (WhatsApp conversation pricing, SMS segment, RCS RBM).
