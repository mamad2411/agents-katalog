---
name: apply-a-late-fee
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

Apply a late fee to an overdue invoice according to agreed terms and record the fee clearly for the customer.

## Preconditions

- The invoice is overdue and unpaid.
- The contract, quote, invoice terms, or policy allows a late fee.
- You know the fee amount, percentage, grace period, and any legal limits.

## Steps

1. **Open the overdue invoice.** Locate the unpaid invoice and confirm due date and open balance. → *Expect:* the invoice shows overdue status or a past due date.
2. **Check fee authority.** Review the contract, invoice terms, or customer agreement for late-fee language. → *Expect:* you can cite the basis for the fee.
3. **Calculate the fee.** Apply the fixed amount or percentage only to the eligible overdue balance after any grace period. → *Expect:* the fee amount is documented.
4. **Add the fee line.** Add a late-fee item, finance charge, or adjustment with a clear description and date. → *Expect:* the invoice total increases by the calculated fee.
5. **Save the updated invoice.** Save the revised invoice or finance charge. → *Expect:* the customer balance reflects the late fee.
6. **Notify the customer.** ⚠️ *Irreversible:* sending the updated invoice changes the collection request, so confirm the fee is allowed and accurate before sending. → *Expect:* the activity log shows the updated invoice or notice sent.

## Decision points

- Terms do not allow a fee → do not apply one; send a reminder or renegotiate terms.
- Customer has a valid dispute → pause the fee until the dispute is resolved.
- Partial payment was received → calculate the fee only on the remaining eligible balance.
- Fee may exceed legal limits → ask an accountant or attorney before charging it.

## Failure modes & recovery

- **F1 Fee not authorized:** detect by missing late-fee terms → recover by removing the fee and updating future contracts.
- **F2 Wrong balance used:** detect by fee calculated on paid or credited amounts → recover by recalculating and revising the invoice.
- **F3 Customer disputes fee:** detect by customer reply or refusal to pay → recover by citing terms or waiving with a documented approval.
- **F4 Tax applied incorrectly:** detect by late-fee line marked taxable when it should not be, or the reverse → recover by correcting tax treatment before filing.

## Verification

The overdue invoice or finance charge shows the allowed late fee amount, clear description, updated balance, and customer notification record.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks may use late fees or finance charge settings; Xero may require an added invoice line; generic tools may use adjustments.
- `us`: late-fee enforceability and maximum rates vary by state and contract type.

## Safety & privacy

Medium risk because late fees can damage customer relationships and may be regulated. Apply only fees supported by written terms and keep dispute notes private.
