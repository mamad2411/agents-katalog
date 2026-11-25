---
name: twilio-sendgrid-inbound-parse
version: 1.0.0
description: Receive inbound email with the SendGrid Inbound Parse Webhook — MX setup, multipart parsing, attachments, spam/SPF fields, and safe handling of untrusted mail.
author: matrixx0070
tags: [sendgrid, inbound-parse, mx-record, multipart, attachments, reply-handling, spam-check]
capabilities: []
---

## When to use

Use this when your app must receive email — replies to notifications, support@ inboxes, email-to-action flows — by having SendGrid parse incoming mail and POST it to your endpoint via Inbound Parse.

**Not for:** tracking outbound delivery/engagement (see `twilio-sendgrid-webhooks`) or sending mail (see `twilio-sendgrid-email-send`).

## Method

1. Pick a hostname/subdomain to receive on (e.g. `parse.yourdomain.com` or `reply.yourdomain.com`). It must be one you control DNS for and is distinct from your send subdomain.
2. Add an MX record pointing that host to `mx.sendgrid.net` (priority 10). Without the MX record, mail never reaches SendGrid to be parsed.
3. Configure the Inbound Parse setting: map the hostname to your HTTPS POST URL. Optionally enable "POST the raw, full MIME message" and "Check incoming emails for spam."
4. Parse the request as `multipart/form-data`, not JSON. Fields include `from`, `to`, `subject`, `text`, `html`, `headers`, `envelope`, `charsets`, `attachments` (count), `attachmentN` (files), and `SPF`/`dkim`/`spam_score`/`spam_report` when enabled.
5. Handle attachments from the multipart file parts (`attachment1`, `attachment2`, ...); `attachment-info` gives filenames and content types. Respect `charsets` to decode fields correctly (UTF-8 is not guaranteed).
6. Treat all content as untrusted. Strip/parse quoted reply history, sanitize HTML before rendering, and validate the sender against expectations before taking action.
7. Respond `2xx` quickly; non-2xx makes SendGrid retry and can drop mail.

## Example

Express handler using multer for the multipart parts:

```js
const upload = multer();
app.post('/inbound', upload.any(), (req, res) => {
  res.sendStatus(200);                       // ack fast
  const { from, subject, text, envelope, SPF, spam_score } = req.body;
  const to = JSON.parse(envelope || '{}').to;
  if (SPF !== 'pass' || Number(spam_score) > 5) return quarantine(req.body);
  const files = req.files;                    // attachment1.. as buffers
  handleReply({ from, to, subject, text, files });
});
```

## Pitfalls

- **Parsing as JSON.** Inbound Parse posts `multipart/form-data`. A JSON body parser yields empty fields. Use a multipart parser.
- **No MX record (or wrong host).** Mail bounces at the receiver; SendGrid never sees it. Verify the MX points to `mx.sendgrid.net`.
- **Assuming UTF-8.** International mail uses varied charsets; the `charsets` field tells you how to decode each part. Honor it.
- **Rendering raw HTML.** Inbound HTML is hostile input. Sanitize before display; never eval or auto-execute links.
- **Acting on spoofed senders.** The `from` header is forgeable. Check the `SPF`/`dkim` results and `envelope` sender before trusting identity.

## Output format

```
# Inbound Parse: <hostname>
MX: <host> -> mx.sendgrid.net (pri 10) [verified]
ENDPOINT: POST <https...>  content-type: multipart/form-data
OPTIONS: raw-mime=<on/off> spam-check=<on/off>
FIELDS USED: from,to,subject,text,html,envelope,attachments,SPF,spam_score
SECURITY: SPF/dkim check | HTML sanitize | sender validation
ACK: 2xx immediate
```

## Reference

- Inbound Parse: configured under Settings / Inbound Parse (`/v3/user/webhooks/parse/settings`); requires an MX record to `mx.sendgrid.net`.
- POST format: `multipart/form-data` with fields `from`, `to`, `cc`, `subject`, `text`, `html`, `headers`, `envelope` (JSON string), `charsets` (JSON string), `attachments` (count), `attachment1..N` (files), `attachment-info`; plus `SPF`, `dkim`, `spam_score`, `spam_report` when spam check is enabled.
- Deliverability/authentication: the `SPF` and `dkim` result fields let you decide whether inbound identity is trustworthy before acting — treat failures as untrusted.
