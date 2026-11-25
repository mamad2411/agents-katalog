---
name: corpl-closing-checklist
version: 1.0.0
description: Build and drive an M&A closing checklist that tracks every deliverable, signature, and condition from signing to closing with owners and status.
author: matrixx0070
tags: [corporate-legal, m&a, closing, checklist, conditions, deal-management]
capabilities: []
---

## When to use

Use this once a deal is signed (or nearing signing) to organize the path to closing: the documents to be executed, the conditions to be satisfied, the third-party consents and approvals to be obtained, and who owns each. It is the operational spine of getting a transaction closed cleanly.

**Not for:** diligence-phase issue tracking (use corpl-diligence-issue-extraction); post-closing integration (use corpl-integration-management); drafting the definitive agreement itself. The checklist tracks and organizes — it does not waive conditions or opine on whether a closing condition is legally satisfied; that judgment is counsel's.

## Method

1. **Establish deal structure and key dates.** Parties, structure (stock/asset/merger), signing date, target closing, drop-dead date.
2. **Extract closing conditions from the agreement.** List each condition precedent (regulatory approval, consents, no-MAC, bring-down of reps, delivery of certificates) with the responsible party.
3. **List every closing deliverable** by document, grouped by category (corporate authorizations, transaction documents, third-party consents, regulatory, financing, ancillary), with signatory and status.
4. **Track third-party consents and approvals** separately — these are the usual critical path. *Decision point:* if a required consent is at risk, escalate to the deal lead early; a missing material consent can block or delay closing.
5. **Assign owners and status** (open / in progress / draft circulated / executed / satisfied / waived) to every line; waivers are counsel decisions.
6. **Run to closing:** hold a pre-closing review, confirm all conditions satisfied or waived, then coordinate the closing/signature logistics (often an escrowed exchange of signature pages released on the closing call).
7. **Capture the post-closing list** (filings, funds flow confirmations, deliverable follow-ups).

## Example

Stock purchase, signed 6/1, target close 7/15. Conditions: HSR clearance (owner: antitrust counsel — in progress), landlord consent on HQ lease (owner: buyer counsel — at risk, escalated), bring-down certificate (owner: seller — draft). Deliverables tracked across 5 categories, 38 lines. Pre-closing review 7/14; signature pages held in escrow, released on the 7/15 closing call. Post-closing: state amendment filing, funds-flow confirmation.

## Pitfalls

- **Underestimating third-party consents.** They are slow and outside your control — start day one.
- **No single owner per line.** Shared ownership means no ownership.
- **Treating a waiver as an operational toggle.** Waiving a closing condition is a legal decision for counsel and the client.
- **No pre-closing bring-down check.** Reps and conditions must be confirmed current at closing, not just at signing.

## Output format

```
CLOSING CHECKLIST — <deal> (<structure>)
Signing: <date> | Target close: <date> | Drop-dead: <date>
Conditions precedent:
  | Condition | Owner | Status | Note |
Deliverables (by category):
  | # | Document | Signatory | Status |
Third-party consents / approvals (critical path):
Open risks / escalations:
Post-closing items:
Attorney sign-off before closing: <name>
```

## Reference

Standard closing categories: corporate authorizations (board/stockholder consents, secretary's certificates), transaction documents, third-party consents, regulatory approvals (e.g., HSR), financing deliverables, and ancillary agreements. Conditions precedent are read directly from the definitive agreement — do not paraphrase them loosely. Waivers, satisfaction determinations, and the closing mechanics (escrow release of signature pages) are executed under attorney supervision.
