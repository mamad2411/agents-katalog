---
name: legal-vendor-check
version: 1.0.0
description: Reconcile the agreements that should exist for a vendor against what actually does across systems, and produce a gap analysis with a coverage verdict.
author: matrixx0070
tags: [legal, vendor, contracts, gap-analysis, compliance]
capabilities: []
---

## When to use
Use this before onboarding, renewing, or auditing a vendor, or when someone asks "are we covered with this vendor." It reconciles what agreements should exist against what actually does, and surfaces gaps that create legal or compliance exposure.

**Not for:** reviewing the terms inside a specific contract (use `legal-review-contract`), rating a single risk in depth (use `legal-risk-assessment`), or negotiating with the vendor. This is a coverage inventory, not a term-quality review.

## Method
1. **Define the vendor and relationship.** What they provide, data they touch, spend level, criticality.
2. **List agreements that should exist** for this relationship type: master agreement / order form, DPA (if personal data), security addendum, BAA (if applicable), SOW, plus required certifications or insurance. *Decision point:* if they touch personal or regulated data with no DPA/BAA, that's an automatic high-severity gap.
3. **Pull actual status from each system** available (contract repository, procurement, finance, security records). Per document: present? executed? current version? expiry date?
4. **Reconcile.** Match expected vs. found; mark present / missing / expired / superseded / unsigned.
5. **Analyze gaps.** For each missing or expired item, state the exposure (unprotected data, uncapped liability, compliance failure) and severity.
6. **Check dates.** Flag anything expiring within the renewal window and any auto-renewal triggers.
7. **Recommend actions** to close each gap, with owner and deadline.

## Example
Vendor: cloud analytics provider, processes customer PII, $120k/yr, business-critical. Expected: MSA, DPA, security addendum, SOC 2 cert. Found: MSA (executed, current), security addendum (executed), SOC 2 (expired 3 months ago), DPA (missing). Verdict: gaps. Gap analysis: DPA missing → PII processed with no data-protection terms, severity Critical; SOC 2 expired → unverified security posture, severity High. Actions: obtain and execute DPA (owner: privacy, by month-end), request renewed SOC 2 (owner: security, 2 weeks).

## Pitfalls
- **Checking one system.** The DPA may live in procurement while the MSA is in the repository; miss a source, miss a document.
- **Marking "present" without checking executed/current.** An unsigned or superseded draft is not coverage.
- **Ignoring expiry dates.** A current-looking agreement that lapses next month is a pending gap.
- **Missing the data-driven gaps.** No DPA/BAA where personal or health data flows is the exposure that matters most.

## Output format
```
Vendor / service / criticality / data touched:
Coverage verdict: covered | gaps | not covered
Agreement table:
  | Document | Expected | Found | Status | Expiry |
Gap analysis:
  | Item | Exposure | Severity |
Expiring / auto-renew alerts:
Actions to close gaps:
  | Action | Owner | Deadline |
```

## Required-document matrix
Match the vendor's relationship and data profile to the documents that must exist. A vendor can trigger several rows at once — collect every document whose trigger fires.

| Relationship / data type | Required documents | Trigger |
|---|---|---|
| Any vendor | MSA or signed order form; W-9 (or W-8 for foreign) / tax form; insurance COI | Any paid engagement — services or goods |
| Processes personal data | DPA with Art. 28 processor terms; SCCs (+ transfer impact assessment) for cross-border transfer | Any PII of EU/UK residents → DPA + Art. 28; transfer outside EEA/UK → SCCs |
| Processes health data (US HIPAA) | Business Associate Agreement (BAA) | Any PHI touches the vendor → BAA signed **before** data flows |
| Handles payment card data | PCI-DSS Attestation of Compliance (AOC); responsibility matrix | Vendor stores/processes/transmits cardholder data |
| Business-critical / hosts your data | SOC 2 Type II report; security addendum; pen-test summary; BCP/DR plan | Vendor hosts your data or is single-source critical to operations |
| High spend | Board/finance approval record; detailed SOW | > $100k/yr, or single-source critical → SOC 2 Type II + exec approval |
| Uses subprocessors | Subprocessor list; flow-down obligations in the DPA | Vendor delegates any processing of your data downstream |

## Severity rubric for gaps

| Gap | Severity | Why |
|---|---|---|
| Missing DPA where PII flows | Critical | Personal data processed with no data-protection terms — direct regulatory (GDPR/CCPA) exposure |
| Missing BAA where PHI flows | Critical | HIPAA violation the moment PHI is shared; per-record penalties, no cure |
| Expired SOC 2 | High | Security posture unverified; renewal lapse often signals control drift |
| Missing / expired insurance COI | High | No financial backstop if the vendor causes loss or breach |
| Unsigned MSA while services are live | High | No enforceable terms, liability caps, or IP protection governing live work |
| Expired MSA still transacting | High | Operating on lapsed terms; auto-renew or hold-over ambiguity, weakened enforceability |
| Missing SOW on active work | Medium | Scope, deliverables, and price undefined — disputes and scope creep |
| No subprocessor list | Medium | Can't verify or object to downstream data recipients; DPA flow-down unconfirmed |
| Missing W-9 | Low | Tax-reporting/paperwork gap; no operational or data risk |

## Reference
- **Where each document lives.** MSAs/order forms and SOWs sit in the contract repository or with procurement; DPAs and BAAs often land with legal/privacy or security; SOC 2 reports, pen-test summaries, and security addenda live with the security team; COIs and W-9s usually sit in finance/AP. Check every relevant system — a document absent from the repository may simply live elsewhere.
- **What "current / executed" really means.** A document counts only if it is fully countersigned by both parties (not a draft or an unsigned PDF), the version matches the approved final redline (no reverted last-minute change), and it is within its term (not expired or superseded). A signature block with one missing signature is not coverage.
- **Renewal-window watch.** Flag anything expiring within 90 days — MSAs, DPAs, SOC 2 reports, COIs, and any auto-renew notice deadline — so renewal or cancellation happens before the lapse, not after.
- **Cardinal rule.** Data-driven gaps (missing DPA where PII flows, missing BAA where PHI flows) outrank paperwork gaps. A missing W-9 is a Low-severity chore; a missing DPA on a vendor already processing customer PII is a Critical exposure. Rank and remediate by data risk first, paperwork second.
