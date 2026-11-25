---
name: targetbay-email-sms-best-practices
description: Use when building or fixing email and SMS for an ecommerce store — emails landing in spam, high bounce or complaint rates, setting up SPF/DKIM/DMARC, registering A2P 10DLC, capturing subscribers and consent, designing lifecycle flows (abandoned cart, post-purchase, review request, replenishment, win-back), meeting CAN-SPAM/GDPR/CASL/TCPA, handling webhooks and retries, making emails accessible, or deciding transactional vs marketing.
license: MIT
metadata:
  author: TargetBay
  version: "1.0.0"
  homepage: https://targetbay.com
---

# TargetBay Email & SMS Best Practices

Guidance for building deliverable, compliant, revenue-producing email and SMS for an ecommerce
store.

Two channels, one reputation, one consent record. Most failures in this domain are not creative
failures — they are a missing DNS record, an unregistered SMS campaign, a suppression list that the
send path can bypass, or a flow that keeps mailing someone who already bought.

## Architecture Overview

```
[Visitor] → [Capture: form, popup, checkout] → [Validation] → [Double Opt-In]
                                                                     ↓
                                              [Consent recorded — per channel]
                                                                     ↓
                    [Suppression + quiet-hours check] ←────── [Ready to send]
                              ↓
              ┌───────────────┴───────────────┐
              ↓                               ↓
    [Email: idempotent send + retry]   [SMS: consent + 10DLC + local time]
              ↓                               ↓
              └───────────────┬───────────────┘
                              ↓
                       [Webhook events]
                              ↓
        ┌──────────┬──────────┬────────────┬──────────┐
        ↓          ↓          ↓            ↓          ↓
    Delivered   Bounced   Complained   Opted-out   Clicked
                    ↓          ↓            ↓
              [Suppression list updated — per channel]
                              ↓
                   [Hygiene + sunset jobs]
```

## Quick Reference

| Need to... | See |
|------------|-----|
| Set up SPF/DKIM/DMARC, fix spam placement | [Deliverability](./references/deliverability.md) |
| Get SMS actually delivered — 10DLC, carrier filtering, segments | [SMS Deliverability](./references/sms-deliverability.md) |
| Meet CAN-SPAM, GDPR, CASL; build unsubscribe | [Compliance](./references/compliance.md) |
| Meet TCPA, state texting laws, quiet hours, STOP/HELP | [SMS Compliance](./references/sms-compliance.md) |
| Decide transactional vs marketing | [Email Types](./references/email-types.md) |
| Build order confirmations, password resets, OTPs | [Transactional Emails](./references/transactional-emails.md) |
| Plan which emails this store needs | [Transactional Email Catalog](./references/transactional-email-catalog.md) |
| Send campaigns, newsletters, promotions | [Marketing Emails](./references/marketing-emails.md) |
| Design cart, post-purchase, review, win-back flows | [Ecommerce Flows](./references/ecommerce-flows.md) |
| Build signup forms, popups, double opt-in, SMS opt-in | [Email Capture](./references/email-capture.md) |
| Handle bounces, complaints, suppression, sunsetting | [List Management](./references/list-management.md) |
| Handle retries, idempotency, timeouts, queueing | [Sending Reliability](./references/sending-reliability.md) |
| Process delivery events, verify webhooks | [Webhooks & Events](./references/webhooks-events.md) |
| Make emails readable by screen readers and in dark mode | [Accessibility](./references/accessibility.md) |
| Design the template — layout, type, colour, CTA, imagery | [Email Template Design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design) |
| Wire the automation that sends it — trigger, operations, guardrails | [Marketing Automation Recipes](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-marketing-automation-recipes) |

## Start Here

**New store, nothing set up yet?**
Plan the message set first with the [Catalog](./references/transactional-email-catalog.md), then do
[Deliverability](./references/deliverability.md) — authentication has to be live before the first
send, not after the first complaint.

**Emails going to spam?**
[Deliverability](./references/deliverability.md) first. Authentication is the most common cause,
and Gmail, Yahoo and Outlook now reject unauthenticated bulk mail at the SMTP level rather than
filtering it.

**Starting SMS?**
[SMS Compliance](./references/sms-compliance.md) → [SMS Deliverability](./references/sms-deliverability.md),
in that order. Consent and registration are prerequisites for delivery, not paperwork to catch up
on later. Unregistered US traffic is not filtered — it is blocked outright.

**Running campaigns and flows?**
[Email Capture](./references/email-capture.md) (collect consent) →
[Compliance](./references/compliance.md) (legal floor) →
[Marketing Emails](./references/marketing-emails.md) (campaigns) →
[Ecommerce Flows](./references/ecommerce-flows.md) (the automated revenue).

**Production-grade sending?**
[Sending Reliability](./references/sending-reliability.md) (idempotency + retry) →
[Webhooks & Events](./references/webhooks-events.md) (know what happened) →
[List Management](./references/list-management.md) (act on it).

**Accessibility?**
Most ecommerce email fails basic checks. See [Accessibility](./references/accessibility.md) for
`lang`, presentational tables, heading order, alt text, `<title>`, contrast and dark mode.

**Designing what the email looks like?**
This skill covers whether a message arrives and what it must contain. How it is laid out — width,
type, colour, dark mode appearance, calls to action, imagery — is the companion skill,
[Email Template Design](https://github.com/targetbay360/targetbay-agent-skills/tree/main/targetbay-email-template-design).
Do [Accessibility](./references/accessibility.md) first; the design decisions there assume it.
