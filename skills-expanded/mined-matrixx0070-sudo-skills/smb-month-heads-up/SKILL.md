---
name: smb-month-heads-up
version: 1.0.0
description: On the 25th, produce a next-30-day cash-flow outlook that flags the items needing owner attention before month-end.
author: matrixx0070
tags: [cash-flow, forecast, monthly, finance, planning, runway]
capabilities: []
---

# Month Heads-Up

## When to use
Run this near the 25th, or whenever the owner wants a forward look at cash before the month closes. It answers "what's coming, and what do I need to touch before the 1st?"

**Not for:** reconciling past books (use smb-month-end-prep); payroll-specific coverage (use smb-plan-payroll); actually sending reminders or moving money — this is a plan the owner acts on.

## Method
1. **Set the starting balance.** Pull current cash from connected accounting/bank data. Decision point: if nothing is connected, ask the owner for a starting balance rather than guessing.
2. **List inflows (next 30 days).** Open invoices with due dates, recurring revenue, scheduled deposits. Flag anything overdue.
3. **List outflows.** Payroll, rent, loan payments, subscriptions, taxes, known one-offs.
4. **Build a running daily balance.** Mark any day the projected balance dips below the owner's comfort floor. Decision point: if a floor breach appears, trace it to the specific bill or timing that causes it.
5. **Surface attention items.** Invoices to chase, bills to time differently, low-balance days, decisions due before the 1st — each with a suggested action and deadline.
6. **Present the outlook.** The owner approves before any invoice reminder, payment, or transfer goes out.

## Example
Start $12,000 on the 25th. Inflows: Invoice #204 $6,000 (due 2nd), retainer $3,000 (1st). Outflows: payroll $9,500 (1st), rent $2,800 (1st), SaaS $600 (3rd). Running balance dips to $2,700 on the 1st before #204 lands on the 2nd — below the owner's $4,000 floor. Attention: nudge #204 to pay by the 31st (closes the dip), or delay the $600 SaaS charge two days. Headline: projected EOM ~$8,100, low point $2,700 on the 1st.

## Pitfalls
- Assuming invoices pay on their due date; use a realistic pay date and flag chronic late payers.
- Reporting only the end-of-month balance and hiding a mid-month dip below the floor.
- Sending a reminder or moving money without owner approval — this skill plans, it doesn't act.
- Omitting irregular outflows (quarterly taxes, annual renewals) that blindside the forecast.

## Output format
- **Headline:** projected end-of-month balance + lowest point (and which day).
- **Daily table:** date | inflows | outflows | running balance (floor breaches marked).
- **"Needs your attention":** item | suggested action | deadline.
- **Approval note:** nothing that moves money or contacts a customer goes out without explicit owner approval.

## Reference

### The 30-day cash-flow model
Build a running daily balance so mid-month dips can't hide behind a healthy end-of-month number.

`Ending balance(day) = Starting balance + cumulative inflows − cumulative outflows`

- **Starting balance** — actual current cash from connected bank/accounting data (if none connected, ask the owner; don't guess).
- **Inflows** — open invoices at their *realistic* pay date (not due date), recurring revenue/retainers, scheduled deposits. Flag anything already overdue.
- **Outflows** — payroll, rent, loan payments, subscriptions, sales/payroll tax, and irregular one-offs.
- **Low point** — the lowest daily balance in the window and the day it hits, plus the specific bill/timing that causes it.

### Realistic pay-date rule
Never assume an invoice pays on its due date. Shift each expected inflow by the customer's actual behavior:
| Payer history | Assumed pay date |
|---------------|------------------|
| Reliable, pays on/before terms | Due date |
| Usually a few days late | Due + 5-7 days |
| Chronically late (2+ episodes) | Due + 15-30 days, or exclude until confirmed |
| Already overdue | Exclude from the plan until a commitment date exists; list as an attention item |

### Recurring outflows checklist (the ones that blindside a forecast)
Payroll and payroll taxes, rent/lease, loan & equipment payments, insurance, software subscriptions (watch **annual renewals**), **quarterly estimated taxes**, sales-tax remittance, merchant/processor fees, and seasonal one-offs (inventory buys, annual licenses). Missing an irregular quarterly or annual item is the top cause of a forecast that looks fine and then breaks.

### The comfort floor and breach handling
Set a **minimum cash floor** with the owner — a common rule of thumb is enough to cover one full payroll + rent cycle, or a target of 3-6 months of operating expenses as the longer-term reserve. Mark every day the projected balance dips below it. For each breach, trace the specific cause, then propose the cheapest fix first:
1. **Accelerate an inflow** — nudge a specific invoice to pay before the dip (least disruptive).
2. **Delay a discretionary outflow** — move a non-critical subscription/purchase a few days past the low point.
3. **Reschedule with a vendor** — request short terms on a large bill.
4. **Draw a buffer** — line of credit / owner injection (last resort, owner decides).
Never sacrifice payroll or tax obligations to hit the floor — flag those as hard constraints.

### Attention-item format
Each surfaced item pairs a **trigger → suggested action → deadline**: e.g. "Balance dips to $2,700 on the 1st (below $4,000 floor) → nudge Invoice #204 to pay by the 31st, or delay the $600 SaaS charge two days → decide by the 30th." Prioritize by size of impact on the low point and how soon the decision is due.

### Headline and cadence
Lead with **projected end-of-month balance** and the **lowest point + day**, then the daily table and attention items. Run near the 25th (enough runway to act before the 1st) or on demand. This skill **plans only** — every invoice reminder, payment, transfer, or vendor conversation it recommends waits for explicit owner approval before anything moves.