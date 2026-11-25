---
name: reconcile-a-payout-report
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 30min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Match a payment processor payout report to orders, refunds, fees, and the bank deposit.

## Preconditions

- You have access to the payment processor, store reports, and bank deposit record.
- You know the payout date range, currency, and account being reconciled.
- You have a spreadsheet or accounting system for recording differences.

## Steps

1. **Open the payout.** Find the processor payout by date, amount, currency, and bank account. → *Expect:* payout summary and transaction list are visible.
2. **Export transaction detail.** Download orders, refunds, disputes, fees, taxes, and adjustments for the payout. → *Expect:* a detail report is available for reconciliation.
3. **Match gross sales.** Compare order sales in the payout to store order reports for the same period. → *Expect:* sales totals match or differences are listed.
4. **Match deductions.** Compare refunds, chargebacks, processor fees, reserves, and adjustments. → *Expect:* net payout calculation explains deductions.
5. **Match bank deposit.** Compare processor net payout to the bank deposit amount and settlement date. → *Expect:* the bank deposit equals the payout or has a documented timing difference.
6. **Investigate variances.** Drill into missing orders, duplicate refunds, currency conversion, pending settlements, or fees. → *Expect:* every variance has a cause or owner.
7. **Record reconciliation.** Enter the matched totals, variance notes, and supporting report links in accounting records. → *Expect:* the payout is marked reconciled or pending with reasons.

## Decision points

- If the bank deposit has not arrived → mark as timing difference and check again after expected settlement.
- If variance is material → escalate to finance before closing the period.
- If currency conversion applies → reconcile in both transaction currency and deposit currency.

## Failure modes & recovery

- **F1 Date mismatch:** detect transactions outside the payout window → use settlement date, not order date, for payout matching.
- **F2 Missing refund:** detect store refund not in payout → check if it settled in another payout.
- **F3 Unexplained fee:** detect fee category not recognized → verify processor fee schedule or ask finance.

## Verification

The payout net amount matches the bank deposit or has documented variances with owners, and supporting reports are attached or linked.

## Variations

- Marketplace payout: include commissions, advertising fees, and marketplace reserves.
- Multiple currencies: reconcile each currency separately before conversion.
- Daily close: use smaller date windows and carry open differences to the next payout.

## Safety & privacy

Medium risk because payout reports include financial and customer transaction data. Store exports securely, restrict access, and avoid sharing full payment identifiers.
