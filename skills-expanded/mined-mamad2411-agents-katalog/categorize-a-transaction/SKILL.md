---
name: categorize-a-transaction
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 2min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Assign a bank or card transaction to the correct accounting category so reports and reconciliation stay accurate.

## Preconditions

- The bank or credit-card feed transaction is visible.
- You know the vendor, customer, business purpose, and whether the transaction matches an existing bill, invoice, payment, or expense.
- Receipt or supporting detail is available when required.

## Steps

1. **Open the transaction.** Go to banking, transactions, or bank feed and select the unmatched item. → *Expect:* transaction date, description, amount, and account are visible.
2. **Check for a match first.** Look for an existing invoice payment, bill payment, expense, transfer, or deposit that has the same amount and date. → *Expect:* you know whether to match or categorize.
3. **Choose the transaction type.** [BRANCH: expense | income | transfer | owner contribution] select the type that reflects what happened economically. → *Expect:* the form shows fields appropriate to that type.
4. **Assign the category.** Choose the account category, customer, project, class, or location if used. → *Expect:* the transaction will appear under the correct reporting line.
5. **Add memo and receipt.** Enter a short business purpose and attach support if needed. → *Expect:* a reviewer can understand the transaction later.
6. **Confirm the categorization.** Save, add, or approve the transaction. → *Expect:* the bank feed item changes to categorized, added, or matched status.

## Decision points

- Transaction matches an existing record → match instead of creating a duplicate.
- Transaction is a transfer between business accounts → use transfer, not income or expense.
- Transaction includes multiple purposes → split it across categories.
- Personal transaction appears in business account → categorize to owner draw, shareholder distribution, or due from owner according to your accountant's guidance.

## Failure modes & recovery

- **F1 Duplicate record:** detect by expense or payment appearing twice after categorization → recover by undoing the added transaction and matching it.
- **F2 Wrong income treatment:** detect by a loan, transfer, or owner contribution showing as sales → recover by recategorizing to the correct balance-sheet account.
- **F3 Missing split:** detect by one receipt containing multiple categories or taxable portions → recover by editing the transaction into split lines.
- **F4 Unknown vendor:** detect by unclear bank description → recover by checking receipt, card statement, or vendor search before approving.

## Verification

The transaction is no longer unmatched and shows the correct type, category, amount, date, account, memo, and attachment or review note.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks often uses Banking > For review; Xero uses Bank reconciliation or Cash coding; generic tools may label the action Categorize, Add, or Match.
- `us`: categories can affect deductible expenses and tax reporting, so ask an accountant before finalizing uncertain categories.

## Safety & privacy

Medium risk because categorization affects financial statements and tax reports. Do not guess on loans, owner transactions, payroll, or taxes without review.
