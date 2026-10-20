---
name: record-a-customer-payment
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

Record a customer payment against the correct invoice so the customer balance and deposits are accurate.

## Preconditions

- The customer payment has been received or confirmed by the payment processor.
- The related invoice, customer, amount, date, and payment method are known.
- You know which bank, clearing, or undeposited funds account should receive the payment.

## Steps

1. **Open receive-payment.** Go to sales, invoices, customers, or payments and choose receive or record payment. → *Expect:* a payment form is visible.
2. **Select the customer.** Choose the paying customer and review open invoices. → *Expect:* the relevant unpaid invoice is listed.
3. **Enter payment details.** Add payment date, amount, method, reference number, and deposit account. → *Expect:* the payment details match the bank, check, card, or gateway record.
4. **Apply to invoice.** Select the invoice or invoices the payment covers and allocate partial amounts if needed. → *Expect:* the applied amount equals the received payment.
5. **Handle overpayment or short payment.** [BRANCH: exact | partial | overpayment] close exact payments, leave partial balance open, or record customer credit for overpayment. → *Expect:* customer balance reflects the remaining amount correctly.
6. **Save the payment.** Save the record without duplicating any payment imported from the bank feed. → *Expect:* the invoice status changes to paid or partially paid.
7. **Match deposit if needed.** Match the saved payment to the bank feed or deposit batch. → *Expect:* the bank transaction links to the payment record.

## Decision points

- Payment came through an online processor → check whether it was already recorded automatically.
- One payment covers multiple invoices → allocate the total across each invoice.
- Fees were deducted by processor → record gross payment and separate processing fee where appropriate.
- Customer paid the wrong amount → leave balance open, issue credit, or refund according to policy.

## Failure modes & recovery

- **F1 Duplicate payment:** detect by invoice overpaid or two payment records for one deposit → recover by deleting or voiding the duplicate according to system rules.
- **F2 Applied to wrong invoice:** detect by incorrect invoice paid and intended invoice still open → recover by unapplying and reapplying the payment.
- **F3 Wrong deposit account:** detect by payment not matching bank feed → recover by changing deposit account or moving from undeposited funds.
- **F4 Net recorded instead of gross:** detect by processor fee missing from reports → recover by recording gross receipt and separate fee.

## Verification

The customer payment is linked to the correct invoice, the invoice status and remaining balance are correct, and the payment is matched or ready to match to the deposit account.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks uses Receive payment and Undeposited Funds; Xero uses Add payment on invoice; generic tools may use Mark paid or Record payment.
- `us`: merchant fees, chargebacks, and 1099-K reporting can make processor deposits differ from customer invoice payments.

## Safety & privacy

Medium risk because payment records affect cash, revenue, and customer balances. Do not store full card or bank credentials in notes.
