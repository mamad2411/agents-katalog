---
name: lseg-swap-curve-strategy
version: 1.0.0
description: Construct and analyze interest-rate swap curve trades — outright, steepeners/flatteners, butterflies, and forward-starting/roll-down structures — with DV01-neutral weighting and carry+roll math. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, rates, swaps, curve, steepener, butterfly, carry-roll]
capabilities: []
---

# Swap Curve Strategy

## When to use
Use this to express a view on the shape of the interest-rate swap curve through cleanly-weighted structures: outright directional, 2s10s/5s30s steepeners and flatteners, and butterflies that isolate curvature — sized DV01-neutral and evaluated on carry, roll-down, and the forward-implied path. Applies to standard IRS curves (SOFR, €STR, SONIA) and their forward-starting variants.

**Not for:** the top-down decision of *whether* the curve should steepen (lseg-macro-rates-monitor), cash-bond rich/cheap (lseg-bond-relative-value), or portfolio-level duration (lseg-fixed-income-portfolio). This skill builds and weights the actual curve structure.

This is educational analysis, not investment advice.

## Method
1. **State the curve view precisely.** Which segment (2s10s, 5s30s, 2s5s10s fly), which direction (steepen/flatten, cheapen/richen the belly), and over what horizon. Vague "curve should steepen" is not a trade.
2. **Get the DV01 of each leg.** For each swap tenor compute the DV01 (PV01) per unit notional. Longer swaps have larger DV01, so equal notionals are *not* curve-neutral.
3. **Weight the structure.**
   - **Steepener/flattener (2 legs):** notionals set so DV01_short-leg = DV01_long-leg; the P&L is then the change in the *slope*, immune (to first order) to parallel shifts.
   - **Butterfly (3 legs):** body DV01 = sum of wing DV01s (50/50), or regression-weighted so the fly is neutral to level and slope and expresses pure curvature.
4. **Compute carry and roll-down.** Carry = the cost/benefit of holding to horizon given the shape (the forward vs spot). Roll-down = the P&L from the position aging along a *static* curve. For curve trades, compute the **net carry+roll of the structure**, not each leg alone.
5. **Check the forwards.** The forward curve already prices a path. A flattener "works" only if the curve flattens *more than the forwards imply* — compare your target to the forward-implied slope, which is the market's baseline.
6. **Stress the structure.** P&L under a bull-steepener, bear-flattener, parallel shift (should be ~0 if DV01-neutral), and a curvature shock (for flies). Confirm the trade isolates the intended factor.
7. **Interpret.** State expected P&L if the view is right, the carry+roll you earn/pay while waiting, the breakeven curve move, and the scenario that hurts most.

## Example
View: 2s10s SOFR curve too flat, should steepen over 3m. Trade: receive 2y, pay 10y (a steepener), DV01-neutral. 2y DV01 ≈ $190/bp per $10mm; 10y DV01 ≈ $880/bp per $10mm. To match, run ~$46mm 2y vs $10mm 10y (46 × 190 ≈ 8,740 ≈ 10 × 880). Current 2s10s = +22bp; forwards imply +30bp in 3m (the curve is *already* priced to steepen 8bp). So the trade profits only if 2s10s exceeds +30bp — the forward, not the spot, is the hurdle. Carry+roll of the DV01-neutral structure ≈ +1.5bp/month (positive — the steepener rolls down favorably here). Worst case: a bear-flattener (front-end sells off on hawkish surprise). Illustrative — NOT advice.

## Pitfalls
- **Equal-notional legs.** A 2s10s in equal notionals is dominated by the 10y's DV01 — it's a covert long/short duration bet, not a slope trade. Always DV01-weight.
- **Forgetting the forwards are the hurdle.** Spot slope is irrelevant; you must beat the forward-implied slope for the trade to pay. This is the single most common error.
- **50/50 fly still carrying slope risk.** A cash/DV01-neutral butterfly is neutral to parallel but not to slope; use regression weights if you want *pure* curvature.
- **Ignoring carry+roll.** A trade that's right on direction can still lose if negative carry bleeds it before the move; compute net carry+roll of the whole structure.
- **Convexity in large moves / long tenors.** DV01-neutrality is first-order; big moves reintroduce curve P&L via convexity, especially with 30y legs.
- **Basis and fixing mismatches** across legs (different indices/tenors) — keep the reference index consistent or price the basis.

## Output format
```
View: <segment> <steepen/flatten/curvature>, horizon <..>
Legs: | tenor | notional | DV01/bp | (pay/receive)
  Weighting: <DV01-neutral / regression β = ..>; parallel-shift P&L ≈ 0? <yes>
Current slope/fly level: <..> | Forward-implied at horizon: <..>  ← the hurdle
Expected P&L if right: <..> | Breakeven move vs forwards: <..>bp
Carry + roll (structure): <..>bp/month
Stress: bull-steep <..> / bear-flat <..> / parallel <..> / curvature <..>
Worst scenario: <..>
NOT investment advice — educational analysis only.
```

## Reference

### DV01 / PV01 weighting
DV01 = PV change per 1bp parallel shift in that swap's rate. Longer tenors carry more DV01 per unit notional (roughly proportional to duration). For an n-leg curve trade, choose notionals so the net parallel-shift DV01 = 0:
- **2-leg (steepener/flattener):** `Notional_A × DV01_A = Notional_B × DV01_B`.
- **3-leg (butterfly):** `DV01_body = DV01_wing1 + DV01_wing2` (equal wings), or set wing weights by regression β of the belly to each wing to also neutralize slope.

### Forwards are the baseline
The swap forward curve is the market's arbitrage-consistent expected path: `forward rate f(t1,t2)` is implied by spot swaps. A curve trade's true benchmark is the **forward-implied** slope/level at the horizon, not the spot. If forwards already price your move, you earn nothing for being right — you must beat the forwards. Roll-down is precisely the P&L from the spot curve converging toward (or the position aging into) the forwards under a static-curve assumption.

### Carry and roll-down (curve structures)
- **Carry** = net running cost/benefit of the legs over the horizon (received fixed − paid fixed, adjusted for the forward vs spot).
- **Roll-down** = P&L as each leg ages to a shorter point on a *static* curve (each swap rolls down/up the curve).
- Compute **net carry+roll of the whole structure**; a steepener can have positive or negative net carry depending on the curve's steepness and the funding leg. Total expected return = curve-move P&L (vs forwards) + carry + roll.

### Butterflies — 50/50 vs regression-weighted
- **50/50 (DV01-neutral wings):** wing DV01s sum to body DV01. Neutral to parallel shifts; **still exposed to slope**.
- **Regression-weighted:** wing weights from the historical betas of belly-vs-wings so the fly is neutral to level *and* slope, isolating **curvature** (the belly's cheapness/richness). Choose based on whether you want a pure-curvature bet or a directional-curve bet.

### Convexity and higher-order risk
DV01-neutral is a first-order (linear) hedge. In large rate moves, gamma/convexity — larger for longer tenors — reintroduces P&L: a DV01-neutral 5s30s will show curve P&L in a big parallel move because the 30y's convexity dominates. For big-move robustness, either add a convexity hedge or acknowledge the residual directional exposure.

### Common structures and their factor
- **Outright receive/pay:** level (duration) bet.
- **Steepener/flattener:** slope bet; DV01-neutral removes level.
- **Butterfly:** curvature bet; regression weights remove level and slope.
- **Forward-starting swap:** isolates a future curve segment (e.g. 1y1y, 5y5y) — a clean expression of the priced forward path vs your view.
