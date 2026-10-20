---
name: mark-a-deal-won-or-lost
domain: business
locale: [generic]
interface: web
difficulty: basic
est_time: 5min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Close a CRM deal as won or lost with accurate reason, amount, date, and handoff context.

## Preconditions

- Permission to edit and close the deal.
- Confirmed buyer decision or signed order for won deals.
- Confirmed no-decision, competitor loss, timing issue, or other reason for lost deals.

## Steps

1. **Open the deal.** Find the opportunity or deal to close. → *Expect:* current stage, amount, and close date are visible.
2. **Confirm the outcome evidence.** Check contract, purchase order, email confirmation, cancellation, or loss reason. → *Expect:* the close outcome is supported by evidence.
3. **Update final fields.** Enter final amount, close date, products, primary competitor, loss reason, or win reason as applicable. → *Expect:* required close fields are complete.
4. **Set the close stage.** [BRANCH: Salesforce | HubSpot | generic] choose Closed Won or Closed Lost in Salesforce; move to Closed Won or Closed Lost in HubSpot; in another CRM, set the terminal won or lost stage. → *Expect:* the deal shows a closed status.
5. **Add a closing note.** Summarize the outcome, reason, and any customer commitments. → *Expect:* the timeline explains why the deal closed.
6. **Trigger next process.** For won deals, start onboarding or order processing; for lost deals, set nurture or closed-lost analysis if appropriate. → *Expect:* the correct post-close workflow begins.

## Decision points

- If commercial approval is still pending → do not mark won until approval or signature is complete.
- If the buyer delayed rather than rejected → move the close date or stage instead of marking lost.
- If the deal closed won with special terms → attach or reference approved documentation.

## Failure modes & recovery

- **F1 Closed without evidence:** detect no contract, confirmation, or loss reason → reopen or correct the deal until evidence is captured.
- **F2 Wrong amount:** detect mismatch with quote or order form → update amount and products from the approved source.
- **F3 Handoff missing:** detect won deal without onboarding task → create or trigger the required handoff.

## Verification

The deal is in a terminal won or lost stage with final amount, close date, required reason fields, closing note, and appropriate post-close action.

## Variations

- Self-serve purchase: payment confirmation may be the win evidence.
- Enterprise deal: legal, finance, or approval fields may be required before close.
- Closed-lost recycle: set a future nurture date if the account remains a fit.

## Safety & privacy

Closing a deal affects revenue reporting, commissions, and customer operations. Do not mark won without reliable commercial evidence or expose contract terms outside approved systems.
