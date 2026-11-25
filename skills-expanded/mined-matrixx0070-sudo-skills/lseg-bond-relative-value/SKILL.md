---
name: lseg-bond-relative-value
version: 1.0.0
description: Screen individual government and credit bonds for relative value against a fitted curve — asset-swap spreads, z-spreads, rich/cheap residuals, and butterfly/box structures — to reason about which bonds are mispriced versus their peers. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, fixed-income, relative-value, asset-swap, z-spread, rich-cheap]
capabilities: []
---

# Bond Relative Value

## When to use
Use this to judge whether a specific bond is cheap or rich versus a fitted curve or a set of comparable bonds: computing asset-swap spread (ASW), z-spread, and the residual to a smooth par/spline curve, and structuring bond-vs-bond trades (switches, butterflies, boxes) that isolate the mispricing while neutralizing duration.

**Not for:** curve-shape or slope trades expressed in swaps (lseg-swap-curve-strategy), whole-portfolio construction (lseg-fixed-income-portfolio), or the cash-vs-futures basis (lseg-bond-futures-basis). This skill is bond-level rich/cheap.

This is educational market analysis, not investment advice.

## Method
1. **Assemble a comparable set.** Same issuer/sector, same currency, similar liquidity. For govvies use the on-the-run + off-the-run curve; for credit use same-rating, same-tenor peers.
2. **Choose a spread measure and be consistent.** Yield-to-maturity for a quick read; **z-spread** (constant spread over the zero curve that reprices the bond) for a curve-aware read; **ASW** (par-par asset-swap spread) for a funding-relative read. Do not mix measures within one screen.
3. **Fit a smooth curve** to the comparable set (Nelson-Siegel / Svensson for govvies, or a monotone spline). The fit is the "fair" line.
4. **Compute each bond's residual** = actual spread (or yield) − fitted value. Positive residual (higher yield/spread than the curve says) = **cheap**; negative = **rich**.
5. **Rank by residual, but normalize.** Divide the residual by its historical standard deviation to get a z-score; a +2σ cheap residual is a stronger signal than a +2bp one. Note liquidity — an illiquid off-the-run will look chronically cheap for a reason.
6. **Structure the trade to isolate the view.** A switch (sell rich, buy cheap) should be **DV01-neutral**; a butterfly (long the belly vs short the wings, or vice versa) should be both DV01-neutral and, ideally, 50/50 or regression-weighted. State the weighting convention.
7. **State the carry and the catalyst.** A cheap bond you hold has carry+roll; quantify it. Name why the mispricing should close (index inclusion, auction concession unwinding, liquidity normalization) — a residual with no catalyst can persist.

## Example
Screening 10 same-issuer bonds around the 7y point. Fitted z-spread curve says the 7.2y bond should trade at +38.0bp; it actually trades at +44.5bp z-spread. Residual = +6.5bp cheap; historical σ of this residual ≈ 2.8bp → z-score ≈ +2.3σ, a meaningful cheapness. Its neighbor at 6.8y trades 3.0bp rich (−1.1σ). A DV01-neutral switch — buy the 7.2y, sell the 6.8y — harvests ~9.5bp of relative cheapness with near-zero outright duration. Catalyst: the 7.2y is a recent auction line still digesting supply; concession typically fades over 4–6 weeks. Carry: the long leg out-carries the short by ~1.2bp/month. NOT a recommendation — illustrative only.

## Pitfalls
- **Comparing yields across different coupons/duration** without a curve — high-coupon bonds have shorter duration and different roll; use z-spread or a fitted residual, not raw YTM gaps.
- **Overfitting the curve** so every bond looks fair — Svensson with too many free knots erases the very residuals you're hunting. Prefer parsimonious fits.
- **Ignoring liquidity/specialness.** A bond trading special in repo will look cheap on ASW but is expensive to short — the RV is illusory once financing is included.
- **Un-normalized residuals.** 5bp is huge for a liquid benchmark and noise for an illiquid tail; always z-score against history.
- **Duration leakage in the switch.** If legs aren't DV01-matched the trade is a covert directional bet, not RV.
- **No catalyst.** Structural cheapness (small size, index-excluded) is not an opportunity; it's a permanent feature.

## Output format
```
Universe: <issuer/sector, ccy, tenor range> | Spread measure: <z-spread/ASW/YTM>
Curve fit: <Nelson-Siegel/Svensson/spline>, R²/RMSE: <..>
Rich/cheap table:
  | bond | tenor | actual spread | fitted | residual (bp) | z-score | liquidity |
Top cheap: <bond> (+<..>bp, +<..>σ) | Top rich: <bond> (−<..>bp, −<..>σ)
Structure: <switch/butterfly>, DV01 weights <..>, expected pickup <..>bp
Carry+roll: <..>bp/mo | Catalyst: <..> | Special/repo caveat: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Spread measures compared
- **YTM gap:** fast, but conflates coupon and curve effects. Screening only.
- **Z-spread (zero-volatility spread):** the constant spread added to every point of the zero/spot curve so discounted cash flows equal the market price. Curve-aware; the workhorse for govvie and non-callable credit RV.
- **ASW (par-par asset swap):** spread over the swap curve from packaging the bond with a par swap. Reflects funding/swap-relative value; the desk measure for financing.
- **OAS:** z-spread minus the cost of embedded optionality — required for callables/MBS, not for bullets.

### Fitting the fair curve
Nelson-Siegel: `y(τ) = β0 + β1·[(1−e^(−τ/λ))/(τ/λ)] + β2·[(1−e^(−τ/λ))/(τ/λ) − e^(−τ/λ)]`. β0 level, β1 slope, β2 curvature, λ the decay. Svensson adds a second hump term for richer long ends. Fit to the comparable set, then read residuals. Keep parameters few — the goal is a smooth "fair" reference, not a perfect interpolation.

### DV01-neutral switch weighting
`Notional_short = Notional_long × (DV01_long / DV01_short)`. This equalizes the price sensitivity per basis point so a parallel curve move nets to ~zero; the P&L is the change in the *relative* spread.

### Butterfly weighting
For a body (belly) vs two wings:
- **50/50 (cash-neutral or DV01-neutral):** wings split so total wing DV01 = body DV01.
- **Regression-weighted:** wing weights from the historical beta of belly-spread to each wing, so the fly is neutral to the dominant curve factor (level/slope) and expresses pure curvature.
State which; a 50/50 fly still carries slope risk.

### Carry and roll-down
- **Carry** ≈ (coupon income − financing) over the horizon.
- **Roll-down** ≈ DV01 × (change in yield as the bond ages down a static curve). A cheap bond on a steep part of the curve can pay you to wait. Total expected return over the horizon ≈ spread change (RV convergence) + carry + roll.

### When cheap is a trap
Persistent cheapness usually reflects a real cost: small issue size (index-excluded), poor liquidity (wide bid-offer), repo specialness (expensive to short the rich leg against it), or credit/headline risk not in the peer average. Always ask what the market knows that the fitted curve doesn't.
