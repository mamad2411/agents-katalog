---
name: fin-variance-analysis
version: 1.1.0
description: Decompose an actual-vs-plan gap into price, volume, mix, and rate drivers that tie to the total EXACTLY, solving for any unknown so the bridge closes with zero residual, plus a waterfall and action-oriented narrative.
author: matrixx0070
tags: [finance, variance, fpa, budget, bridge, waterfall, pvm]
---

# Variance Analysis

## When to use
Use this to explain why actuals differ from budget, forecast, or prior period — for a P&L line, a department, or a KPI — turning a raw dollar gap into named, quantified drivers that **tie exactly** to the total.

**Not for:** the statement-level "material line changed" flagging inside a reporting package (fin-financial-statements), or reconciling GL to a source (fin-reconciliation). This is the *why* behind one variance, decomposed to closure.

## Method
1. **Frame the comparison.** Metric, actual, baseline (budget/forecast/prior), total variance in $ and %; favorable (F) or unfavorable (U).
2. **Set materiality.** The $ and/or % threshold below which you do not decompose.
3. **Decompose into drivers.** Price × volume for revenue, rate × hours for labor, volume × mix for product lines, plus one-time/timing. Isolate each in turn holding the others constant. Decision point: revenue → PVM; margin/rate → rate/mix + interaction; cost → rate + efficiency.
4. **CLOSE THE BRIDGE TO AN EXACT TIE.** The drivers must sum to the total variance with **zero residual**. If a driver depends on an unknown (e.g. what share of COGS saw the input-cost rise), **solve for that unknown so the bridge ties**, then state it as a falsifiable hypothesis to confirm ("input exposure ≈ 36% of COGS — verify"). An open bridge with a plug is a defect, not an analysis.
5. **Show the interaction term.** When two effects compound (a price cut *and* a cost rise), show the standalone price effect, the standalone cost effect, AND their interaction — don't bury the cross-term inside one bar.
6. **Attribute causes and judge the quality of the beat.** Give each driver a business reason, and state whether a favorable result is volume-driven (durable) or price-/one-time-inflated (fragile) — the first question a CFO asks next.
7. **Build the waterfall** (baseline → bars → actual, ties) and **write the narrative**, tagging each driver persistent vs one-time and flagging timing reversals (see FIFO caveat).

## Example
Revenue: actual $4.6M vs budget $4.0M, +$600k (+15%, F). Volume +8,000 units × $50 budget price = +$400k; price +$2.50 × 84,000 actual units = +$210k; mix to a lower-price SKU = −$10k. Sum = +$600k — **ties exactly**. Quality of the beat: mix is *unfavorable* (−$10k), so the beat is volume+price driven (durable), not mix. Causes: volume from a new enterprise deal (persistent), price from the January list increase (persistent), mix from an SMB promo (one-time). Action: raise the forward forecast for volume and price; do not extrapolate the promo mix.

## Pitfalls
- **Leaving a residual / plug.** If the drivers don't sum to the total, solve for the unknown that closes it — never assert "ties ✓" over an approximate sum.
- **Burying the interaction.** Computing cost sequentially on the cut price hides the price×cost cross-term; show it explicitly.
- **Double-counting price and volume** by applying both at actual quantities — hold one constant per driver.
- **Naming a number, not a cause** — and not judging whether a favorable variance is durable or fragile.
- **Treating one-time or timing items as run-rate** — corrupts the next forecast.

## Output format
```
Metric: <...> | Actual: <...> | Baseline: <budget/fcst/prior> | Total var: <$> (<%>) [F/U]
Materiality: <$ / %>
Drivers:
  | driver | $/pp impact | % of total | cause | persistent? |
  Residual after all drivers = 0? [MUST be yes — if not, solve for the unknown]
  Solved-for assumption (if any): <e.g. input exposure ≈ 36% of COGS — verify>
Interaction term (if compounding effects): <price-only | cost-only | interaction>
Quality of the beat: <volume-driven/durable | price-or-one-time/fragile>
Waterfall: baseline → <bars> → actual  (ties exactly: yes)
Narrative + risks + recommended actions: <...>
```

## Reference

### The price / volume / mix bridge (revenue)
Let `b`=budget, `a`=actual. Drivers **must sum to the total**:
- **Volume** = (Units_a − Units_b) × Budget avg price_b
- **Price** = Σ (Price_a − Price_b) × Units_a, per product
- **Mix** = Σ [ (mix%_a − mix%_b) × (Budget product price − Budget avg price) ] × Units_a

Isolate volume at the *budget* price and price at the *actual* quantity so the price×volume interaction is attributed once. **Joint-variance convention:** some FP&A shops break out the price×volume interaction as a separate fourth bar instead of folding it into price — state which convention you use.

Worked: Budget 10,000 @ $50 = $500,000; Actual 11,000 @ $52 = $572,000; total +$72,000. Volume = 1,000×$50 = +$50,000; Price = $2×11,000 = +$22,000; sum +$72,000 ✓ (single product → mix 0).

### Closing the bridge when a driver is unknown (solve-for-the-tie)
Often you know the total and all-but-one driver; the missing piece is a *share* or *exposure*. Solve for it so the bridge ties, then flag it to confirm.

Example — gross margin 35% actual vs 40% budget, after a 5% price cut and an 8% input-cost rise. Budget price 100, COGS 60. Post-cut price = 95. Let `x` = share of COGS exposed to the 8% rise: COGS_a = 60 × (1 + 0.08x). Set (95 − COGS_a)/95 = 0.35 → COGS_a = 61.75 → 60(1+0.08x)=61.75 → x = **0.365**. So ~36.5% of COGS saw the increase. Report: "margin fell 5pp = price cut (≈ −3.2pp standalone) + input-cost rise on ~36% of COGS (≈ −4.8pp standalone), with a small interaction; verify the exposed share." The bridge now ties to 35.0% exactly.

### Interaction / compounding decomposition (margin)
When price and cost both move, report three parts, not a sequential blend:
- **Price-only effect** = margin at new price, old cost.
- **Cost-only effect** = margin at old price, new cost.
- **Interaction** = the residual so the three reconcile to the total margin change. Showing it prevents silently burying the cross-term in the cost bar.

### Break-even volume for a price change
To hold **gross-profit dollars** flat after a price cut of fraction `c` at gross margin `m`:
required volume multiplier = **m / (m − c)**, i.e. Δvolume = c / (m − c).
Worked: m = 40%, c = 5% → 0.40/0.35 = 1.1428 → **+14.3% volume** just to break even on GP dollars. (GP/unit falls from price×0.40 to price×0.35, so 0.40/0.35 − 1 = 14.3%.) A price cut is value-destructive unless it buys at least this much incremental volume — always quantify it.

### Cost / spend variances
- **Rate** = (Actual rate − Standard rate) × Actual qty. **Efficiency** = (Actual qty − Standard qty for actual output) × Standard rate.
- **Labor:** Rate = (Act wage − Std wage) × Act hrs; Efficiency = (Act hrs − Std hrs allowed) × Std wage.
- **Materials:** Price = (Act price − Std price) × Act qty; Usage = (Act qty − Std qty allowed) × Std price.
- **Overhead:** Spending (actual vs budgeted at actual activity) + Volume (budgeted vs applied).

### Timing / FIFO caveat (don't call a deferral a save)
If a favorable cost variance comes from **inventory layers** (FIFO), the margin relief is *deferred, not avoided* — older, cheaper cost is flowing through the P&L while replacement cost has already risen. It **reverses** as newer layers sell. Flag any offset that is a timing artifact (FIFO layers, capitalized-vs-expensed timing, accrual true-ups) as one-time and warn that it unwinds next period.

### New / discontinued products, gross vs net
- **New or discontinued SKUs** have no budget/actual counterpart — treat as **pure mix** or break out as a separate portfolio bar; do not let them distort the price bar.
- Decide the **revenue basis up front** — gross vs net of returns, rebates, and allowances — and decompose consistently; a basis mismatch is a hidden residual.

### Sign / labeling and materiality
- Revenue/margin: Actual > Budget = **F**; Cost/expense: Actual < Budget = **F**. A negative dollar variance is not automatically bad — direction depends on the line.
- Waterfall order: Baseline → volume → mix → price → rate → efficiency → one-time/timing → Actual. Only decompose lines above materiality (e.g. ≥5% and ≥ a dollar floor) — surface the two or three drivers leadership can act on.
