---
name: smb-invoice-chase
version: 1.0.0
description: Draft overdue-invoice reminders tuned to each customer's payment history and the right tone, with a cadence plan — every message owner-approved before send.
author: matrixx0070
tags: [small-business, ar, collections, dunning, invoicing, customers]
capabilities: []
---

# Invoice Chase

## When to use
Use this when receivables are aging and the owner needs reminder messages that recover cash without damaging good relationships — tuned to how late each customer is and how they've paid before.

**Not for:** forecasting when cash will land (use smb-cash-flow) or sending anything automatically. This drafts reminders; the owner approves every one.

## Method
1. **Pull the aging list.** List overdue invoices with customer, amount, invoice date, due date, and days overdue.
2. **Read payment history.** For each customer, note typical days-to-pay, prior late episodes, and lifetime value.
3. **Segment by tone.** Decision point: sort into gentle nudge (first reminder, usually reliable), firm follow-up (repeatedly late or well past due), and escalation candidate (severely overdue or unresponsive).
4. **Draft the message.** Write each reminder with the invoice number, amount, due date, a clear pay link/next step, and tone matched to the segment — warm for good customers, firmer for chronic late payers.
5. **Set the cadence.** Recommend when to send the next touch if unpaid.
6. **Flag escalations.** Identify accounts that may need a call, payment plan, or hold.

Do not send anything directly. Present drafts for the owner to review, edit, and approve — every customer-facing message and any escalation is owner-approved.

## Example
Aging: 1-30 → 4 invoices ($6.2k); 31-60 → 2 ($3.1k); 60+ → 1 ($9k). Riverside Co. (INV-1043, $1,200, 12 days over) usually pays on time → gentle nudge: "Just a quick heads-up, INV-1043 slipped past due — pay link here, no worries if it's already on the way." Delta LLC ($9k, 63 days, third late episode) → firm + flag for a call and a possible payment plan.

## Pitfalls
- **Same tone for everyone.** Dunning a reliable customer over a 5-day slip damages a good relationship.
- **Missing the pay link/next step.** A reminder with no clear way to pay just adds friction.
- **Auto-sending.** Every message and any escalation waits for owner approval.
- **Ignoring history.** A chronic late payer needs a firmer path (call, plan, hold), not a fourth polite nudge.

## Output format
```
Aging summary: 1-30 <n>/$__ | 31-60 <n>/$__ | 60+ <n>/$__
Per invoice:
| Customer | Amount | Days over | Segment | History note |
Draft messages (one per invoice, ready to send on approval):
  <customer>: "<draft>"
Cadence plan: next touch timing if unpaid
Escalations flagged for owner: <account — why>
```

## Reference

### Dunning sequence by days overdue
A dunning ladder is a fixed cadence of escalating reminders. Anchor timing to the **due date**, and adjust the starting tone by the customer's history (reliable payers start softer, chronic-late start firmer). Owner approves every send.

| Stage | Timing | Channel | Tone | Goal |
|-------|--------|---------|------|------|
| Pre-due courtesy | Due date − 3 days | Email | Friendly, neutral | Prevent lateness; surface disputes early |
| Reminder 1 | Due + 1-7 days | Email | Warm nudge | Assume oversight |
| Reminder 2 | Due + 8-14 days | Email + SMS | Polite but clear | Create mild urgency |
| Reminder 3 | Due + 15-30 days | Email + phone call | Firm, direct | Get a commitment date |
| Final notice | Due + 31-45 days | Formal email/letter + call | Firm, consequences stated | Last step before escalation |
| Escalation | Due + 45-60+ days | Owner decision | Collections / hold / plan | Recover or contain loss |

### Message templates
Every message names the invoice number, amount, original due date, and a one-click pay path.

- **Pre-due courtesy:** "Hi {name}, a quick heads-up that invoice {#} for ${amount} is due {date}. Here's the pay link — and let me know if anything looks off."
- **Reminder 1 (gentle):** "Hi {name}, just flagging that invoice {#} (${amount}) slipped past its {date} due date — likely an oversight. Pay link here; ignore if it's already on the way."
- **Reminder 2 (clear):** "Hi {name}, invoice {#} for ${amount} is now {days} days overdue. Could you settle it this week, or reply if there's a problem I can help with? Pay link."
- **Reminder 3 (firm):** "Hi {name}, invoice {#} (${amount}) is {days} days past due and I haven't been able to reach you. Can you confirm a payment date by {date}? Happy to arrange a short plan if cash timing is the issue."
- **Final notice:** "Hi {name}, invoice {#} for ${amount} is {days} days overdue. If it isn't paid or a plan agreed by {date}, we'll pause further work/orders and refer it to {collections/next step}. I'd much rather resolve this directly."

### Segmentation cues
- **Gentle track:** first-ever slip, pays reliably (avg days-to-pay ≤ terms), high lifetime value. Protect the relationship over speed.
- **Firm track:** history of 2+ late episodes, or > 30 days over, or unresponsive to two touches.
- **Escalation track:** > 60 days, disputed and unresolved, going-out-of-business signals, or amount large enough to threaten your own runway.

### Payment-plan and prevention levers
When a customer genuinely can't pay in full, a structured plan beats a stalled balance: split into 2-4 dated installments, get it in writing, and pause the dunning clock only while payments stay on schedule (resume immediately on a miss). To prevent future aging: shorten terms for chronic-late accounts (Net-15 or deposit-upfront), add late fees to terms where enforceable, offer a small early-pay discount (e.g. 2/10 Net 30 — 2% off if paid within 10 days), and require a card on file or deposit for high-risk customers.

### Benchmarks worth watching
- **DSO (Days Sales Outstanding)** = (accounts receivable ÷ credit sales) × days in period. Healthy small-business DSO is roughly 30-45 days; trending up means collections are slipping.
- **% AR over 60 days** — keep under ~10-15% of total receivables.
- **Collection effectiveness** (collected ÷ collectible) — aim above 80%.
- **Bad-debt write-off rate** — under ~1-2% of revenue for most SMBs. Anything sustained above that means the terms and dunning cadence need tightening, not just more reminders.
