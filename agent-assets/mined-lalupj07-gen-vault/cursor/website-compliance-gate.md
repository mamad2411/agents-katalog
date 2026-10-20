---
description: Website compliance gate — run the website-compliance-audit skill before shipping forms, trackers, embeds, images, legal pages, pricing, or checkout changes
alwaysApply: true
---

# Website Compliance Gate

## When this gate applies

Invoke the `website-compliance-audit` skill **before finishing** any work that:

- Adds/changes forms, signup, checkout, pricing, or newsletter opt-ins
- Adds analytics, trackers, cookies, localStorage/sessionStorage keys, or third-party scripts/iframes/fonts/CDNs
- Adds images, icons, fonts, testimonials, ratings, counters, logos, or marketing claims
- Touches legal pages (privacy, terms, cookie, refund) or the consent banner
- Prepares a website launch or release

Also invoke when the user asks for a compliance, legal, cookie/consent, GDPR/DPDP/CCPA, or accessibility audit.

## Hard rules (every change)

- Never invent company facts; use `{{PLACEHOLDERS}}`
- Never fabricate reviews, ratings, user counts, awards, logos, or urgency
- No non-essential script/cookie before consent; Reject all is equal weight to Accept all
- Newsletter checkbox separate and unticked; Terms acceptance is an explicit checkbox
- New cookie/storage key or third party → update cookie policy, `docs/third-parties.md`, `docs/data-inventory.md`
- New asset → record licence in `docs/asset-licenses.md`; no hotlinked or unknown-source images
- Every `<img>` has alt; icon buttons have aria-label; real `<button>`/`<a>`; visible focus; inputs labelled
- Legal text must match what the code does; mark legal files "draft, needs lawyer review"

Templates only, not legal advice. Have a qualified lawyer review.
