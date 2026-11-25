---
name: set-up-recurring-billing
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: medium
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Create a recurring billing schedule that automatically drafts or sends invoices for repeat work on the agreed cadence.

## Preconditions

- The customer has agreed to recurring charges, billing cadence, start date, amount, and cancellation terms.
- Stored payment authorization exists if charges will be collected automatically.
- Products, services, tax settings, and customer contact details are ready.

## Steps

1. **Open recurring billing settings.** Go to recurring invoices, repeating invoices, subscriptions, or templates. → *Expect:* a recurring billing setup form is visible.
2. **Select the customer.** Choose the customer and billing contact. → *Expect:* the schedule is tied to the correct customer.
3. **Enter recurring line items.** Add services, products, quantities, rates, discounts, and taxable status. → *Expect:* each future invoice will contain the right charges.
4. **Set the cadence.** Choose start date, frequency, end date or number of occurrences, due terms, and invoice send timing. → *Expect:* the schedule preview shows the intended billing dates.
5. **Choose collection behavior.** [BRANCH: auto-charge | auto-send | draft-only] charge saved payment automatically, send invoices automatically, or create drafts for review. → *Expect:* the schedule behavior matches the customer agreement.
6. **Add customer-facing notes.** Include contract reference, service period, cancellation terms, and support contact. → *Expect:* future invoices explain the recurring charge.
7. **Activate the schedule.** Save and enable the recurring billing rule. → *Expect:* the schedule shows active status and next invoice date.

## Decision points

- Amount changes each period → use draft-only or variable billing instead of auto-send.
- Stored payment is missing → send invoices manually until authorization is collected.
- Customer requires purchase orders → confirm whether the same PO can be reused.
- Service has a minimum term → include the term in invoice notes or the linked contract.

## Failure modes & recovery

- **F1 Wrong cadence:** detect by next invoice date or preview not matching contract → recover by editing frequency and start date before activation.
- **F2 Auto-charge not authorized:** detect by missing mandate or payment consent → recover by switching to auto-send or collecting authorization.
- **F3 Duplicate billing:** detect by active manual and recurring invoices for the same period → recover by voiding the unsent duplicate or crediting the customer.
- **F4 Tax changed:** detect by rate or nexus change before the next run → recover by updating item tax settings before invoices are generated.

## Verification

The recurring billing schedule is active with the correct customer, line items, cadence, collection behavior, next invoice date, and authorization status if auto-charge is enabled.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks uses recurring transactions; Xero uses repeating invoices; generic platforms may call this subscriptions or billing schedules.
- `us`: recurring taxable services may need rate updates when customer location or tax rules change.

## Safety & privacy

Medium risk because recurring billing can repeatedly charge customers. Keep written authorization, avoid storing payment details outside approved processors, and review schedules after contract changes.
