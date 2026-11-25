---
name: smb-friday-brief
version: 1.0.0
description: A read-only Friday end-of-week pulse — revenue vs prior week, top sellers, and the wins and watches to carry into next week.
author: matrixx0070
tags: [reporting, analytics, revenue, weekly, operations]
capabilities: []
---

# Friday Brief

## When to use
Use this at the end of the week for a tight, honest read on how the business did — what moved, what sold, what to watch going into next week. Read-only reporting; it changes nothing.

**Not for:** a live cross-functional snapshot (use smb-business-pulse), forward cash forecasting (use smb-cash-flow), or taking any action. This reports the week just ended.

## Method
1. Pull this week's sales, revenue, and order data, plus the prior week for comparison.
2. Compute revenue vs prior week (absolute and percent) and note the drivers behind any swing.
3. Identify the top-selling products or services and any notable drop-offs.
4. Surface wins (deals closed, milestones, standout days) and watches (slipping deals, refund spikes, inventory or cash concerns). Decision point: a watch is something that needs attention next week, not just a bad number.
5. Keep it scannable and factual. Cite the numbers; if data is incomplete, say so rather than estimating. This is a report only — no actions are taken.

## Example
Headline: Revenue $18,400 this week, up 12% from $16,450 last week — driven by two large repeat orders on Wednesday. By the numbers: 47 orders (up from 41), AOV $391. Top sellers: Deep Clean package ($6,200), Gift cards ($1,900). Wins: closed the Harbor account ($4k). Watches: refunds up to 4 (from 1) — all tied to the new courier; one $9k invoice now 40 days overdue.

## Pitfalls
- **Estimating missing data.** If Thursday's numbers haven't synced, say so — don't fabricate a total.
- **Reporting swings without drivers.** "Up 12%" is trivia; "up 12% on two repeat orders" is insight.
- **Watches with no teeth.** List only items worth acting on next week, not every minor dip.
- **Turning a report into action.** Suggestions are optional prompts; nothing changes without a separate request.

## Output format
```
Headline: revenue $__ this week vs $__ last (<±>%)
By the numbers: orders, AOV, key figures
Top sellers: <item> $__ [...]
Wins: <bullet> [...]
Watches: <bullet with figure> [...]
Suggested focus for next week (optional): 2-3 prompts
(No changes made without a separate request.)
```

## Reference

### Weekly metric set (compute each, always with a comparison)
A number alone says nothing — pair every figure with prior week and, where useful, a 4-week average to strip out noise.
- **Revenue** — this week, ± vs prior week (absolute and %), vs 4-week trailing average.
- **Orders / transactions** and **AOV** (average order value = revenue ÷ orders). A revenue swing is either more orders or bigger orders — always decompose which.
- **New vs repeat revenue** — a week carried by one big repeat order is a different story than broad-based growth.
- **Top sellers** (by revenue and by units) and any notable **drop-offs** vs the item's norm.
- **Refunds / returns** — count and $, and refund rate (refunds ÷ gross). A spike is a watch even if net revenue looks fine.
- **Gross margin** if cost data is available — revenue can rise while margin falls on discounting.
- **Cash-adjacent flags** — new overdue invoices, large upcoming outflows next week.

### The driver rule
For every material swing (say > ±10%), name the cause, not just the number. "Revenue up 12%" is trivia; "up 12% on two repeat orders Wednesday — underlying daily run-rate flat" is insight the owner can act on. Trace swings to: a specific large order, a promotion, a seasonal shift, a channel change, or a data-sync gap. If you can't find the driver, say so rather than inventing one.

### Wins vs watches — the distinction
- **Win** = a positive that's worth noticing or repeating (a closed deal, a record day, a product breaking out). Keep to real signal, not "revenue was positive."
- **Watch** = something that needs *attention next week*, with a figure attached and an implied owner action. A one-off bad day is not a watch; a trend, a threshold breach, or a risk is. Test each candidate: "does this change what someone should do next week?" If no, drop it.

### Threshold triggers (flag automatically when crossed)
| Signal | Watch trigger |
|--------|---------------|
| Revenue vs prior week | down > 10% |
| Refund rate | > 5% of gross, or 2x the 4-week norm |
| AOV | down > 15% (discount creep) |
| Any invoice | newly crossed 30 / 60 days overdue |
| Single customer concentration | one customer > 30% of the week's revenue |
| Inventory | a top seller below reorder point |
| Cash | known outflow next week > cash on hand |

### Data-integrity rules (read-only means honest)
- If a day or channel hasn't synced, state "Thursday not yet synced — totals partial," never fabricate or straight-line a total.
- Distinguish booked vs collected revenue if they differ; a sale isn't cash.
- Note one-time distortions (a bulk order, a refund of a prior-period sale) so the trend isn't misread.

### Common weekly patterns to name
- **Concentration risk** — one customer or one order drove most of the week. Flag it; it's fragile, not a trend.
- **Discount creep** — revenue flat but AOV and margin down means you're buying sales with price. Worth a watch.
- **Front/back-loaded week** — most revenue on one or two days signals dependence on a channel or promo, not steady demand.
- **Refund lag** — refunds spiking after a fulfillment change (new courier, new packaging, new supplier) points straight at the cause.
- **Quiet leading indicators** — a dip in new-customer orders or in pipeline touches this week is next month's revenue problem showing up early.

### Format discipline
Keep it to one screen. Lead with the headline number and its driver, then by-the-numbers, top sellers, wins, watches, and at most 2-3 *optional* focus prompts for next week. This is a report: any suggested focus is a prompt for the owner, and nothing is actioned, no message sent, and no money moved without a separate, explicit request.
