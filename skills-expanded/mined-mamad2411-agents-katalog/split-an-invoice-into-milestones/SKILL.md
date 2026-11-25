---
name: split-an-invoice-into-milestones
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

Create milestone invoices so a project is billed in agreed stages instead of as one full invoice.

## Preconditions

- The contract or quote defines milestones, amounts or percentages, due dates, and acceptance criteria.
- The customer, project, tax treatment, and payment terms are known.
- You know whether a deposit or prior invoice has already been paid.

## Steps

1. **Review the billing schedule.** List each milestone, trigger, amount, due date, and remaining balance. → *Expect:* the total across milestones equals the contract amount.
2. **Open the project or original quote.** Find the source estimate, project, or customer record. → *Expect:* project billing context is visible.
3. **Create the first milestone invoice.** Add line items for the milestone deliverable, percentage, deposit, tax, and payment terms. → *Expect:* the invoice total matches the first milestone.
4. **Label the milestone clearly.** Include milestone number, service period, acceptance trigger, and remaining schedule in notes. → *Expect:* the customer can identify what the invoice covers.
5. **Save or send based on readiness.** [BRANCH: draft | send] save as draft if approval is pending, or send if the milestone is earned and approved. ⚠️ *Irreversible:* sending requests payment, so confirm milestone completion and amount before sending. → *Expect:* the invoice is draft or sent with the correct status.
6. **Create future milestone records.** Draft future invoices or set reminders for later milestones without sending early. → *Expect:* the remaining billing schedule is tracked.
7. **Update the project balance.** Record billed, paid, and remaining amounts in the project or customer notes. → *Expect:* the project shows what has been billed and what remains.

## Decision points

- Milestones are percentage-based → calculate percentages from the approved contract total.
- Customer requires acceptance before billing → keep invoice in draft until written acceptance.
- Deposit was collected → apply it to the correct milestone or final invoice.
- Scope changed → issue a change order before changing milestone amounts.

## Failure modes & recovery

- **F1 Milestones do not total contract:** detect by sum of milestone invoices differing from contract → recover by adjusting drafts before sending.
- **F2 Milestone billed too early:** detect by missing acceptance or incomplete deliverable → recover by voiding unsent drafts or issuing a credit if sent.
- **F3 Deposit applied twice:** detect by contract balance too low or negative → recover by removing the duplicate credit.
- **F4 Tax differs by milestone:** detect by mixed taxable and nontaxable deliverables → recover by setting tax per line item.

## Verification

Milestone invoices or drafts total the contract amount, each milestone has a clear description and due trigger, and the project balance shows billed, paid, and remaining amounts.

## Variations

- [BRANCH: QuickBooks | Xero | generic] QuickBooks may convert estimates to progress invoices; Xero may require separate invoices; generic tools may use project billing schedules.
- `us`: tax timing can depend on when taxable goods or services are invoiced, delivered, or paid.

## Safety & privacy

Medium risk because milestone invoices affect cash flow and contractual obligations. Do not bill before the agreed trigger unless the customer has approved the change.
