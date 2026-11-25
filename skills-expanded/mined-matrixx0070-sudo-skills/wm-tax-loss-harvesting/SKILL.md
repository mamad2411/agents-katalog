---
name: wm-tax-loss-harvesting
version: 1.0.0
description: Structure a tax-loss-harvesting review — identify loss lots, avoid wash sales, choose replacements, and quantify the benefit — as educational advisory support.
author: matrixx0070
tags: [wealth-management, tax-loss-harvesting, wash-sale, cost-basis, tax-aware, advisory]
capabilities: []
---

## When to use

Reach for this when you are an advisor reviewing a taxable account for opportunities to realize losses that can offset gains or income, and you want a disciplined checklist that respects wash-sale rules and keeps the client's target allocation intact. Use it during volatile markets or at year-end tax planning.

**Not for:** general rebalancing (wm-portfolio-rebalance) or plan-level projections (wm-financial-plan). This is educational and advisory-support only, not personalized tax or investment advice — tax rules are jurisdiction-specific and change. Every harvest decision must be confirmed with a licensed tax professional and a licensed advisor before acting.

## Method

1. **Identify loss lots** — scan the taxable account for positions with unrealized losses, lot by lot; separate short-term from long-term. Only taxable accounts qualify — tax-advantaged accounts do not.
2. **Check the wash-sale window** — a loss is disallowed if a "substantially identical" security is bought within 30 days before or after the sale (US rule; confirm the local equivalent). Decision point: scan for purchases across ALL accounts including spouse and IRAs, and reinvested dividends, or the harvest is disallowed.
3. **Choose a compliant replacement** — to stay invested and keep allocation, swap into a similar-but-not-substantially-identical security (e.g., a different index tracking a related but distinct benchmark). Note the correlation and the tracking difference.
4. **Quantify the benefit** — realized loss × applicable rate, netted against current-year gains, then up to the ordinary-income offset cap, with the remainder carried forward. Subtract transaction costs.
5. **Watch basis reset and holding period** — harvesting lowers cost basis in the replacement; the benefit is a deferral, not always a permanent saving. State this honestly.
6. **Document and route** — present the candidate list, wash-sale clearance, replacement, and estimated benefit as a proposal; confirm with a tax professional and licensed advisor.

## Example

A client holds an S&P 500 ETF at a $6,000 unrealized loss. Weak: sell it and rebuy the same ETF next week. Strong: "That rebuy would trigger a wash sale and disallow the loss — and you also have this ETF in a dividend-reinvesting IRA, which counts. Instead: sell the S&P 500 ETF, harvest the $6,000 loss, and buy a total-market ETF (highly correlated, not substantially identical) to stay invested. Estimated benefit ~$1,440 at a 24% rate, less ~$30 costs. This lowers your basis, so it's largely a deferral. Please confirm with your tax professional before we execute." Wash-sale exposure is checked across accounts and the benefit is stated honestly as a deferral.

## Pitfalls

- Missing wash-sale triggers in other accounts (spouse, IRA) or from automatic dividend reinvestment.
- Swapping into a "substantially identical" security and disallowing the very loss you harvested.
- Overstating the benefit by ignoring the basis reset — it is often deferral, not permanent savings.
- Presenting harvest actions as tax advice; keep it a proposal and route to a licensed tax professional and advisor. Rules vary by jurisdiction.

## Output format

```
Account (taxable only): [name] | Review date:
Loss candidates: [lot | security | ST/LT | unrealized loss | acquired date]
Wash-sale clearance: [checked across all accounts + dividend reinvestment? Y/N per lot]
Replacement plan: [sell | buy (not substantially identical) | correlation note]
Estimated benefit: realized loss [$] × rate → offset gains/income, carryforward, less costs
Caveats: basis reset (deferral), holding-period reset, jurisdiction-specific rules
Disclosures: educational only; confirm with a licensed tax professional and advisor before acting
```

## Reference

US IRS wash-sale rule (IRC §1091) and capital-loss offset/carryforward limits; local equivalents differ. Not tax advice — verify current rules and thresholds with a licensed tax professional.
