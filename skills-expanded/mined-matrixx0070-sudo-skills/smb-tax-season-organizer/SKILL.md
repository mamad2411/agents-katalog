---
name: smb-tax-season-organizer
version: 1.0.0
description: Organize tax-season materials for a quarterly estimate or year-end 1099 and produce an accountant handoff packet.
author: matrixx0070
tags: [tax, organization, quarterly, 1099, accountant, handoff]
capabilities: []
---

# Tax Season Organizer

## When to use
Run this ahead of a quarterly estimated-tax deadline or at year-end 1099 time, when the owner needs their numbers and documents gathered into something an accountant can use.

**Not for:** filing or tax advice (this organizes; the accountant advises and files); sending the packet externally without owner approval; bookkeeping cleanup (use smb-month-end-prep).

## Method
1. **Confirm the mode.** Quarterly estimate or year-end 1099 packet, and the tax period.
2. **Pull income and expense totals.** From connected accounting or bank data, categorized by common tax buckets. Flag gaps and uncategorized items for the owner to resolve.
3. **For quarterly mode.** Summarize period income, deductible expenses, and a rough estimate range, clearly labeled as an estimate to confirm with the accountant.
4. **For 1099 mode.** List contractors paid over the reporting threshold; check for missing W-9 details (name, TIN, address). Decision point: flag incomplete records for collection rather than filing partial data.
5. **Assemble the handoff packet.** Organized summary, supporting-document checklist, and open questions.
6. **Deliver for review.** To the owner first; the owner approves any external send to the accountant.

## Example
Year-end 1099 mode. Contractors over threshold: Jordan Lee $8,400 (W-9 complete), Sam Diaz $2,100 (missing TIN — flag to collect), Riya Patel $640 (under $600? no, over — include). Income/expense summary attached by category. "Needs your attention": Sam's TIN, 3 uncategorized expenses. Packet outline + document checklist assembled; delivered to the owner to review before it goes to the accountant.

## Pitfalls
- Filing or preparing 1099s with a missing TIN instead of flagging it for the owner to collect.
- Presenting the estimate range as a final figure — it's for accountant confirmation only.
- Miscategorizing expenses into wrong tax buckets, which the accountant then has to unwind.
- Sending the packet to the accountant before the owner has reviewed and approved it.

## Output format
- **Mode + period header.**
- **Categorized income/expense summary** (or contractor table for 1099).
- **"Missing or needs your attention"** list.
- **Handoff packet outline** + document checklist.
- **Disclaimer:** figures are for accountant review, not filed advice; owner approves any external send.

## Reference

### Key dates at a glance
| Date | What |
|------|------|
| Jan 15 | Q4 prior-year estimated payment due |
| Jan 31 | 1099-NEC to contractors **and** IRS; W-2s to employees + SSA; Form 940 |
| Mar 15 | S-corp (1120-S) and partnership (1065) returns due |
| Apr 15 | Sole prop (Schedule C) + C-corp returns; Q1 estimate due |
| Jun 15 / Sep 15 / Jan 15 | Q2 / Q3 / Q4 estimates |
Confirm state deadlines separately; several differ.

### Document-gathering checklist (what to pull before handoff)
**Income:** sales reports by channel, merchant/payment-processor statements, 1099-Ks received, other income.
**Expenses (by tax bucket):** advertising, contract labor, supplies, rent, utilities, insurance, software/subscriptions, professional fees, travel, meals, vehicle/mileage, bank + merchant fees, home office.
**Accounts:** all bank + credit-card statements reconciled; loan statements (interest vs principal split).
**Assets:** equipment/asset purchases with dates + amounts (depreciation / Section 179).
**Payroll:** 941s, W-2/W-3, retirement contributions.
**Contractors:** W-9 on file + total paid per payee.
**Reference:** prior-year return, record of estimated payments already made.

### Tax-bucket mapping cheatsheet (categorize into these, not vague labels)
- "Facebook/Google ads" → **Advertising**
- "Freelancer / subcontractor" → **Contract labor** (and 1099 check)
- "Zoom, Adobe, QuickBooks" → **Software/subscriptions** (often under Office/Other)
- "Client lunch" → **Meals** (generally 50% deductible)
- "Gas / mileage" → **Car & truck** (standard mileage vs actual — flag for accountant)
- "Home internet, portion of rent" → **Home office** (needs sq-ft + business-use %)
Miscategorization forces the accountant to unwind it — flag uncertainties instead of guessing.

### Quarterly-estimate range (label as estimate only)
Rough taxable income = period income − deductible expenses. Apply the owner's effective rate (or safe harbor: 100% of last year's tax, 110% if AGI > $150k, split across remaining quarters). Present as a **range**, clearly marked "confirm with accountant." Remember self-employed owners also owe **15.3% SE tax** on net earnings — surface it so the estimate isn't understated.

### 1099 threshold + W-9 rules
- File **1099-NEC** for each unincorporated contractor paid **$600+** for services during the year.
- **Aggregate** multiple small payments to the same payee — three $250 payments cross the threshold.
- No 1099 for corporations (except legal fees) or for goods.
- **W-9 required fields:** legal name, business name (if any), TIN/EIN, address, tax classification. Missing any → flag for collection; never file partial data.
- Recipient + IRS copies both due **Jan 31**.

### Handoff packet outline
1. Cover summary (business, entity type, period).
2. Categorized income/expense summary (or contractor table in 1099 mode).
3. Reconciliation status per account.
4. "Missing or needs your attention" list.
5. Supporting-document index.
6. Open questions for the accountant.

### Boundary
This organizes; it does not advise or file. Deliver to the **owner first**; the owner approves any external send to the accountant. All figures are for professional review, not filed advice.
