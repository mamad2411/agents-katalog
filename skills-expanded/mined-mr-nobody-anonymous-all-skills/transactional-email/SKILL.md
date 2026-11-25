---
name: transactional-email
description: "Send transactional email reliably: provider APIs, SPF/DKIM/DMARC alignment, template versioning, bounce handling and deliverability monitoring."
type: procedural
category: communication
domain: communication
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - transactional email setup
  - spf dkim dmarc
  - email bounce handling
  - email template versioning
  - resend api integration
keywords:
  - email
  - smtp
  - spf
  - dkim
  - dmarc
  - deliverability
  - transactional
source: custom
enabled: true
---

# Transactional Email

## Purpose

Send transactional email reliably: provider APIs, SPF/DKIM/DMARC alignment, template versioning, bounce handling and deliverability monitoring.

## When to Use

- An application must send receipts, invites or password resets.
- Mail lands in spam and authentication records need checking.
- Bounces and complaints must feed back into the product.

## When NOT to Use

- You need marketing campaign tooling with segmentation and drip flows.
- The volume is a one-off manual message.
- The user has not consented or the message would be unsolicited.

## Capabilities

- Integrate a provider API with idempotent send keys.
- Configure SPF, DKIM and DMARC with alignment for the sending domain.
- Version templates and render them with escaped variables.
- Process bounces and complaints to protect sender reputation.

## Inputs

- The sending domain and its DNS control.
- The provider (Resend, SES, Postmark) and its API key scope.
- The email types and their required data fields.

## Workflow

1. Verify domain ownership and publish SPF, DKIM and DMARC records.
2. Send a test to a real mailbox and inspect the headers for alignment.
3. Template with a single escaping strategy; never interpolate raw HTML from users.
4. Attach an idempotency key per logical send to avoid duplicates on retry.
5. Wire bounce/complaint webhooks into suppression lists.

## Tools

- provider API (e.g. Resend)
- DNS records
- webhook handler

## Examples

- `allskills mcp install --harness claude --servers resend`
- `dig +short TXT _dmarc.example.com`
- `curl -s https://api.resend.com/emails -H "Authorization: Bearer $RESEND_API_KEY" -d @mail.json`

## Safety

- Never send to a purchased list; reputation damage is immediate and hard to reverse.
- A missing DMARC record lets attackers spoof your domain.
- Test emails must not reach real customers; use sandbox recipients.

## Source

All-Skills canonical library (`skills/communication/transactional-email`). First-party skill, maintained in this repository.

## Notes

- Start DMARC at `p=none` with reporting before enforcing `p=reject`.
- Transactional and marketing traffic belong on separate subdomains.
- Pairs with: `communication/sms-messaging`, `security/secrets-management`.
