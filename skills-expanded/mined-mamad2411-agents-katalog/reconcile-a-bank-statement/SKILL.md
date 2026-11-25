---
name: reconcile-a-bank-statement
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

Reconcile an accounting account to a bank or credit-card statement so the cleared balance matches the statement ending balance.

## Preconditions

- You have the official statement with ending date and ending balance.
- All known transactions for the statement period have been entered or imported.
- You can access the reconciliation tool for the account.

## Steps

1. **Open reconciliation.** Choose the bank, credit-card, or payment account to reconcile. → *Expect:* the reconciliation screen asks for statement details.
2. **Enter statement details.** Add statement ending date, ending balance, and service charges or interest if the tool asks. → *Expect:* the system shows a list of unreconciled transactions.
3. **Mark cleared deposits and credits.** Compare each statement credit to accounting records and mark matches only. → *Expect:* cleared deposits match the statement amounts.
4. **Mark cleared payments and charges.** Compare checks, card charges, fees, withdrawals, and transfers to the statement. → *Expect:* cleared payments match the statement amounts.
5. **Investigate differences.** Review missing transactions, duplicates, reversed signs, timing differences, and bank fees. → *Expect:* the difference moves toward zero for valid records.
6. **Finish the reconciliation.** Complete only when the difference is exactly zero. → *Expect:* the system generates a completed reconciliation or report.
7. **Save the report.** Store the reconciliation report with the statement period. → *Expect:* the reconciled period can be reviewed later.

## Decision points

- Difference is not zero → do not force reconciliation; find the cause.
- Transaction cleared after the statement date → leave it unreconciled for the next period.
- Bank fee or interest is missing → add the statement transaction and then clear it.
- Prior reconciliation changed → investigate before reconciling the current period.

## Failure modes & recovery

- **F1 Wrong ending balance:** detect by difference equal to statement entry error → recover by correcting the entered ending balance or date.
- **F2 Duplicate transaction:** detect by two accounting entries for one statement line → recover by deleting, voiding, or excluding the duplicate according to system rules.
- **F3 Missing transaction:** detect by statement line with no accounting match → recover by adding the correct expense, deposit, transfer, fee, or interest.
- **F4 Forced adjustment:** detect by system offering a reconciliation adjustment → recover by canceling and resolving the underlying mismatch.

## Verification

The reconciliation difference is zero, the account shows reconciled through the statement ending date, and the saved reconciliation report matches the official statement ending balance.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks uses Reconcile; Xero uses Reconcile and Bank statements; generic tools may call this Close statement or Match statement.
- `us`: keep reconciliation reports with bank statements for audit support and bookkeeping review.

## Safety & privacy

Medium risk because reconciliation locks in financial records and may hide errors if forced. Use official statements and avoid downloading bank files to unsecured devices.
