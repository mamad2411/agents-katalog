---
name: eqr-catalyst-calendar
version: 1.0.0
description: Build a forward calendar of dated and undated catalysts for a stock or watchlist — earnings, product, regulatory, and macro events — ranked by impact and conviction.
author: matrixx0070
tags: [equity-research, catalysts, calendar, events, monitoring]
capabilities: []
---

## When to use

Use this when you cover a name or list and need to know what could move the price and when — so you can size positions, time work, and avoid being surprised. A catalyst calendar turns a scattered set of events into a ranked, dated timeline you can act on.

**Not for:** deciding whether to own the stock (that is the thesis — see `eqr-thesis-tracker`), building the numbers (see `eqr-model-update`), or a single upcoming print (see `eqr-earnings-preview`). This organizes events; it does not form the view. Outputs are research and education, not personalized investment advice.

## Method

1. **Fix the horizon.** Default to the next 4 quarters. *Decision point:* event-driven names → extend to the full catalyst path (e.g., trial readout timelines); index-like names → shorten.
2. **List dated catalysts first.** Earnings dates, ex-dividend, lockup expiries, index rebalances, scheduled regulator decisions, investor days, contract renewals. Cite the source and mark confirmed vs. estimated.
3. **Add undated catalysts.** Product launches, approvals, litigation rulings, M&A, guidance revisions, management changes, macro prints the name is sensitive to. Give each an expected window, not a false exact date.
4. **Classify each: known vs. surprise.** Scheduled events are priced-in to a degree; unscheduled ones carry more asymmetry.
5. **Rank by impact × conviction.** Impact = estimated share-price sensitivity. Conviction = how sure you are of timing and direction. *Decision point:* high-impact/low-conviction items need monitoring triggers, not forecasts.
6. **Attach a watch trigger** to each material item: the observable that tells you it is happening (filing, press wire, data source).
7. **Set a refresh cadence** — weekly for active names, at each print otherwise — and note what would pull an undated item into a dated one.

## Example

Semi-cap name, next 4 quarters. Dated: Q3 earnings 10/28 (confirmed, IR), analyst day 11/14, lockup expiry 12/2. Undated: China export-rule revision (window: this quarter, high impact, low conviction — trigger: BIS Federal Register), a hyperscaler capex guide (window: peer earnings weeks, high impact, medium conviction). Ranked #1 = export rule (impact 9 × conviction 3). Refresh weekly; export item promotes to dated if a proposed rule posts.

## Pitfalls

- **False precision.** Assigning an exact date to an inherently undated event. Use windows and label estimates.
- **Listing without ranking.** A flat list of 30 events is noise. Force impact × conviction.
- **No trigger.** A catalyst you cannot observe in time is not actionable. Every item needs a watch signal.
- **Stale calendar.** Dates slip and events resolve. Set a cadence or it rots within a quarter.
- **Ignoring the priced-in effect.** A known, consensus-anticipated event moves the stock less than its raw importance suggests.

## Output format

```
CATALYST CALENDAR: <ticker / watchlist> | horizon: <n quarters> | as of <date>
DATED
  <date> | <event> | confirmed/est | impact 1-10 | conviction 1-10 | source | trigger
UNDATED
  <window> | <event> | impact | conviction | source | trigger
TOP 3 (impact x conviction): 1) … 2) … 3) …
PROMOTIONS TO WATCH: <undated item -> what dates it>
REFRESH: <cadence>
Note: research/education, not personalized investment advice.
```

## Reference

Research process: separate confirmed dated events (from IR, exchange, regulator, and filing calendars) from estimated windows, and cite each source. Rank by estimated price sensitivity times timing/direction conviction rather than by raw importance, and attach an observable trigger to every material item so it can be caught in real time. Modeling: the calendar feeds position timing and preview work but does not itself change estimates — route number changes to `eqr-model-update`. Disclosure: this is an events framework for research and education, reflects estimates that can slip, and is not personalized investment advice or a recommendation to transact.
