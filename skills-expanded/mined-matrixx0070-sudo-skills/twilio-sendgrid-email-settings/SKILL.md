---
name: twilio-sendgrid-email-settings
version: 1.0.0
description: Configure account-wide SendGrid mail behavior — sandbox mode, footer, click/open tracking, subscription tracking, BCC, spam checker, and the tracking settings that affect deliverability.
author: matrixx0070
tags: [sendgrid, mail-settings, tracking-settings, sandbox, subscription-tracking, click-tracking, open-tracking]
capabilities: []
---

## When to use

Use this when you need to change how SendGrid treats every message account-wide — enabling/disabling click and open tracking, adding a compliant footer, forcing TLS, or turning on the spam checker — via the Mail Settings and Tracking Settings APIs.

**Not for:** per-message options set in the send payload (see `twilio-sendgrid-email-send`) or per-recipient suppression management (see `twilio-sendgrid-suppressions`).

## Method

1. Distinguish the two setting groups. Mail Settings (`/v3/mail_settings/*`) govern message handling: footer, forward spam, forward bounce, BCC, bounce purge, address whitelist, template, plain content. Tracking Settings (`/v3/tracking_settings/*`) govern instrumentation: click, open, subscription, Google Analytics.
2. Set click and open tracking deliberately. Open tracking injects a pixel; click tracking rewrites URLs through your branded link domain. Decision point: sensitive/high-trust transactional mail (2FA codes, legal notices) → disable tracking to avoid URL rewriting and pixel warnings.
3. Enable subscription tracking to inject a compliant one-click unsubscribe. This is effectively mandatory for bulk/marketing mail and improves reputation by giving recipients an alternative to the spam button.
4. Use the footer setting for a global compliance footer (physical address, unsubscribe) when your templates do not already include one.
5. Use sandbox mode during development — but note sandbox is a per-request mail setting in the send payload, not an account toggle; the account-level spam checker (`mail_settings/spam_check`) is separate and screens outbound content.
6. Enforce TLS via the account's transport requirements where available so mail is not sent in cleartext to receivers that support STARTTLS.
7. Read current state before writing. GET each setting, change only the field you intend, PATCH back.

## Example

Enable subscription tracking and disable click tracking for a transactional stream:

```bash
# Turn on one-click unsubscribe injection
curl -sS -X PATCH https://api.sendgrid.com/v3/tracking_settings/subscription \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true}'

# Turn OFF URL rewriting so 2FA links stay untouched
curl -sS -X PATCH https://api.sendgrid.com/v3/tracking_settings/click \
  -H "Authorization: Bearer $SENDGRID_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'
```

## Pitfalls

- **Click tracking on security mail.** Rewritten URLs and redirect domains alarm users and some filters on 2FA/reset mail. Disable tracking on those streams.
- **Open-tracking pixel on plaintext-critical mail.** The pixel forces HTML and can trip filters; skip it where it adds no value.
- **Blind PATCH without GET.** Settings objects have multiple fields; PATCHing a partial body you assembled from memory can wipe a value. Read first.
- **Assuming sandbox is account-wide.** Sandbox mode is per-request in the send payload. Leaving it "on" in code means nothing ever delivers.
- **No unsubscribe path.** Marketing mail without subscription tracking or a footer link drives spam complaints and reputation loss.

## Output format

```
# Mail/Tracking Settings: <account/stream>
MAIL SETTINGS: footer=<on/off> forward_spam=<..> bcc=<..> spam_check=<on/off>
TRACKING: open=<on/off> click=<on/off> subscription=<on/off>
TLS: enforced=<yes/no>
RATIONALE: <why each toggle for this stream>
CHANGED: [<field: old -> new>]
VERIFY: GET <setting> -> reflects change
```

## Reference

- Mail Settings: `GET/PATCH https://api.sendgrid.com/v3/mail_settings/{footer,forward_spam,forward_bounce,bcc,bounce_purge,address_whitelist,template,plain_content,spam_check}`.
- Tracking Settings: `GET/PATCH https://api.sendgrid.com/v3/tracking_settings/{click,open,subscription,google_analytics}`.
- Auth: `Authorization: Bearer <API_KEY>`; PATCH bodies are partial JSON.
- Deliverability note: subscription tracking (one-click unsubscribe) and a compliant footer directly reduce spam complaints; tracking on transactional/security mail can hurt more than help. Tune per stream, not globally.
