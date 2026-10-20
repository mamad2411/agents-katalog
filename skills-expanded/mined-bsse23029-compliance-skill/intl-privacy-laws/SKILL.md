---
name: intl-privacy-laws
description: GDPR and the ePrivacy cookie rules, CCPA/CPRA including the 2026 ADMT and cybersecurity-audit regulations, and the HIPAA applicability gate. Use when EU/EEA or California data subjects are in scope, or to record why a US health-data regime does not apply.
---

# International privacy law

Registry: `EU-GDPR`, `EU-EPRIVACY`, `US-CCPA`, `US-HIPAA`.

These sit **on top of** Saudi PDPL for this product, never instead of it. A hotel in Riyadh taking
bookings from Europe is subject to both.

## GDPR — `EU-GDPR`

Applies through Article 3(2): offering services to people in the EU/EEA. For this product that is
the guest-facing booking path, not the staff back office.

Where it differs from PDPL in ways that change the code:

| Area | Note |
|---|---|
| Legitimate interests | Broader and more usable than under PDPL — do not copy a GDPR LI assessment into a Saudi context |
| Data subject rights | Adds portability in a structured, machine-readable format and the right to object |
| Breach notification | 72 hours to the supervisory authority — currently stricter than what the Digital Omnibus proposes |
| Records of processing | Article 30 — a documentation artefact, not a code one |
| Processor terms | Article 28 contracts with every processor |
| Transfers | Chapter V — a second, independent transfer analysis alongside the PDPL one |
| Representative | Article 27 EU representative may be needed for a non-EU controller |

**Under revision.** The Commission's Digital Omnibus (proposed 19 Nov 2025) would change breach
reporting to a high-risk-only threshold, give an explicit legitimate-interest route for AI training
and operation with safeguards, and reform cookie consent (single-click accept/refuse-all, choices
respected for at least six months). The AI omnibus was adopted; the **data omnibus touching GDPR was
still in negotiation as of mid-2026**. Do not redesign consent or breach workflows on the proposal —
check the registry entry first.

## ePrivacy — `EU-EPRIVACY`

The rule that actually governs cookies and any read/write to the browser's terminal equipment,
including `localStorage`. Consent **before** the write, for anything not strictly necessary.
Frontend surface — see `frontend-compliance` F-05. Also in scope of the Digital Omnibus reform.

## CCPA/CPRA — `US-CCPA`

Only in scope once the business meets CCPA thresholds for California residents. Check that first
and record the answer; if the thresholds are not met, this is one `n/a` row, not fifteen.

If in scope, the **amended regulations effective 1 January 2026** are the live change:

| Obligation | Deadline |
|---|---|
| ADMT — notice, access and opt-out for automated decision-making used in significant decisions | 1 January 2027 for uses started before then |
| Risk assessments for processing presenting significant risk (selling/sharing PI, sensitive PI, ADMT for significant decisions) | Pre-2026 activities assessed by 31 December 2027; attestations to the Agency by 1 April 2028 |
| Cybersecurity audits where processing presents significant security risk | Earliest report 1 April 2028 |

The ADMT hook matters for this product specifically if AI ever drives pricing, credit, screening or
anything decision-like about a person — cross-reference `ai-governance`.

## HIPAA — `US-HIPAA` (applicability gate)

**Presumed not applicable.** HIPAA engages only where the product handles protected health
information for a US covered entity or business associate. A hotel PMS does not — unless a
medical-spa, clinic or wellness module starts recording health information tied to US insurance
billing, or a US healthcare group deploys it for patient lodging.

Keep this as a standing `n/a` row in the backend grid with that reason recorded, so the question is
settled once. Re-open it only if a health-data module appears.

## Grid guidance

- GDPR and CCPA rows exist on both frontend and backend, with different requirements each.
- Where PDPL and GDPR require the same control, grade it once per surface and cite both ids. Where
  they diverge (transfers, legitimate interests, breach clock), they are separate rows.
