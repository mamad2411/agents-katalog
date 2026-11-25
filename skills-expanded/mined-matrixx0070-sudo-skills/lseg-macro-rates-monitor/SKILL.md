---
name: lseg-macro-rates-monitor
version: 1.0.0
description: Build a structured macro-rates monitor — growth/inflation/policy dashboard, market-implied policy path vs your own, curve regime, and cross-asset confirmation — to reason about the interest-rate environment. Educational analytical workflow, not investment advice.
author: matrixx0070
tags: [lseg, macro, rates, central-bank, yield-curve, inflation, policy]
capabilities: []
---

# Macro Rates Monitor

## When to use
Use this to maintain a disciplined read on the interest-rate macro environment: assemble the growth/inflation/labor/policy dashboard, extract the market-implied policy path from OIS/futures, compare it to your own reaction-function view, classify the yield-curve regime, and cross-check against risk assets and the dollar. The output is a coherent "where are we in the cycle and what's priced" picture.

**Not for:** constructing a specific curve trade (lseg-swap-curve-strategy), FX carry positioning (lseg-fx-carry-trade), or bottom-up bond selection (lseg-bond-relative-value). This is the top-down environment monitor those trades sit inside.

This is educational analysis, not investment advice.

## Method
1. **Build the macro dashboard.** For each major economy: growth (GDP nowcast, PMIs), inflation (headline + core, trend and momentum), labor (unemployment, wages), and financial conditions. Note the direction of surprise vs consensus, not just the level.
2. **Pin the central-bank reaction function.** What is the bank targeting now (inflation down, growth, employment), and what have they signaled? State the framework (data-dependent, forward-guidance, average-inflation-targeting) explicitly.
3. **Extract the market-implied path.** Read expected policy rates from OIS / STIR futures / dated meeting pricing. State, meeting by meeting, how many bp of hikes/cuts are priced and the terminal/trough rate.
4. **Form your own path and diff it.** Given the dashboard and reaction function, where do you think policy goes? The **gap between your path and the market's** is the actionable macro view — quantify it in bp at specific dates.
5. **Classify the curve regime.** Bull/bear × steepener/flattener. Bull-steepener (front-end rallies, cuts coming) vs bear-flattener (front-end sells off, hikes) etc. Compute 2s10s, 5s30s, and the level of real yields and breakevens (nominal = real + breakeven inflation).
6. **Cross-asset confirmation.** Does the rates read agree with credit spreads, equities, the dollar, and gold? Divergences (e.g. rates pricing cuts while credit is tight) are either an opportunity or a warning — flag them.
7. **Synthesize.** State the base-case macro regime, the top risk to it, and the single most mispriced part of the curve/policy path (your view vs market) — with the data that would change your mind.

## Example
US dashboard: core PCE momentum cooling (3m annualized 2.4% vs 2.9% prior), payrolls softening but not breaking, PMIs mixed. Reaction function: data-dependent, easing bias. Market prices ~2 cuts (50bp) over the next 4 meetings, trough ~3.75%. My path: the disinflation trend supports 3 cuts (75bp) into a softer labor print — so the market is **~25bp too hawkish at the 6-month point**. Curve: 2s10s at +18bp and steepening = bull-steepener consistent with priced cuts. Cross-asset: credit spreads tight (agrees with soft-landing), but the dollar is firm (mild disagreement — flag). Most mispriced: the front-end 6m sector. Data that flips it: a re-acceleration in core services inflation or wages. Illustrative — NOT advice.

## Pitfalls
- **Confusing level with surprise.** Markets move on data *relative to expectations*; a "strong" number below consensus is dovish. Track surprise, not the raw print.
- **Reading forward rates as forecasts.** Market-implied paths embed a term/risk premium — they are risk-neutral expectations plus premium, not a pure forecast.
- **Fighting the reaction function.** Your macro view is only tradable through the central bank's framework; a bank targeting inflation won't cut on weak growth alone.
- **Nominal-only analysis.** Decompose nominal yields into real + breakeven; a selloff driven by real yields (tightening) means something different from one driven by breakevens (inflation risk premium).
- **Ignoring cross-asset divergence.** Rates pricing a recession while equities make highs is information — don't dismiss it.
- **Single-country tunnel vision** — rate differentials and global spillovers (US → world) drive local curves.

## Output format
```
Region(s): <..> | As of: <date>
Dashboard: | metric | level | trend | vs consensus | (growth/inflation/labor/FCI)
Central bank: framework <..>, current stance <..>, latest signal <..>
Market-implied path: <bp priced per meeting>, terminal/trough <..>
My path: <..> → GAP vs market: <..>bp at <date> (the view)
Curve regime: <bull/bear × steep/flat>, 2s10s <..>, 5s30s <..>, real <..> / BE <..>
Cross-asset check: credit <..> | equities <..> | USD <..> | (agree/diverge)
Base case + top risk + most mispriced sector: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Nominal = real + breakeven
`Nominal yield ≈ real yield (TIPS/linkers) + breakeven inflation`. Decompose every rate move: rising real yields = tightening financial conditions / stronger growth expectations; rising breakevens = higher inflation risk premium. The Fisher decomposition is the first cut on *why* rates moved. Breakeven ≈ expected inflation + inflation risk premium − liquidity premium.

### Extracting the market-implied policy path
- **OIS** (overnight-index swaps) give the cleanest expected average policy rate per horizon.
- **STIR futures** (SOFR, €STR, SONIA, Fed Funds) price dated periods; dated-meeting OIS gives per-meeting probabilities.
- Convert to bp of hikes/cuts by meeting; the **terminal rate** (peak) or **trough** is the path's asymptote.
- Remember: these are **risk-neutral** — they include a term/risk premium, so a "priced cut" is expectation + premium, not certainty.

### Curve regime taxonomy
| | Steepener | Flattener |
|---|---|---|
| **Bull (yields ↓)** | front-end rallies most → cuts priced / easing | long-end rallies most → growth/inflation fears, flight-to-quality |
| **Bear (yields ↑)** | long-end sells most → term-premium/supply/reflation | front-end sells most → hikes priced / tightening |
Inversion (2s10s < 0) has historically preceded recessions; the **dis-inversion** (bull-steepening from deep inversion) often coincides with the onset of cuts.

### Reaction functions
- **Inflation-targeting:** responds to core inflation vs target and expectations; growth matters only via the output gap.
- **Dual mandate (Fed):** inflation + employment; watch which side is binding.
- **Average-inflation-targeting / flexible:** tolerates overshoot to make up undershoots — changes the hiking threshold.
State the framework before forecasting; the same data implies different policy under different mandates.

### Cross-asset consistency checks
- **Credit spreads** widening while rates rally = genuine risk-off (recession pricing); tight spreads + rate cuts priced = soft-landing.
- **Dollar** strength usually accompanies relative US rate/growth outperformance; a falling dollar with US cuts priced is consistent.
- **Gold / breakevens** rising together = inflation/real-rate story.
Persistent divergences are either a mispricing (opportunity) or a regime the rates market hasn't caught up to (warning) — always name which you think it is.
