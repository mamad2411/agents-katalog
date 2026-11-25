---
name: record-an-expense
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Record a business expense with the correct vendor, amount, category, date, payment method, and receipt so books and reports stay accurate.

## Preconditions

- You can access the bookkeeping or accounting system.
- You have the receipt, invoice, card charge, or bank transaction.
- You know whether the expense is reimbursable, billable to a customer, or tax-related.

## Steps

1. **Open the expense entry form.** Go to expenses, bills, purchases, or transactions and choose new expense. → *Expect:* a blank expense form is visible.
2. **Enter the vendor and date.** Select or add the vendor and use the transaction or receipt date. → *Expect:* the expense has the correct payee and date.
3. **Enter the payment details.** Add amount, currency, payment account, payment method, and reference number if available. → *Expect:* the total matches the source document.
4. **Choose the category.** Pick the expense account that best matches the business purpose. → *Expect:* the expense will appear in the correct report line.
5. **Attach the receipt.** Upload or link the receipt, bill, or invoice image. → *Expect:* the source document is attached to the record.
6. **Mark billable or reimbursable if needed.** Assign the customer, project, employee, or reimbursement flag. → *Expect:* the expense can be billed or reimbursed later.
7. **Save the expense.** Save the entry and leave it unmatched if a bank feed transaction still needs to be matched. → *Expect:* the expense appears in the expense list or ledger.

## Decision points

- Expense was paid later by bill payment → enter it as a bill first, then record payment when paid.
- Expense is personal or mixed-use → split out only the business portion.
- Category is unclear → use a temporary uncategorized account and ask your accountant before filing taxes.
- Receipt is missing → enter the expense with a note and recover the receipt from the vendor or bank.

## Failure modes & recovery

- **F1 Duplicate expense:** detect by matching vendor, date, amount, and receipt already in the system → recover by deleting or merging the duplicate before reconciliation.
- **F2 Wrong payment account:** detect when the expense does not match the bank or card feed → recover by editing the payment account.
- **F3 Missing receipt:** detect by empty attachment field → recover by uploading the receipt or adding a note that explains why it is unavailable.
- **F4 Wrong category:** detect by review of the profit-and-loss detail → recover by recategorizing before reports are finalized.

## Verification

The expense record shows the correct vendor, date, amount, payment account, category, receipt attachment or note, and billable/reimbursable status if applicable.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks often separates Expense, Bill, and Check; Xero often uses Bills to pay or Spend money; generic tools may use Purchases or Transactions.
- `us`: keep receipts and business-purpose notes for deductible expenses, especially meals, travel, vehicle, and home-office costs.

## Safety & privacy

Medium risk because expense categories affect financial reports and taxes. Receipts may contain card numbers, addresses, or employee details, so store them only in approved systems.
