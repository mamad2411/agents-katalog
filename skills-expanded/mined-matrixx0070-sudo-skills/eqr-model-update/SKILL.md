---
name: eqr-model-update
version: 1.0.0
description: Update a financial model after new information — reported results, guidance, or revised assumptions — with a driver-based estimate change, a reconciliation, and target impact.
author: matrixx0070
tags: [equity-research, modeling, estimates, forecast, valuation]
capabilities: []
---

## When to use

Use this when new information should change the numbers: a quarter reported, guidance moved, an assumption was falsified, or a driver (price, volume, FX, rates) shifted. The goal is a disciplined, driver-based revision with a clean before/after reconciliation so you know exactly what changed and why the target moved.

**Not for:** interpreting the quarter (use `eqr-earnings-analysis` — it feeds this), building a model from scratch (use `eqr-initiating-coverage`), or deciding the thesis still holds (use `eqr-thesis-tracker`). Outputs are research and education, not personalized investment advice.

## Method

1. **Roll the actuals in.** Replace the estimated period with reported figures and re-tie the model (balances, cash flow, share count) before touching the forecast.
2. **Update from guidance.** Reset near-term drivers to the new guide where credible. *Decision point:* if guidance conflicts with your thesis, model your view and show the gap to guidance explicitly.
3. **Revise assumptions at the driver level.** Change volume, price/mix, margin, capex, tax, share count — not the output line directly. Every changed cell traces to a stated reason.
4. **Reconcile old vs. new.** Bridge the EPS/estimate change: how much from actuals, guidance, each assumption, tax, and buyback. The bridge must sum.
5. **Re-run valuation.** Flow the new estimates through the same methods as the initiation (DCF/comps) and note the new fair value.
6. **Update rating and target.** *Decision point:* if the target moves materially, does the rating still hold? State upside/downside vs. current price.
7. **Log the deltas and drivers.** Record what changed, the new vs. old numbers, and the assumptions to watch next period.

## Example

Post-print update. Actuals rolled: EPS came in $0.04 above the modeled quarter. Guidance raised full-year revenue 2%. Driver revisions: units +1%, price flat, gross margin +50bps on mix, tax rate down 1pt. EPS bridge: +$0.04 actuals, +$0.06 higher units, +$0.05 margin, +$0.03 tax, -$0.02 higher opex = +$0.16 to FY EPS ($4.20 → $4.36). Valuation re-run lifts DCF fair value ~4%; target $X → $X+. Rating unchanged (Buy); upside now +18%. Watch next: whether the margin mix benefit is durable.

## Pitfalls

- **Plugging the output.** Typing a new EPS instead of moving the drivers that produce it — untraceable and unfalsifiable.
- **Bridge that doesn't sum.** If the old-to-new walk doesn't reconcile, a change is unexplained or double-counted.
- **Forgetting the balance sheet and cash flow.** Rolling only the P&L breaks FCF, buyback capacity, and the DCF.
- **Anchoring to guidance you don't believe.** Model your view; show the delta to guidance rather than adopting it silently.
- **Moving the target, ignoring the rating.** A materially higher/lower fair value may flip upside/downside past the rating threshold.

## Output format

```
MODEL UPDATE: <ticker> | trigger: <print/guidance/assumption> | as of <date>
ACTUALS ROLLED: <period> — re-tied Y/N
GUIDANCE: old -> new | modeled to guide or to our view (gap: …)
DRIVER CHANGES: driver | old | new | reason
EPS BRIDGE (old -> new): actuals +.. | volume +.. | margin +.. | tax +.. | other +.. = Δ
VALUATION: new fair value (method) | target old -> new
RATING: <held/changed> | upside/downside vs current
WATCH NEXT: <assumptions to monitor>
Note: research/education, not personalized investment advice.
```

## Reference

Research process: roll reported actuals in and re-tie the three statements before forecasting, revise at the driver level so every changed cell traces to a stated reason, and produce an old-to-new EPS bridge that sums. Modeling: model your own view where guidance is not credible and show the gap explicitly; re-run the same valuation methods as the initiation and re-check whether a moved target crosses the rating threshold. This skill executes the changes that `eqr-earnings-analysis` prescribes and that `eqr-thesis-tracker` may trigger. Disclosure: updated estimates, fair values, and targets are research and education built on assumptions that can prove wrong, and are not personalized investment advice or a recommendation to transact.
