---
name: smb-business-pulse
version: 1.0.0
description: Build a one-page cross-functional snapshot of cash, sales, pipeline, and the watch-list so an owner can read the whole business at a glance.
author: matrixx0070
tags: [small-business, dashboard, cash, sales, pipeline, owner-report, kpi]
capabilities: []
---

# Business Pulse

## When to use
Use this when the owner wants a single-glance read on how the business is doing right now — before a call, at the start of a day, or when something feels off and they need one page tying finance, sales, and operations together.

**Not for:** forward forecasting (use smb-cash-flow), month-end reconciliation (use smb-close-month), or the weekly retrospective (use smb-friday-brief). This is a live cross-section, not a closed period.

## Method
1. **Set the as-of date and comparison.** State the snapshot date and the prior period you compare against. Decision point: pick last week for an operational read, last month or same-period-last-year for a trend read.
2. **Pull cash.** Report cash on hand, net change since the last snapshot, and weeks of runway at current burn (use trailing burn, not one day's outflow).
3. **Pull sales.** Show revenue period-to-date vs target and vs prior period, plus the new vs repeat mix.
4. **Pull pipeline.** Summarize open opportunities by stage, weighted value, and expected close this period.
5. **Build the watch-list.** Flag anything off-trend: overdue AR, thin margins, slipping deals, staffing or supply risk. Decision point: keep only items actionable this week — park the rest.
6. **Rank actions.** Convert the watch-list into the top 3 things the owner should act on.

This is an internal read only. Do not send anything to customers or move money — get owner approval before acting on any item.

## Example
As-of Fri vs prior Fri. Cash $48,200 (down $6,100), 5.1 weeks runway. Sales MTD $71k vs $90k target (79%), 62% repeat. Pipeline: 4 deals in Proposal, weighted $22k, two expected to close this month. Watch-list: a $9k invoice 40 days overdue; ad spend up 30% with flat leads. Top 3: chase the $9k, pause the underperforming ad set, confirm the two Proposal closes.

## Pitfalls
- **Padding the watch-list.** Ten flags with no ranking is noise; force it down to the top 3 actions.
- **Stale comparisons.** Comparing to an atypical prior period (a holiday week) hides the real trend — note anomalies.
- **Runway from a single balance.** Weeks-of-runway off one day's cash misleads; base it on trailing burn.
- **Silently guessing missing numbers.** If a source is unavailable, mark the line UNKNOWN rather than estimating.

## Output format
```
As-of: <date> | vs <comparison period>
Cash: on hand $__ | net change $__ | runway __ wks
Sales: PTD $__ vs target $__ vs prior $__ | new/repeat __%/__%
Pipeline:
  <stage> — <count> deals — weighted $__ — exp. close $__
Watch-list:
  - <flag> — <one-line why>
Top 3 actions (owner approval required to act):
  1. ___  2. ___  3. ___
```

## Reference

### The six vital signs every pulse should carry
A pulse is only useful if each line has a target next to the actual. Carry these six numbers and always show actual vs target vs prior:

| Vital sign | How to compute | Healthy zone (typical SMB) |
|---|---|---|
| Cash runway | Cash on hand ÷ avg weekly net burn (trailing 8 wks) | 13+ weeks comfortable, 6-13 caution, under 6 act now |
| Sales attainment | Revenue PTD ÷ target PTD | 95-105% on track, under 90% investigate |
| Gross margin | (Revenue − COGS) ÷ revenue | Services 50-70%, retail/e-comm 30-50%, food/hospitality 60-70% food-cost inverse |
| Repeat mix | Repeat-customer revenue ÷ total | 40%+ is a healthy base; under 25% means you live on acquisition |
| Weighted pipeline coverage | Weighted open pipeline ÷ remaining-period target | 3x rule: carry ~3x the gap you still need to close |
| AR overdue ratio | AR past due ÷ total AR | Under 10% clean, 10-25% watch, over 25% a collections problem |

### Runway calculated honestly
Trailing burn beats a single day. Compute: `net weekly burn = (sum of last 8 weeks' outflows − sum of last 8 weeks' inflows) ÷ 8`. If the business is cash-positive, report runway as "positive — building reserves" rather than a huge misleading number. Always name the fixed monthly nut (rent + payroll + loan + insurance + core SaaS) separately, since that is the floor that keeps burning even if sales stop.

### Watch-list trigger thresholds
Only promote something to the watch-list when it crosses a line. Suggested triggers:
- **AR:** any single invoice over 30 days past due, or total overdue AR exceeding 15% of one month's revenue.
- **Margin:** gross margin down more than 5 points vs the prior period, or any job/product priced below its variable cost.
- **Pipeline:** a deal that has slipped its expected-close date twice, or coverage under 2x with the period more than half over.
- **Marketing:** spend up more than 20% with leads or bookings flat (rising cost per acquisition).
- **Ops/people:** a key role uncovered, a single customer over 20% of revenue, or a single supplier with no backup.

### Top-3 ranking rubric
Score each candidate action on three axes, 1-3 each, and act on the highest totals:
- **Cash impact** — does it protect or free up money this week?
- **Reversibility** — cheap to try and undo scores high; one-way doors score low and need more thought.
- **Effort** — can the owner move it in under an hour, or does it need a project?
Pick the three highest scorers. A $9k overdue invoice (cash 3, reversible 3, effort 1 = 7) beats "redesign the website" (cash 1, reversible 2, effort 1 = 4) every time.

### Owner-approval gate
The pulse reads and ranks; it never acts. Chasing an invoice, pausing an ad set, calling a customer, or moving money are all owner decisions. Present the top 3 as proposals with the one-line rationale and wait for a yes before anything leaves the building.
