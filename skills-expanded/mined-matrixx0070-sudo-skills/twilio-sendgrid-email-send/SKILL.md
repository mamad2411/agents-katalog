---
name: twilio-sendgrid-email-send
version: 1.0.0
description: Send email through the SendGrid v3 Mail Send API — personalizations, templates, attachments, categories, and correct handling of the 202 response and error bodies.
author: matrixx0070
tags: [sendgrid, mail-send, email, dynamic-templates, personalizations, attachments, api]
capabilities: []
---

## When to use

Use this when your app needs to send transactional or bulk email through SendGrid — a receipt, a password reset, a batch newsletter — via the `/v3/mail/send` endpoint.

**Not for:** account provisioning and domain auth (see `twilio-sendgrid-account-setup`) or account-wide send behavior like sandbox mode and footers (see `twilio-sendgrid-email-settings`).

## Method

1. Build the request against `POST /v3/mail/send`. The payload has `personalizations` (per-recipient blocks), `from`, and either `content` or `template_id`.
2. Use `personalizations` for recipient targeting and per-recipient substitution. Each entry can carry its own `to`/`cc`/`bcc` and `dynamic_template_data`. One send can hold up to 1000 recipients across personalizations.
3. Prefer Dynamic Templates for anything with structure: set `template_id` and pass `dynamic_template_data` per personalization. Do not send `content` alongside a dynamic template — the template owns the body.
4. Add `categories` (up to 10) so Stats and the event webhook can segment performance by message type.
5. Attach files as base64 in `attachments[]` with `content`, `type`, `filename`, and `disposition`. Keep total payload under the ~30 MB limit; large files belong behind a link.
6. Set `custom_args` (e.g. an internal message id) so webhook events map back to your records.
7. Handle the response: success is `202 Accepted` with an empty body and an `X-Message-Id` header — not `200`, and not a delivery guarantee. Parse `errors[]` on 4xx.
8. Test safely with sandbox mode (`mail_settings.sandbox_mode.enable = true`) — it validates the payload without delivering.

## Example

```bash
curl -sS -X POST https://api.sendgrid.com/v3/mail/send \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "from": {"email": "no-reply@em.yourdomain.com", "name": "YourApp"},
    "personalizations": [
      {"to": [{"email": "user@example.com"}],
       "dynamic_template_data": {"first_name": "Ada", "amount": "$42.00"}}
    ],
    "template_id": "d-xxxxxxxxxxxxxxxxxxxx",
    "categories": ["receipt"],
    "custom_args": {"order_id": "ord_9182"}
  }'
```

Expect `HTTP/2 202` with an empty body. Capture `X-Message-Id` from the response headers to correlate later webhook events.

## Pitfalls

- **Treating 202 as delivered.** 202 means accepted for processing. Actual delivery, bounces, and spam reports arrive later via the event webhook.
- **Mixing `content` with `template_id`.** With a dynamic template, the template supplies the body; extra `content` causes confusing or rejected sends.
- **Handlebars typos in `dynamic_template_data`.** A key that does not match the template renders blank silently. Verify against the template's test data.
- **Ignoring suppressions.** Sends to suppressed addresses are dropped, not delivered. Check the suppression lists (see `twilio-sendgrid-suppressions`).
- **Oversized attachments.** Base64 inflates size ~33%; large attachments blow the payload limit and slow sends. Link instead.

## Output format

```
# Send: <purpose>
ENDPOINT: POST /v3/mail/send
FROM: <authenticated domain address>
RECIPIENTS: <n> across <m> personalizations
BODY: template_id=<d-...> | inline content
CATEGORIES: [...]  CUSTOM_ARGS: {id: <...>}
RESULT: 202 Accepted  X-Message-Id: <...>
ON ERROR: errors[].message -> <action>
```

## Reference

- Endpoint: `POST https://api.sendgrid.com/v3/mail/send`; auth `Authorization: Bearer <API_KEY>`; `Content-Type: application/json`.
- Success: `202 Accepted`, empty body, `X-Message-Id` response header (the root id that prefixes webhook `sg_message_id`).
- Limits: up to 1000 recipients per send, up to 10 categories, payload ceiling ~30 MB.
- Related: Dynamic Templates managed under `/v3/templates`; event outcomes surface via the Event Webhook (see `twilio-sendgrid-webhooks`); deliverability of what you send tracked in Stats and reputation tooling.
