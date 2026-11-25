---
name: wm-portfolio-rebalance
version: 1.0.0
description: Plan a portfolio rebalance back to target weights — drift analysis, trade list, cost and tax awareness, and cash-flow-first methods — as advisory support.
author: matrixx0070
tags: [wealth-management, rebalance, drift, allocation, trade-list, tax-aware]
capabilities: []
---

## When to use

Reach for this when you are an advisor bringing an existing portfolio back to its target allocation and want a disciplined method that respects costs, taxes, and thresholds rather than trading reflexively. Use it after wm-investment-proposal has set the targets, or at a scheduled rebalance date.

**Not for:** setting the target allocation in the first place (wm-investment-proposal) or realizing losses for tax purposes as the primary goal (wm-tax-loss-harvesting). It is advisory-support, not personalized investment or tax advice, and it does not place trades. Route execution decisions to a licensed advisor and tax questions to a tax professional.

## Method

1. **Measure drift** — compute current vs. target weight per sleeve and the absolute drift. Decision point: only sleeves breaching the rebalance band (e.g., ±5% absolute or ±25% relative) are candidates; small drift is left alone to avoid churn.
2. **Prefer cash-flow rebalancing** — direct contributions, dividends, and withdrawals to under/over-weight sleeves first, before selling. This minimizes taxable events.
3. **Sequence by account type** — do taxable-heavy trades last; use tax-advantaged accounts (IRA/401k) for the trades that would otherwise realize gains. Note the asset-location angle without giving tax advice.
4. **Build the trade list** — for remaining drift, size buys and sells to reach target within the band, netting where possible. Prefer selling highest-cost-basis lots to limit gains (flag; confirm with a tax professional).
5. **Estimate cost and tax friction** — transaction costs and estimated realized gains for the proposed trades; compare against the benefit of correcting drift.
6. **Document and route** — present the trade list with rationale as a proposal; execution and tax confirmation go to a licensed advisor and tax professional.

## Example

Equity target 60%, now 68% after a rally; band is ±5%, so it breaches. Weak: sell 8% of equities in the taxable account immediately. Strong: "Drift is +8%, past the band. First I'd direct the next two quarters of dividends and the pending $10k contribution to bonds, closing ~3%. For the remaining 5%, I'd rebalance inside the IRA — no tax there — selling the appreciated equity sleeve rather than the taxable account. Estimated transaction cost ~$40, realized gains ~$0. Confirm with your tax professional before we act." Cash flow and account location do the work before any taxable sale.

## Pitfalls

- Rebalancing on a calendar with no threshold, generating needless trades and taxes.
- Selling in the taxable account when the same trade could happen tax-free in a retirement account.
- Ignoring cost basis and lot selection, realizing avoidable short-term gains.
- Presenting the trade list as executed advice; keep it a proposal and route to a licensed advisor and tax professional.

## Output format

```
Portfolio: [name] | Rebalance date: | Band: [±% absolute / relative]
Drift table: [sleeve | current % | target % | drift | breaches band? Y/N]
Cash-flow rebalance: [contributions/dividends/withdrawals directed to which sleeves]
Trade list: [account | buy/sell | asset | amount | lot/basis note]
Account sequencing: [which trades in tax-advantaged vs. taxable, why]
Cost & tax estimate: transaction [$], est. realized gains [$]
Disclosures: proposal only; confirm execution with a licensed advisor and tax with a tax professional
```

## Reference

Rebalancing-band and cash-flow-rebalancing research; asset-location principles. Confirm firm trading and suitability policy; tax treatment varies by jurisdiction and account.
