---
name: common-privacy
description: Application-layer privacy — consent management (TCF / GPP / region-specific), DSAR fulfillment, data minimization, purpose limitation, cookie / SDK governance. Auto-invoked when designing consent flows, handling access / deletion requests, or mapping data to purposes.
---

# Privacy

Privacy posture is the sum of small choices across the stack: one rogue analytics
SDK, one unconsented email pixel, one un-redacted log line, and you're on the front
page. The application-layer privacy contract is what gets collected, why, for how
long, and how users control it.

## When to reach for this

- Designing or reviewing a consent flow (CMP integration, TCF/GPP/US-state signals)
- Handling a data subject access/deletion request, or building the DSAR workflow
- Adding a new SDK, pixel, or vendor that receives user data
- Running a privacy impact assessment on a new feature or data use

## Principles

1. **Consent is a signal, not a button.** TCF/GPP strings, first-party consent state,
   and per-purpose granularity must propagate from the CMP to every analytics pixel,
   ad tag, SDK, and server-side handler. Missing propagation is the #1 CMP audit
   failure.
2. **Map data to purposes, not to features.** Users opt into purposes ("account
   management", "personalization", "ad measurement"). A feature needing a new purpose
   triggers a notice update, never a silent change.
3. **DSARs are cross-system.** Primary DB, warehouse, ticketing, email provider,
   support tools, backups. Build the discovery map once, then automate per-request —
   manual DSARs blow the GDPR 30-day window (CCPA allows 45).
4. **Default to minimum.** Default opt-in only where legally permitted
   (transactional). Marketing, analytics, and cross-site sharing default opt-out;
   users opt in knowingly.
5. **Inventory every vendor.** Every SDK, script tag, and processor goes in a
   register with purpose, data shared, retention, sub-processor list, and DPA on
   file. New vendor → review gate before it ships.
6. **Transparency is continuous.** Version the privacy notice, surface a change
   summary in-product on update, and prefer layered notices (short → long) over a
   40-page wall.
7. **Sensitive categories get their own rules.** Children (COPPA age gates), health,
   biometric, and other special-category data need explicit handling decisions and a
   DPIA when processing is high-risk.

## DSAR fulfillment workflow

| Step | What happens | Watch for |
|---|---|---|
| 1. Intake | Request logged with type (access / delete / rectify / port) and clock started | clock starts at receipt, not verification |
| 2. Verify | Identity proven proportionate to data sensitivity | over-collection during verification is itself a violation |
| 3. Discover | Query the system-by-system data map | shadow copies: exports, support tools, backups |
| 4. Fulfill | Export in portable format, or delete/anonymize per system | deletion must reach processors and caches |
| 5. Attest | Record what was done, where, when; respond to the user | keep the attestation, not the data |

## Data-purpose map (the core artifact)

One row per data element: **element × purpose × lawful basis × retention × systems
holding it**. This single table drives consent UI granularity, DSAR discovery, the
vendor register, and retention jobs — keep it versioned next to the code.

## Pitfalls

- Consent banner that sets cookies/fires SDKs before the user chooses
- "Reject all" that takes more clicks than "Accept all" (dark pattern, regulator bait)
- Consent state stored client-side only — server-side handlers keep sending data
- Deletion that clears the primary DB but not the warehouse, search index, or backups policy
- New SDK added by a feature team straight to the tag manager, bypassing vendor review
- Logging full request bodies that contain PII the privacy notice never mentioned

---
*Related: `common-product-analytics` (consent-gated event streams),
`common-notifications` (opt-out mechanics), `security-checklist` (data-exposure
findings) · pulled by any domain agent · output/ADR format: `playbook-conventions`*
