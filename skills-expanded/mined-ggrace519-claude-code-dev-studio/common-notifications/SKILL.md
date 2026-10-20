---
name: common-notifications
description: Cross-channel user notifications — push, email, SMS, in-app, webhook, batching / throttling / quiet-hours, preferences, deliverability. Auto-invoked when designing notification flows, investigating open-rate drops, or implementing preferences UI.
---

# Notifications

Notifications are the fastest way to ruin user trust: too many and users silence
you, too few and they don't know you exist, wrong channel and they miss what matters.

## When to reach for this

- Designing a notification flow: which message, which channel, what default opt-in
- Building or reviewing the preferences UI and its category × channel model
- Investigating deliverability problems (open-rate drops, spam-folder placement, SMS filtering)
- Adding rate limits, quiet hours, digests, or dedupe to the sending pipeline

## Principles

1. **Preferences are a first-class surface.** Categories named in user language
   ("Order updates", not `transactional_order`), per-channel toggles, a working
   global unsubscribe — and default-on only where legally permitted.
2. **Respect quiet hours by the user's timezone.** No push at 3 AM local. Digest
   overnight non-urgent messages into a morning summary; transactional messages fire
   immediately regardless.
3. **Deliverability is ongoing work.** SPF/DKIM/DMARC alignment, IP warm-up, separate
   subdomains for transactional vs marketing, automatic suppression on bounce and
   complaint. One careless broadcast can undo a year of reputation warm-up.
4. **Cap aggressively per user.** A global per-user send cap across all categories
   (e.g. N pushes/day, M emails/week) prevents one surprise campaign from flooding a
   single user.
5. **Send-time optimization pays back on broadcast.** Per-user best-time sends
   improve open rates 20–40% over blanket blasts; never apply it to transactional.
6. **Instrument for attribution, not vanity.** Open rate is noisy (privacy proxies
   inflate it); measure click-through → completed action.
7. **Comply per channel and jurisdiction.** CAN-SPAM/CASL for email, TCPA and
   10DLC/sender-ID registration for SMS, GDPR/e-Privacy consent for anything tracked.

## Channel decision matrix

| Message type | Primary channel | Backup | Default opt-in | Quiet hours |
|---|---|---|---|---|
| Security alert (login, password change) | email + push | SMS | yes (mandatory) | ignored |
| Transactional (order, receipt, reset) | email | push | yes | ignored |
| Action needed (approval, mention, reply) | push | email | yes | digested |
| Lifecycle / engagement | email | in-app | opt-in | respected |
| Marketing / broadcast | email | — | opt-in only | respected + send-time optimized |
| System status (incident, maintenance) | in-app banner | email | yes | respected unless critical |

## Sending-pipeline checklist

- [ ] Template → localize → personalize → rate-limit → send, in that order
- [ ] Dedupe key per logical event (a retried job must not double-send)
- [ ] Per-user caps and quiet-hours check before enqueue, not after
- [ ] Bounce and complaint webhooks wired to the suppression list
- [ ] Suppression list checked on every send path, including one-off scripts
- [ ] Delivery, open, click, and conversion events emitted with the message ID
- [ ] Unsubscribe honored within the legal window and reflected in preferences UI

## Pitfalls

- Burying opt-out in a footer while the preferences page shows different state
- Sending marketing from the transactional domain — one spam complaint poisons receipts
- Quiet hours computed in server timezone instead of the user's
- Retried jobs without idempotency keys double-pinging users
- Treating Apple's mail-privacy-inflated open rates as engagement signal
- Push permission requested on first app launch, before any value is shown

---
*Related: `common-privacy` (consent and opt-out mechanics), `common-i18n` (template
localization), `common-product-analytics` (attribution events), `common-a11y`
(accessible email HTML) · pulled by any domain agent · output/ADR format:
`playbook-conventions`*
