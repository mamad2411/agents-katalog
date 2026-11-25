---
name: issue-a-refund
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 10min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Issue a customer refund for a valid return, overpayment, cancellation, or service credit and record it against the correct sale.

## Preconditions

- The original customer payment or invoice is visible in the system.
- The refund reason, amount, method, and approval are known.
- You have confirmed whether goods were returned, service was canceled, or a credit memo is required.

## Steps

1. **Find the original sale.** Locate the invoice, receipt, order, or payment being refunded. → *Expect:* the original customer, amount, and payment method are visible.
2. **Confirm the refund amount.** Calculate full or partial refund, tax reversal, shipping, restocking fee, and any store credit. → *Expect:* the refund amount matches policy and approval.
3. **Choose the refund path.** [BRANCH: refund payment | credit memo | account credit] refund to the original method when possible, create a credit memo for invoice accounting, or leave a customer credit if agreed. → *Expect:* the system shows the chosen refund action.
4. **Enter the reason and references.** Add return authorization, cancellation note, approval name, or customer message. → *Expect:* the refund record explains why money is leaving the business.
5. **Submit the refund.** ⚠️ *Irreversible:* refunding sends money or creates a binding credit, so confirm customer, amount, and payment method before submitting. → *Expect:* the system shows refund submitted, processing, or completed.
6. **Send confirmation.** Provide the customer with amount, method, timing, and reference number. → *Expect:* the customer has written confirmation of the refund.
7. **Check accounting impact.** Confirm the refund reduced revenue, tax liability, accounts receivable, or customer credit as intended. → *Expect:* reports no longer show the refunded amount as collectible revenue.

## Decision points

- Original card is expired or closed → ask the processor whether refund to original payment route still works before using another method.
- Refund exceeds original payment → escalate for approval and document why.
- Customer wants credit instead of cash → record a customer credit and expiration terms if allowed.
- Tax was collected on the sale → reverse the tax only for the refunded taxable portion.

## Failure modes & recovery

- **F1 Wrong original transaction:** detect by customer or amount mismatch → recover by canceling only if still pending, otherwise issue a correcting charge or credit with approval.
- **F2 Processor rejects refund:** detect by failed or declined refund status → recover by checking settlement status, payment method limits, and processor rules.
- **F3 Refund recorded but not paid:** detect by accounting credit without gateway refund → recover by processing the payment refund or documenting store credit.
- **F4 Tax not reversed:** detect by sales-tax report still showing the refunded taxable sale → recover by editing the credit memo or refund tax lines.

## Verification

The refund record links to the original sale, shows the approved amount and method, has submitted or completed status, and the customer balance and reports reflect the refund.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks may use Refund receipt or Credit memo; Xero may use Credit note and cash refund; generic tools may separate payment gateway refund from accounting credit.
- `us`: sales-tax refunds usually need the taxable sale reversed in the same jurisdiction and period rules may affect reporting.

## Safety & privacy

Medium risk because funds leave the business and the action may be difficult to reverse. Never refund to a new destination without confirming anti-fraud policy and customer authorization.
