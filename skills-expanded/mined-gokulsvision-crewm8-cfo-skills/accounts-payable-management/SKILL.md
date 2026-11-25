---
name: accounts-payable-management
description: Manages the full accounts payable workflow including vendor invoice intake, approval routing, payment scheduling, vendor reconciliation, AP aging tracking, and DPO optimization. Use when the user mentions paying vendor invoices, scheduling payments, managing AP aging, reconciling vendors, approving invoices for payment, or asks about accounts payable workflows and vendor payment strategies.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, accounts-payable, vendors, payments, ap-aging]
related_skills:
  - transaction-processing
  - ledger-management
  - cash-forecasting
  - working-capital-optimization
  - bank-reconciliation
inputs_required:
  - invoice-stack
  - vendor-master-list
  - current-ap-aging-report
  - cash-position-forecast
deliverables:
  - ap-aging-summary
  - payment-run-proposal
  - flagged-items-report
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Accounts Payable Management

## Purpose

Every dollar the company owes to vendors must be managed — from invoice receipt through approval, payment scheduling, and reconciliation. This skill ensures the right amount is paid to the right vendor at the right time, optimizing cash without damaging vendor relationships. Without it, invoices get lost, DPO suffers, and vendor trust erodes.

## When to Use

- "Pay these vendor invoices"
- "What's our AP aging look like?"
- "Schedule this week's payments"
- "Reconcile this vendor's account"
- "Approve these invoices for payment"
- "What's our DPO and how can we improve it?"

## Inputs Required

1. **Invoice stack** — PDFs, email bodies, or a CSV listing: vendor name, invoice number, date, amount, due date, line items.
2. **Vendor master list** — names, payment terms, banking details.
3. **Current AP aging report** — if available; if not, build one from the ledger.
4. **Cash position / forecast** — from `cash-forecasting` skill to time payments.

## Quick Reference

| Metric / Concept | Definition | Why It Matters |
|-----------------|-----------|---------------|
| DPO (Days Payable Outstanding) | (AP balance / COGS) × Days in period | Measures how long you hold cash before paying vendors. Target: 30-45 days |
| 2/10 Net 30 | 2% discount if paid within 10 days, otherwise full amount due in 30 | ~36% annualized return — always take the discount |
| AP Turnover | COGS / Average AP balance | How frequently you pay vendors. Higher = faster payment cycle |
| Aging Bucket | Current, 1-30, 31-60, 60+ days past due | Surfaces which invoices are at risk of late fees or service interruption |
| Payment Run | Batched payments grouped by vendor and due date | Reduces transaction fees and reconciliation effort |

## Procedure

### 1. Invoice Intake & Validation

- Extract from PDF/email: vendor name, invoice number, invoice date, due date, amount, line items.
- Validate:
  - Invoice number is not a duplicate of one already paid/posted.
  - Amount matches the PO or contract (if available).
  - Vendor exists in the vendor master.
- Flag if: no PO match, amount mismatch > $50, no vendor on file, past due immediately.

### 2. Approval Routing

- **< $1,000** → Department manager approval.
- **$1,000 – $10,000** → Department manager + CEO/COO.
- **> $10,000** → Full approval chain including CFO review.
- Track approval status per invoice: `Pending | Approved | Rejected | Query`.

### 3. Payment Scheduling

- Sort all approved invoices by due date.
- Group by vendor (one payment run per vendor per week, unless urgent).
- Recommend payment dates using these rules:
  - Pay net-30 on day 28, never early without a discount incentive.
  - Pay net-15 on day 13.
  - If the vendor offers a 2/10 net 30 discount, always recommend paying within the discount window — it's an ~36% annualized return.
  - Stretch payments when cash is tight but never > 15 days past due without a conversation.

### 4. Payment Execution (review-only)

- Prepare a payment run summary: list of vendors, amounts, bank accounts to debit, total cash outflow.
- **Do not execute** — present for human approval.
- Once approved, record payments into the ledger.

### 5. Vendor Reconciliation

- Monthly: pull the vendor statement, match to the AP subledger.
- Flag any unmatched items.
- Resolve discrepancies: missing invoices, duplicate payments, credit notes not applied.

## Output Format

**AP Aging Summary:**

| Aging Bucket | Count | Total |
|---|---|---|
| Current | 34 | $82,400 |
| 1-30 days | 5 | $12,100 |
| 31-60 days | 2 | $3,200 |
| 60+ days | 0 | $0 |

**Payment Run Proposal:**

| Vendor | Invoice # | Due Date | Amount | Recommend Pay Date |
|---|---|---|---|---|
| AWS | INV-8922 | 2026-05-01 | $3,421 | 2026-04-28 |
| Deel | INV-4412 | 2026-05-05 | $1,200 | 2026-05-02 |

**Flagged Items:**
- Duplicate invoice numbers
- Vendors with missing W-9/W-8BEN
- Approaching-credit-limit vendors

## Done Criteria

The skill is complete when:
1. All invoices are extracted, validated, and routed for approval
2. A payment run proposal is prepared with recommended payment dates
3. DPO is calculated and trend is noted
4. Vendor reconciliation is completed with all discrepancies flagged
5. The payment run is presented for human approval (not auto-executed)
6. AP aging is summarized with aging buckets and totals

## Pitfalls

- **Paying all invoices the day they arrive**: Paying net-30 invoices on day 1 destroys DPO and trains vendors to expect instant payment. Pay near the due date unless a discount incentive exists
- **Approving without PO/contract match**: Rubber-stamping invoices that don't match a purchase order or signed contract. Even a $200 mismatch on a recurring SaaS invoice compounds monthly — validate every time
- **One payment run per invoice**: Running individual wires for every invoice instead of batching by vendor weekly. Transaction fees and reconciliation effort explode at scale
- **Ignoring vendor statement discrepancies**: Assuming the AP subledger is correct and the vendor statement is wrong without investigating. Vendors catch billing errors the company misses — investigate every mismatch
- **Stretching payments silently**: Delaying payments beyond terms without communicating with the vendor. A 2-minute "cash is tight, can we pay on the 45th?" email preserves the relationship; a surprise non-payment burns it

## Verification

Are all invoices in the payment run validated against the vendor master? Is DPO calculated and compared to the target range? Has the 2/10 net 30 discount been checked for each qualifying invoice? Is the payment run presented for human approval rather than auto-executed? Are all vendor reconciliation discrepancies documented?

## Example

**Example 1: Weekly Payment Run**
> User: "Schedule this week's vendor payments — here are the 18 approved invoices"

→ You compile the invoices, sort by due date, group by vendor (4 vendors across 18 invoices), recommend payment dates using the net-30-pay-on-28 rule, flag one 2/10 net 30 discount opportunity ($1,200 invoice, $24 discount pays $1,176 if paid within 10 days — ~36% annualized return), and present the payment run proposal for human approval with total cash outflow noted.

**Example 2: Vendor Reconciliation**
> User: "AWS sent their quarterly statement — reconcile it against our AP"

→ You pull the statement against the AP subledger, match all regular monthly invoices, flag one $2,100 invoice on the vendor statement that isn't in the subledger (possibly sent to a different billing contact), and present the reconciliation with the unmatched item for investigation.
