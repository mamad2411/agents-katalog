---
name: send-a-quote-for-approval
domain: business
locale: [generic]
interface: web
difficulty: intermediate
est_time: 15min
risk: low
prerequisites: []
status: draft
last_verified: 2026-08-17
---

## Goal

Submit a sales quote for internal approval with complete pricing, discount, customer, and deal context.

## Preconditions

- A draft quote connected to a CRM deal or opportunity.
- Current products, quantities, prices, discount, terms, and customer information.
- Knowledge of approval thresholds and approvers.

## Steps

1. **Open the quote.** Navigate from the deal to the quote, CPQ record, or quoting tool. → *Expect:* quote lines and approval controls are visible.
2. **Validate quote details.** Check account, billing entity, products, quantities, currency, term dates, taxes, and expiration date. → *Expect:* commercial fields match the intended offer.
3. **Check pricing policy.** Compare discount, margin, payment terms, and nonstandard terms against approval rules. → *Expect:* approval requirement is clear.
4. **Add approval context.** Write the business case, competitor context, customer deadline, discount rationale, and any legal or finance notes. → *Expect:* approvers have enough context to decide.
5. **Submit for approval.** [BRANCH: Salesforce | HubSpot | generic] use Submit for Approval in Salesforce or CPQ; use HubSpot quote approval workflow if enabled; in another CRM, start the configured approval workflow. → *Expect:* quote status changes to pending approval.
6. **Notify the deal team.** Mention or message the owner, manager, or deal desk if separate notification is expected. → *Expect:* relevant internal owners know the quote is pending.
7. **Track approval status.** Review workflow status and respond to approver questions. → *Expect:* the quote has a visible pending, approved, or rejected state.

## Decision points

- If pricing is within self-serve authority → document rationale and skip formal approval if policy allows.
- If customer deadline is urgent → mark priority and notify approvers through the approved channel.
- If quote terms are incomplete → fix the quote before submitting.

## Failure modes & recovery

- **F1 Approval rejected:** detect rejected status or approver comment → revise quote or rationale and resubmit if appropriate.
- **F2 Missing approver:** detect workflow stuck with no approver → escalate to sales ops or deal desk.
- **F3 Wrong quote version:** detect approval submitted for an obsolete draft → withdraw if possible and submit the correct version.

## Verification

The quote is in pending, approved, or rejected approval status with complete quote details, rationale, and approver trail.

## Variations

- CPQ workflow: approval may be triggered automatically by discount or term fields.
- Deal desk review: attach supporting emails, pricing model, or order form draft.
- Renewal quote: include current contract, renewal baseline, and uplift rationale.

## Safety & privacy

Quotes contain confidential pricing and customer terms. Share only through approved internal systems and do not send an unapproved quote externally.
