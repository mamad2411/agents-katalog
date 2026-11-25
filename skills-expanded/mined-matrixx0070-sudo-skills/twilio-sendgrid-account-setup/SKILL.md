---
name: twilio-sendgrid-account-setup
version: 1.0.0
description: Stand up a Twilio SendGrid account for sending — API keys, sender identity, domain authentication (SPF/DKIM/DMARC), and the checks that must pass before you send real mail.
author: matrixx0070
tags: [sendgrid, email, api-key, domain-authentication, spf, dkim, dmarc, sender-identity]
capabilities: []
---

## When to use

Use this when you are provisioning a new SendGrid account (or a new sending domain on an existing one) and need it ready to send authenticated email that lands in the inbox rather than spam.

**Not for:** composing and sending individual messages (see `twilio-sendgrid-email-send`) or tuning inbox placement after you are already sending (see `twilio-sendgrid-deliverability-advisor`).

## Method

1. Create the account and confirm the plan matches your volume. Note that Twilio and SendGrid share login for newer accounts, so decide which console you drive.
2. Mint an API key with least privilege. Prefer a Restricted Access key scoped to only the resources you use (Mail Send, plus Suppressions/Stats if needed). Never use a Full Access key for an app. Store the key once — SendGrid shows it exactly one time.
3. Authenticate your sending domain, not just a single sender. Domain Authentication publishes CNAMEs that establish DKIM signing and SPF alignment under your own domain (`em.yourdomain.com` style). Decision point: transactional-only from one address → Single Sender Verification is acceptable to start, but domain auth is required to scale and to pass DMARC.
4. Publish DNS records at your registrar: the CNAMEs SendGrid generates for DKIM/SPF, then add your own DMARC record (`_dmarc.yourdomain.com`, start at `p=none` to monitor).
5. Verify in the console until every record shows "Verified." DNS propagation can lag; do not send until green.
6. Set up link branding (CNAME for click-tracking domain) so tracked links use your domain, not sendgrid.net — unbranded links depress reputation.
7. Confirm access with a single authenticated API call before wiring the app.

## Example

Smoke-test the key and sender identity without sending bulk mail:

```bash
curl -sS https://api.sendgrid.com/v3/scopes \
  -H "Authorization: Bearer $SENDGRID_API_KEY"
```

A `200` with a scopes array confirms the key is live and shows exactly what it can do. If Mail Send is absent from the list, the key is under-scoped and sends will 403.

## Pitfalls

- **Full Access keys in app config.** A leaked full key can drain your account and alter suppressions. Scope to Restricted Access and rotate on exposure.
- **Sender verification instead of domain authentication.** Single Sender works for a demo but fails DMARC alignment and caps deliverability. Authenticate the domain.
- **Sending before DNS is verified.** Records that read "pending" mean DKIM is unsigned; mail will be penalized. Wait for green.
- **DMARC at enforcement too early.** Jumping straight to `p=reject` before confirming alignment can bounce your own legitimate mail. Start `p=none`, watch aggregate reports, then tighten.
- **Storing the key after the reveal.** SendGrid never shows a key again. Capture it into your secret store immediately.

## Output format

```
# SendGrid Setup: <domain>
API KEY: name=<...> scope=restricted perms=[mail.send, ...] stored=<vault ref>
SENDER IDENTITY: <domain-auth | single-sender> address=<...>
DNS: DKIM=verified SPF=verified LINK-BRAND=verified
DMARC: _dmarc.<domain> policy=p=none rua=<mailbox>
VERIFY: GET /v3/scopes -> 200 (mail.send present)
BLOCKERS: [<any record still pending>]
```

## Reference

- SendGrid v3 API base: `https://api.sendgrid.com/v3/`; authenticate with `Authorization: Bearer <API_KEY>`.
- Key endpoints: `/v3/scopes` (verify key), `/v3/api_keys` (manage keys), `/v3/whitelabel/domains` (domain authentication), `/v3/whitelabel/links` (link branding), `/v3/verified_senders` (single sender).
- Authentication stack: DKIM (SendGrid-generated CNAMEs), SPF (via the same CNAMEs for alignment), DMARC (your own TXT at `_dmarc`). All three reinforce deliverability and inbox placement.
- Domain authentication is the deliverability foundation — it is what lets receivers tie your mail to your domain reputation rather than the shared IP pool.
