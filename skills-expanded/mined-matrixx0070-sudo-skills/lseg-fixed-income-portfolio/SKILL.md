---
name: lseg-fixed-income-portfolio
version: 1.0.0
description: Analyze and structure a fixed-income portfolio — duration, key-rate durations, convexity, spread duration, and benchmark-relative risk — to reason about positioning versus a benchmark and interest-rate scenarios. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, fixed-income, portfolio, duration, convexity, key-rate, benchmark]
capabilities: []
---

# Fixed-Income Portfolio Analysis

## When to use
Use this to characterize the risk of a bond portfolio and its position versus a benchmark: aggregate duration and DV01, key-rate durations across the curve, convexity, spread duration by sector/rating, and the active bets (duration, curve, spread, credit) implied by the holdings. Then scenario-test the portfolio against rate and spread shocks.

**Not for:** single-bond rich/cheap (lseg-bond-relative-value), curve-slope trade construction (lseg-swap-curve-strategy), or cash-vs-futures hedging mechanics (lseg-bond-futures-basis). This skill is portfolio-level risk and positioning.

This is educational analysis, not investment advice.

## Method
1. **Aggregate the core risk.** Portfolio modified duration = market-value-weighted average of holding durations; portfolio DV01 = Σ position DV01. State both — duration for the summary, DV01 for hedging.
2. **Decompose along the curve with key-rate durations (KRDs).** A single duration hides curve shape. Compute KRDs at 2y/5y/10y/30y (or finer) so you see whether risk is bulleted, barbelled, or laddered.
3. **Measure convexity.** Positive convexity helps in large moves; callables/MBS bring negative convexity. Report portfolio convexity and flag any negatively-convex sleeve.
4. **Split rate vs spread risk.** Compute **spread duration** by sector and rating — the sensitivity to a spread move independent of the govvie curve. A portfolio can be duration-neutral to the benchmark yet heavily long credit spread.
5. **Frame the active position vs benchmark.** For each risk axis, state the active bet: duration over/underweight (in years and % of benchmark), curve tilt (KRD differences), spread/credit overweight (spread-DV01 difference), and any sector/quality skew.
6. **Scenario-test.** Apply parallel shifts (±25/±50/±100bp), curve twists (steepener/flattener), and spread shocks (e.g. +50bp IG, +150bp HY); estimate P&L via duration + convexity, and note where the linear estimate breaks down.
7. **Interpret against the mandate.** Tie active risk back to the tracking-error budget and any constraints (duration band, credit-quality floor). State the single largest active risk and what move hurts most.

## Example
Portfolio duration 6.2y vs benchmark 6.5y → **−0.3y underweight duration** (defensive). KRDs show the underweight sits entirely at the 30y (portfolio 30y-KRD 0.9 vs bench 1.6) while the 5y is overweight (2.1 vs 1.7) — so it's really a **curve steepener** dressed as a small duration underweight, not a parallel call. Spread duration 4.1y vs bench 3.2y → **long credit spread** (+0.9y spread-DV01 overweight), concentrated in BBB industrials. Scenario: +50bp parallel → ≈ −3.1% (duration) +0.4% (convexity) ≈ −2.7%; a 30s flattener would hurt the steepener; +75bp IG spread widening costs ≈ −3.1% on the credit overweight. Largest active risk: the BBB spread overweight, not duration. Illustrative only — NOT advice.

## Pitfalls
- **Reporting duration alone.** Two portfolios with identical duration can have opposite curve exposure — always show KRDs.
- **Ignoring convexity in big moves.** Duration-only P&L understates gains and overstates losses symmetrically; convexity correction matters beyond ~50bp.
- **Conflating rate and spread duration.** A duration-hedged credit book is still fully exposed to spread widening — keep the two separate.
- **Negative convexity surprises.** MBS and callables shorten when rates fall (you don't get the rally) and extend when they rise (you get the selloff) — model the option, don't use static duration.
- **Weighting by par not market value** — distorts every aggregate; use market-value weights.
- **Scenario P&L that ignores carry** over the horizon — a small yield give-up can be paid for by carry.

## Output format
```
Portfolio vs Benchmark: <name> | MV: <..>
Core: duration <p> vs <b> (active <..>y), DV01 <..>, convexity <..>
Key-rate durations: | tenor | port | bench | active | (2y/5y/10y/30y)
  Curve read: <bullet/barbell/steepener/flattener bet>
Spread risk: spread-duration <p> vs <b> (active <..>y), by sector/rating: <..>
Active bets: duration <..> | curve <..> | credit/spread <..> | sector skew <..>
Scenarios (P&L est): ±25/±50/±100bp parallel | twist | spread shock
Largest active risk: <..> | Tracking-error read: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Duration and DV01
- **Modified duration** = − (1/P)(dP/dy); % price change ≈ −ModDur × Δy.
- **DV01 (dollar duration / BPV)** = ModDur × price × 0.0001 × notional. Aggregate DV01 is additive across positions; duration is a MV-weighted average. Use DV01 to size hedges, duration to communicate.

### Key-rate (partial) durations
KRD_i = sensitivity to a 1bp shift at curve node i, holding other nodes fixed. Σ KRDs ≈ effective duration for a parallel move. The **shape** of the KRD vector is the curve position: front-loaded = short-end bet, back-loaded = long-end bet, barbell = wings vs belly. Match KRDs, not just total duration, to control curve risk vs a benchmark.

### Convexity
`%ΔP ≈ −ModDur·Δy + ½·Convexity·(Δy)²`. Positive convexity is a free option-like benefit in volatile markets (you gain more than you lose for symmetric moves). Callable bonds and MBS carry **negative convexity** near the strike — model with effective (option-adjusted) duration and convexity, computed by repricing under ± shocks, not closed-form.

### Spread duration and credit risk
Spread duration = price sensitivity to a change in the bond's spread (OAS/z-spread), holding the risk-free curve fixed. `%ΔP ≈ −SpreadDur × ΔSpread`. Report spread-DV01 by rating bucket; credit P&L in a risk-off scenario is dominated by this, not by govvie duration. Also track **DTS (duration × spread)** as the empirically better measure of relative credit-spread volatility across quality tiers.

### Scenario / stress framework
- **Parallel:** ±25/50/100bp — the first-order rate risk.
- **Twists:** 2s10s steepener/flattener, 5s30s — reveals KRD exposure.
- **Spread shocks:** by sector and rating; correlate with a rate move (risk-off = rates down, spreads up).
- Combine duration + convexity for the rate leg, spread-duration for the credit leg, and add **horizon carry+roll** so the scenario is total-return, not just price.

### Tracking error intuition
Ex-ante tracking error ≈ f(active KRD vector, active spread-DV01, factor covariances). Even without a full risk model, rank active bets by their standalone P&L in a 1σ move on each factor — the largest is usually the binding risk against the TE budget.
