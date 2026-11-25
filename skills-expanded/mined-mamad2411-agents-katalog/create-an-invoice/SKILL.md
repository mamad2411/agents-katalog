---
name: create-an-invoice
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a complete invoice for goods or services so the customer can review what they owe and pay through the agreed channel.

## Preconditions

- You can access the invoicing or accounting system.
- The customer, billing address, line items, prices, due date, and payment terms are known.
- Tax, discount, deposit, and purchase-order details are available if they apply.

## Steps

1. **Open a new invoice.** Go to the invoices area and choose the option to create a new invoice. → *Expect:* a blank invoice form is visible.
2. **Select the customer.** Choose an existing customer or add the customer name, email, billing address, and tax details. → *Expect:* the invoice shows the correct billing recipient.
3. **Enter invoice dates and terms.** Set the invoice date, due date, payment terms, and invoice number if the system does not assign one. → *Expect:* the header shows a due date and unique invoice number.
4. **Add line items.** Enter each product or service with description, quantity, rate, discount, and taxable status. → *Expect:* subtotals match the agreed prices.
5. **Review taxes and totals.** Confirm sales tax, VAT, shipping, credits, deposits, and rounding. → *Expect:* the total due equals the amount you intend to bill.
6. **Add payment instructions.** Include online payment, bank transfer, check, or other accepted methods. → *Expect:* the customer has at least one clear way to pay.
7. **Save as a draft.** Save without sending so you can check the final preview. → *Expect:* the invoice exists in draft or unsent status.

## Decision points

- Customer needs a purchase order → add the PO number before sending.
- Work is not complete → create a quote, estimate, or milestone invoice instead.
- Deposit was already paid → apply the deposit credit before finalizing.
- Tax treatment is uncertain → pause and verify the rate or exemption status.

## Failure modes & recovery

- **F1 Wrong customer:** detect by mismatched name, email, or billing address → recover by changing the customer before sending.
- **F2 Total does not match agreement:** detect by comparing the invoice total to the contract or quote → recover by correcting quantities, rates, discounts, tax, or credits.
- **F3 Duplicate invoice number:** detect by a system warning or matching prior invoice → recover by assigning the next unused number.
- **F4 Missing payment method:** detect by preview showing no payment instructions → recover by adding the accepted payment channel.

## Verification

The invoice is saved as draft or unsent with the correct customer, invoice number, due date, itemized charges, tax, total due, and payment instructions.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks often uses Sales > Invoices; Xero uses Business > Invoices; generic tools usually label this Create invoice or New invoice.
- `us`: confirm state and local sales-tax treatment before sending taxable invoices.

## Safety & privacy

Medium risk because the invoice affects money owed and exposes customer contact details. Do not send until the customer, amount, tax, and payment destination are confirmed.
