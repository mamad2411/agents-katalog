---
name: data-privacy-compliance
description: Engineering for personal data — minimization, retention, deletion, subject rights, and compliance basics (GDPR, India DPDP, CCPA-class laws) as buildable requirements. Use when handling user personal data (names, mobiles, emails, addresses, IDs), designing signup/KYC/contact features, adding analytics or third-party trackers, planning data retention or deletion, or when the user says "privacy", "PII", "GDPR", "DPDP", "compliance", "user data", or "right to be forgotten".
---

# Data Privacy Compliance

Personal data is not an asset with a downside; it's a **liability with a use case**. Every mobile number you store can leak, be subpoenaed, be demanded back by its owner, or trigger a regulator. The engineering stance: collect the minimum, know where every copy lives, and be able to prove deletion. Retrofitting privacy is 10× the cost of designing it in — this skill is the design-it-in checklist.

(Legal disclaimer that is itself a rule: this skill makes you *ready* for compliance; the final word on GDPR/DPDP/sector rules for your product comes from qualified counsel. Flag to the user when their situation needs one — payments, health, minors, cross-border.)

## Gate 1: Minimization — the cheapest compliance is data you don't have

- For every field collected: **what feature needs it?** No feature, no field. "Might be useful later" is how liability accumulates. Optional fields default to not-asked, not merely not-required.
- Collect at the moment of need, not at signup ("we'll need GSTIN eventually" → ask when they create their first tax invoice).
- Derived beats raw: store age-band not birthdate, city not GPS trail, "verified: yes" not the ID document — whenever the feature allows.
- Third-party sprawl counts: every analytics snippet, error tracker, and marketing pixel is you *sharing* personal data. Each gets the question: what do they receive, is it configured to mask it (IP anonymization, PII scrubbing in the error tracker), and is there an agreement (DPA) behind it? Keep the list of processors written down — every privacy law asks for it.

## Gate 2: The data map — you can't protect what you can't find

Maintain a one-page inventory: **each category of personal data × where it lives** — primary DB tables, logs, error tracker, analytics, backups, exports, search indexes, caches, third parties, spreadsheets someone downloaded. This map is the prerequisite for every other gate, and it's what deletion requests get executed against. Update it when schemas change (same-PR rule, docs-and-runbooks).

The copies everyone forgets: request logs with PII in URLs (put identifiers in bodies/headers, not paths/query strings), error-tracker payloads, LLM prompts sent to AI providers (ai-engineering — that's a processor too), webhook payloads stored raw, and old exports in object storage.

## Gate 3: Protection tiers (proportional, not theatrical)

- Baseline for all personal data: encrypted in transit (everywhere, including internal hops) and at rest (disk/DB-level suffices for most), access through the app's authz — no shared read-everything DB credentials for humans; admin access audited (saas-multi-tenancy's admin rules).
- Elevated for sensitive classes (government IDs, financial account numbers, health, anything about minors): field-level encryption or tokenization, masked in every UI/log (`****1234`), access logged per-view, and a real justification for storing it at all (see Gate 1).
- Logs and analytics are the leak-by-default channel: PII masked at the logging layer (observability-readiness's rules), not by per-callsite discipline.

## Gate 4: Retention and deletion — the part that must be BUILT

"Delete on request" is a feature with real engineering inside; laws (GDPR erasure, DPDP) make it mandatory, and it cannot be bolted on later:

- **Retention schedule**: for each data category, how long and why ("invoices: 8 years, tax law" — legal holds beat deletion requests, and that's fine, but write it down). "Forever, by default" is the anti-pattern; a scheduled purge job enforces the schedule (idempotent, audited, tested).
- **Deletion capability**: one tested procedure that, given a person, removes/anonymizes them across the data map — DB rows, files, search indexes, caches, and requests forwarded to processors. Where financial records must survive (they usually must), **anonymize**: keep the transaction, sever the person (name → "Deleted user", contact fields nulled).
- Backups: industry-accepted answer is documented — deleted data expires with backup rotation (e.g., "gone from backups within 35 days"), and restores replay deletions. Write this down; auditors ask.
- Account/tenant offboarding runs the same machinery (saas-multi-tenancy Gate 4: export → grace window → purge).

## Gate 5: Subject rights and consent — the user-facing surface

- **Export** ("give me my data"): produce a person's data in usable form — mostly a scoped query + JSON/CSV. Build it once, before it's requested with a deadline attached.
- **Consent where required** (marketing communications, tracking cookies, anything beyond providing the service): recorded with timestamp and version of what they agreed to; withdrawable as easily as given; defaults unchecked. Transactional messages (OTP, invoice) don't need marketing consent — don't mix the streams, and honor unsubscribe on the marketing one.
- Privacy policy states what you actually do (generated-boilerplate that contradicts your data map is worse than none). Update it when the map changes.

## Gate 6: Breach readiness (before, not during)

You'll be judged on speed and honesty: know **who** decides (name a person), **what** laws require notification and in what window (GDPR: 72h to regulator; DPDP: notify the Board and affected users; know yours), and **how** you'd determine scope — which is your audit trail and access logs again (observability-readiness). A 30-minute tabletop drill ("support laptop stolen — what do we do?") is the whole preparation, and it's 30 minutes.

## Review checklist for any new feature touching personal data

- [ ] New fields pass Gate 1 (feature-justified, minimal, derived where possible).
- [ ] Data map updated; new third-party recipients added to the processor list.
- [ ] Fields masked in logs/errors; not in URLs.
- [ ] Deletion procedure covers the new data; retention class assigned.
- [ ] If it's a new sensitive class or crosses borders — flag for counsel, don't improvise.
