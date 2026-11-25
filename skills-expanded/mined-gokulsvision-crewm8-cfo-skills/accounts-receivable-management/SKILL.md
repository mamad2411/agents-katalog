---
name: accounts-receivable-management
description: Manages the full accounts receivable workflow including customer invoicing, payment collection and matching, DSO calculation and trend analysis, AR aging reports, collections escalation, and bad debt reserve recommendations. Use when the user mentions invoicing customers, collecting payments, tracking DSO, AR aging analysis, collections follow-up, reconciling customer payments, or asks about accounts receivable workflows and cash collection strategies.
version: 2.0.0
author: Crewm8
maintainer: Gokul (github.com/gokulb20)
license: MIT
homepage: https://crewm8.ai
tags: [cfo, finance, accounts-receivable, invoicing, collections, dso]
related_skills:
  - transaction-processing
  - ledger-management
  - cash-forecasting
  - working-capital-optimization
  - revenue-forecasting
inputs_required:
  - customer-contract-data
  - existing-ar-aging
  - payment-history
  - customer-master
deliverables:
  - ar-aging-dashboard
  - dso-trend-report
  - collections-escalation-plan
compatible_agents: [hermes, claude-code, droid, cursor, windsurf, openclaw, openai, generic]
---

# Accounts Receivable Management

## Purpose

Every dollar customers owe must be managed — from issuing invoices through payment collection, DSO tracking, aging analysis, and collections escalation. This skill ensures the company gets paid on time, minimizes bad debt, and keeps cash flowing. Without it, invoices go unpaid, DSO balloons, and the company runs cash-constrained unnecessarily.

## When to Use

- "Invoice this customer / send invoices"
- "What's our AR aging / who hasn't paid?"
- "Follow up on late payments / collections"
- "What's our DSO?"
- "Reconcile customer payments"
- "How can we speed up cash collections?"

## Inputs Required

1. **Customer contract / sales data** — customer name, billing terms, amount, frequency, start date.
2. **Existing AR aging** — if available from the ledger.
3. **Payment history** — Stripe/bank records for payment matching.
4. **Customer master** — entity names, billing contacts, payment terms.

## Quick Reference

| Metric / Concept | Definition | Why It Matters |
|-----------------|-----------|---------------|
| DSO (Days Sales Outstanding) | (AR balance / Revenue in period) × Days in period | How fast customers pay. Good: < 30 days SaaS, < 45 enterprise |
| AR Aging | AR grouped by days past due (0-30, 31-60, 61-90, 90+) | Surfaces which accounts are at risk of non-payment |
| Collections Escalation | Automated outreach timeline based on days past due | Ensures consistent follow-up without manual tracking |
| Bad Debt Reserve | % of AR set aside for uncollectible accounts | Required for accurate financial statements (typically 1-3% for SaaS) |
| Early Payment Discount | Incentive for customers to pay before net terms | Accelerates cash inflows at a known cost |

## Procedure

### 1. Invoice Generation

- For each invoice to issue, confirm:
  - Customer name and billing entity match.
  - Amount matches the contract/SOW/order.
  - Payment terms (net 15, net 30, upfront, milestone).
  - Invoice number is sequential and unique.
  - Bill-to email/address is correct.
- Draft the invoice. Present for review before sending.
- Post to AR subledger upon issuance.

### 2. Payment Collection & Matching

- Monitor incoming payments (bank feed, Stripe).
- Match each payment to an open invoice:
  - Exact match on amount → auto-apply.
  - Partial payment → apply and flag remaining balance.
  - Overpayment → apply and flag credit.
  - No match → flag for investigation.
- Record payment date for DSO calculation.

### 3. AR Aging Analysis

Calculate and present:

| Customer | 0-30 days | 31-60 days | 61-90 days | 90+ days | Total |
|---|---|---|---|---|---|
| Acme Corp | $10,000 | $0 | $0 | $0 | $10,000 |
| Beta Inc | $5,000 | $5,000 | $0 | $0 | $10,000 |
| Gamma LLC | $0 | $0 | $2,000 | $8,000 | $10,000 |

### 4. DSO Calculation

- **DSO** = (AR balance / Revenue in period) × Days in period
- Calculate trailing 3-month DSO and trend.
- **Good**: DSO < 30 days for monthly-billed SaaS. DSO < 45 for enterprise.
- **Warning**: DSO climbing > 10 days quarter-over-quarter.
- **Critical**: DSO > 60.

### 5. Collections Escalation

| Days Past Due | Action |
|---|---|
| 1-7 | Auto-reminder email (friendly) |
| 8-14 | Second reminder + statement |
| 15-30 | Personal email from account owner |
| 31-60 | Phone call + flag to CEO if strategic account |
| 60+ | Formal demand letter + pause service (if contract allows) |
| 90+ | Escalate to legal / collections agency |

- Track collections notes per customer.

## Output Format

**AR Aging Dashboard:**
- Total AR balance
- DSO (current and trend)
- % of AR in each aging bucket
- Top 5 past-due customers with amounts
- Bad debt reserve recommendation (typically 1-3% of AR for SaaS)

## Done Criteria

The skill is complete when:
1. All invoices are drafted and presented for review before sending
2. Incoming payments are matched to open invoices (exact, partial, or unapplied)
3. AR aging report is generated with aging buckets and totals
4. DSO is calculated with trailing 3-month trend analysis
5. Collections escalation plan is drafted for all past-due accounts
6. Bad debt reserve recommendation is calculated and documented

## Pitfalls

- **Delaying invoice issuance until "things settle"**: Waiting for the end of the month or until a contract amendment is finalized before invoicing. Every day of billing lag adds a day to DSO — invoice on day 1 and true-up later if needed
- **One-size-fits-all collections cadence**: Sending the same automated reminder schedule to a $50k enterprise customer and a $200 SMB account. Enterprise accounts need personal outreach after day 15; SMB can go fully automated
- **Counting disputed invoices in DSO**: Including invoices the customer is actively disputing in the AR balance used for DSO calculation. Disputed amounts inflate DSO and mask the real collections performance — quarantine disputes
- **Ignoring partial payments as noise**: Writing off small underpayments ($50 here, $200 there) without investigation. These are often intentional — a customer testing whether you notice — and they compound across billing cycles
- **Offering annual discounts without modeling revenue recognition impact**: Giving 15% off for annual prepay without accounting for the deferred revenue waterfall. The cash benefit is real, but the revenue recognition complexity and SaaS metrics distortion need equal consideration

## Verification

Is every invoice validated against the contract (amount, terms, billing entity)? Are all payment matches accounted for (exact, partial, overpayment, no match)? Is DSO calculated correctly and trended against the prior quarter? Are disputed invoices quarantined from DSO calculation? Is the collections escalation plan appropriate for each customer's size and relationship?

## Example

**Example 1: AR Health Check**
> User: "How's our AR looking right now?"

→ You pull the AR aging, calculate DSO (32 days, up from 27 last quarter — warning threshold), identify the top 3 past-due accounts (Beta Inc at $5,000 aged 31-60, Gamma LLC at $8,000 aged 90+), recommend a 2% bad debt reserve ($2,400 on $120k total AR), and note that DSO is trending up due to two enterprise accounts paying slower than terms.

**Example 2: Collections Run**
> User: "Run collections follow-ups — send reminders for everything past due"

→ You triage 7 past-due accounts into the escalation framework: 3 accounts at days 1-7 (auto-friendly reminder drafted), 2 accounts at days 8-14 (second reminder with statement attached), 1 account at day 18 (personal email draft for the account owner), 1 account at day 65 (formal demand letter draft + service-pause recommendation flagged for CEO review). All communications drafted, none sent without human approval.
