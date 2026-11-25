---
name: wm-client-report
version: 1.0.0
description: Produce a clear, compliant periodic client statement summarizing account performance, holdings, activity, and fees for an advisory relationship.
author: matrixx0070
tags: [wealth-management, client-report, performance, reporting, advisory, statement]
capabilities: []
---

## When to use

Reach for this when you are an advisor or paraplanner assembling a quarterly or annual client-facing report that explains how accounts performed, what changed, and what it cost. Use it to turn raw custodian and performance data into a narrative a client can read in five minutes.

**Not for:** deciding what to buy or sell — that is wm-investment-proposal and wm-portfolio-rebalance. It is not a tax document, and it is not personalized investment advice. This skill is educational and advisory-support only; direct the client to a licensed advisor for any decision, and to a tax professional for tax questions.

## Method

1. **Set the reporting frame** — confirm the period (start/end dates), the accounts included, the base currency, and the benchmark(s) each sleeve is measured against. State the return methodology (e.g., time-weighted vs. money-weighted) so figures are comparable.
2. **Reconcile the data** — pull beginning value, contributions, withdrawals, and ending value; confirm they tie out before computing returns. Decision point: if the source data does not reconcile, flag the discrepancy and stop rather than reporting a number you cannot defend.
3. **Compute and contextualize performance** — report net-of-fee return alongside the benchmark and the prior period. Explain drivers in plain language (what helped, what hurt), not jargon.
4. **Summarize holdings and activity** — current allocation vs. target, notable trades, income received, and any drift worth noting.
5. **Disclose fees and costs** — advisory fee, fund expenses, and any transaction costs for the period, in dollars and as a percentage.
6. **Add forward notes and disclosures** — items to discuss at the next review, plus standard disclosures (past performance is not indicative of future results; figures unaudited; not tax advice).

## Example

A client asks "did I make money this quarter?" Weak: "Your account is up." Strong: "Your portfolio returned +3.1% net of fees for Q2, versus +2.8% for your blended benchmark. The overweight to industrials added about 0.4%; cash drag cost about 0.1%. Advisory fees for the quarter were $1,240 (0.25%). Ending value $498,300, up from $486,900 after a $2,000 withdrawal." Every number ties to the reconciliation and names its benchmark.

## Pitfalls

- Reporting gross returns while implying they are net — always label net-of-fee explicitly.
- Comparing to a benchmark that does not match the mandate (e.g., an all-equity index for a balanced portfolio).
- Publishing figures that do not reconcile to the custodian statement; ties-out first, narrative second.
- Framing commentary as a recommendation to act; keep it descriptive and route decisions to a licensed advisor.

## Output format

```
Client / Accounts: [names, account numbers masked]
Period: [start – end] | Base currency: [ccy] | Method: [TWR/MWR]
Performance:
  Net return: [x%] | Benchmark: [name, y%] | Prior period: [z%]
  Beginning value / +contributions / -withdrawals / ending value
  Drivers: [what helped / what hurt, plain language]
Allocation: current vs. target [table]
Activity: [notable trades, income]
Fees & costs: advisory [$ / %], fund expenses [%], transactions [$]
Discussion items: [for next review]
Disclosures: past performance not indicative; unaudited; not tax advice
```

## Reference

CFA Institute Global Investment Performance Standards (GIPS) for return methodology; SEC marketing-rule guidance on net-of-fee presentation and benchmark disclosure. Confirm firm-specific compliance requirements before distribution.
