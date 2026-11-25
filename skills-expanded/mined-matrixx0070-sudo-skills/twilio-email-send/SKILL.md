---
name: twilio-email-send
version: 1.0.0
description: Send email via the Twilio SendGrid v3 Mail Send API with API-key auth, dynamic templates, attachments, and categories.
author: matrixx0070
tags: [twilio, sendgrid, email, api, templates, mail-send]
capabilities: []
---

## When to use

Use this when you need to send transactional or marketing email through Twilio SendGrid's v3 Mail Send API — a single `POST /v3/mail/send` with Bearer API-key auth. Use it when building personalizations for multiple recipients, rendering dynamic templates (`d-...` template IDs), attaching files, or tagging sends with categories for analytics. Use it when you want a safe dry-run via sandbox mode before real delivery.

**Not for:** SMS/voice — use twilio-webhook-architecture and twilio-reliability-patterns. SPF/DKIM/DMARC, domain authentication, IP warmup, and inbox placement — use twilio-email-deliverability-advisor.

## Method

1. Create a SendGrid API key (Settings → API Keys) with least privilege — "Mail Send" scope is enough to send. Store it as `SENDGRID_API_KEY`; never embed it client-side.
2. Authenticate every request with `Authorization: Bearer <SENDGRID_API_KEY>` and `Content-Type: application/json`. The endpoint is `POST https://api.sendgrid.com/v3/mail/send`.
3. Set a `from` address on an authenticated domain. The from-domain must pass domain authentication (DKIM/SPF) or mail lands in spam / is rejected (see twilio-email-deliverability-advisor). A verified single-sender works only for low-volume testing.
4. Build `personalizations`. Each personalization is one envelope: its own `to`/`cc`/`bcc`, `subject`, and (for templates) `dynamic_template_data`. Multiple personalizations = multiple independent messages in one API call. Decision point: to prevent recipients seeing each other, use separate personalizations, not multiple `to` entries.
5. Choose content mode. Either provide `content` (text/plain and/or text/html) OR set `template_id` to a dynamic template (`d-...`) and pass `dynamic_template_data` per personalization — do not hand-write body content when using a template.
6. Add optional features: `attachments` (base64 `content`, `type`, `filename`, `disposition`), `categories` (up to 10, for analytics), `custom_args`, `send_at` (unix epoch for scheduled send), and `reply_to`.
7. Dry-run first with `mail_settings.sandbox_mode.enable = true`: SendGrid validates the request and returns 2xx without delivering. Flip it off for real sends.
8. Handle the response. Success is `202 Accepted` with an empty body and an `X-Message-Id` header — capture it for correlation with the Event Webhook. On 4xx, read the `errors[]` array (field + message).
9. Prefer the official SDK (`@sendgrid/mail`) for retries/serialization, but the raw curl shape below is the source of truth.

## Example

```bash
curl -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "personalizations": [
      { "to": [{"email":"ada@example.com"}],
        "dynamic_template_data": { "first_name": "Ada", "order_id": "1024" } }
    ],
    "from": { "email": "receipts@mail.example.com", "name": "Example Receipts" },
    "reply_to": { "email": "support@example.com" },
    "template_id": "d-abc123def4567890abc123def4567890",
    "categories": ["receipts", "prod"],
    "attachments": [
      { "content": "'"$(base64 -w0 invoice.pdf)"'",
        "type": "application/pdf", "filename": "invoice.pdf", "disposition": "attachment" }
    ],
    "mail_settings": { "sandbox_mode": { "enable": false } }
  }'
```

```javascript
import sgMail from '@sendgrid/mail';
sgMail.setApiKey(process.env.SENDGRID_API_KEY);

const [res] = await sgMail.send({
  to: 'ada@example.com',
  from: { email: 'receipts@mail.example.com', name: 'Example Receipts' },
  templateId: 'd-abc123def4567890abc123def4567890',
  dynamicTemplateData: { first_name: 'Ada', order_id: '1024' },
  categories: ['receipts', 'prod'],
});
console.log(res.statusCode, res.headers['x-message-id']); // 202, <id>
```

## Pitfalls

- **Unauthenticated from-domain.** Sending from a domain that hasn't passed domain authentication (DKIM/SPF CNAMEs) means spam-foldering or rejection, regardless of a correct API call. Authenticate the domain first.
- **Mixing template and content.** If you set `template_id` for a dynamic template, don't also send conflicting `content`/`subject` unless the template intends it — the template's Handlebars owns the body.
- **CC/BCC leak.** Multiple `to` entries in one personalization expose recipients to each other. Use one personalization per recipient for privacy and per-recipient template data.
- **Forgetting sandbox is on.** `sandbox_mode.enable=true` returns 202 but sends nothing — a classic "why didn't my email arrive" that is actually success-without-delivery.
- **Silent 202.** 202 means accepted, not delivered. Bounces/blocks/spam show up later via the Event Webhook, not in the send response. Capture `X-Message-Id` to correlate.
- **Attachment encoding.** `content` must be base64 with no line wrapping; the wrong `type` MIME or a huge attachment (SendGrid caps total message ~30MB) fails the send.

## Output format

```
SEND: endpoint=POST /v3/mail/send  sandbox=<on|off>
FROM: <email@authenticated-domain>  template=<d-... | inline-content>
RECIPIENTS: <count personalizations>  categories=[..]
RESULT: http=<202|4xx>  x-message-id=<id | none>
ERRORS: <field: message, if 4xx>
FOLLOW-UP: <correlate via Event Webhook message_id>
```

## Reference

- **Endpoint:** `POST https://api.sendgrid.com/v3/mail/send`. Auth: `Authorization: Bearer <API key>`. Success: `202 Accepted`, empty body, `X-Message-Id` header.
- **Request body keys:** `personalizations[]` (`to`, `cc`, `bcc`, `subject`, `dynamic_template_data`, `send_at`, `custom_args`), `from`, `reply_to`, `subject`, `content[]` (`type`: `text/plain`|`text/html`, `value`), `template_id` (`d-...`), `attachments[]` (`content` base64, `type`, `filename`, `disposition`, `content_id`), `categories[]` (max 10), `send_at`, `batch_id`, `asm` (unsubscribe groups), `mail_settings.sandbox_mode`, `tracking_settings`.
- **Dynamic templates:** created in the SendGrid UI/API, IDs prefixed `d-`; use Handlebars (`{{first_name}}`) rendered from `dynamic_template_data`. Legacy transactional templates are separate.
- **Sandbox mode:** `mail_settings.sandbox_mode.enable=true` validates and returns 202 without sending.
- **Categories vs custom_args:** categories (≤10) group sends for Stats/analytics; `custom_args` are opaque key/values echoed in the Event Webhook.
- **Limits:** up to 1000 recipients per request across personalizations; total message size ~30MB.
- **Events:** delivery outcome (delivered, bounce, dropped, spamreport, open, click) arrives via the SendGrid Event Webhook, correlated by `sg_message_id`.
- **Compliance:** transactional email is exempt from CAN-SPAM unsubscribe requirements but still must not be deceptive; marketing email must include a physical address and unsubscribe (use ASM unsubscribe groups).
