---
name: lseg-option-vol-analysis
version: 1.0.0
description: Analyze an option volatility surface — implied vs realized, term structure, skew/smile, and the greeks — to reason about whether options are rich or cheap and how a position behaves. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, options, volatility, skew, term-structure, greeks, vrp]
capabilities: []
---

# Option Volatility Analysis

## When to use
Use this to read an option volatility surface and reason about relative value in vol: implied vs realized volatility (the variance risk premium), the term structure (contango/backwardation), the skew and smile, and how the greeks (delta, gamma, vega, theta) shape a position's behavior. Applies to single-name and index equity options, and adapts to FX and rates vol.

**Not for:** directional equity valuation (lseg-equity-research), FX carry (lseg-fx-carry-trade — though its crash risk is a skew story), or delta-one positioning. This skill is about volatility itself as the traded object.

This is educational analysis, not investment advice.

## Method
1. **Anchor implied vs realized.** Compare the ATM implied vol to trailing realized (close-to-close and a range estimator like Parkinson/Garman-Klass). The gap is the **variance risk premium (VRP)** — implied typically exceeds realized, compensating option sellers for tail risk.
2. **Read the term structure.** Plot ATM IV by expiry. **Contango** (longer-dated higher) is the normal calm regime; **backwardation** (short-dated spiking above long) signals near-term stress/event risk. Note any event dates (earnings, central-bank, elections) that create local bumps.
3. **Read the skew/smile.** For equities, downside puts trade at higher IV than upside calls (negative skew) — the crash premium. Quantify with 25-delta risk-reversal (put IV − call IV) and butterfly (wing IV − ATM). Steepening skew = rising crash fear.
4. **Locate rich/cheap.** Compare current IV levels and skew to their own history (percentile), to realized, and across the surface (e.g. one expiry's skew vs another). State what looks mispriced and versus what benchmark.
5. **Map the greeks of any position under consideration.** Delta (direction), gamma (delta's convexity — long gamma benefits from big moves), vega (sensitivity to IV), theta (time decay — the cost of long gamma). State the sign of each.
6. **Reconcile the trade-offs.** Long options = long gamma/vega, short theta (pay to hold, win on moves/vol spikes). Short options = the reverse (earn theta/VRP, short gamma crash risk). The position's edge must be stated in these terms.
7. **Interpret.** Conclude whether vol is rich or cheap and how a candidate structure (calendar, risk-reversal, butterfly, straddle) expresses the view, with the greek profile and the scenario that hurts most.

## Example
Index ATM 1m IV = 15.2%, trailing 1m realized = 11.0% → VRP ≈ +4.2 vol pts (implied rich to realized, the normal state, but wide vs its median +2.5). Term structure in contango (1m 15.2 < 3m 16.8). 25-delta skew: put IV − call IV = 5.1 vol pts, ~70th percentile (elevated crash pricing). Read: outright vol looks rich to realized, and downside protection is expensive. A structure that is short the expensive puts and long ATM (e.g. a put ratio or risk-reversal) harvests skew — but is short gamma/skew on a crash, which is exactly the scenario that hurts most. If a big move comes, being short gamma is the pain. Illustrative — NOT advice.

## Pitfalls
- **Comparing IV to a single realized estimate.** Close-to-close realized is noisy; use a range-based estimator and multiple windows before calling VRP rich or cheap.
- **Ignoring events in the term structure.** An earnings or FOMC date inflates the straddle of the expiry that spans it — strip the event vol before comparing "clean" term structure.
- **Skew read without history.** Absolute skew levels mean little; percentile-rank them.
- **Confusing vega and gamma.** Vega is sensitivity to *implied* vol changes; gamma is P&L from *realized* moves. Long-dated options are vega-heavy, short-dated are gamma-heavy — different bets.
- **Theta blindness on long vol.** Long gamma bleeds theta daily; the realized move must exceed the implied (breakeven) move to profit.
- **Assuming Black-Scholes flat vol.** The smile exists because returns aren't lognormal; use the surface, don't price off one ATM number.

## Output format
```
Underlying: <..> | Spot: <..> | As of: <date>
Implied vs realized: ATM IV <..>%, realized (CtC / range) <..>% → VRP <..> vol pts (pctile <..>)
Term structure: | expiry | ATM IV |  → contango/backwardation; event bumps: <..>
Skew: 25Δ risk-reversal <..> vol pts (pctile), butterfly <..>; read: <crash premium ..>
Rich/cheap: <what, vs what benchmark, percentile>
Candidate structure: <straddle/calendar/risk-reversal/fly>
  Greeks: delta <..> gamma <..> vega <..> theta <..>
  Worst scenario: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Implied vs realized and the variance risk premium
- **Realized vol:** close-to-close = annualized stdev of log returns; **Parkinson** uses high-low range; **Garman-Klass** uses OHLC (more efficient). Report at least two windows.
- **Implied vol:** backed out of option prices; the market's risk-neutral expected vol plus a risk premium.
- **VRP = implied − realized**, structurally positive (option sellers demand compensation for gap/crash risk). A wide VRP favors sellers *on average* but the tail is the whole risk.

### Term structure
ATM IV by expiry. **Contango** (upward) = calm; the vol-carry (roll-down) rewards being short front vol. **Backwardation** (short > long) = acute stress or a near-term event. Calendar spreads trade the slope. Always identify **event-driven** local peaks (earnings ≈ isolate the implied one-day move = straddle price / spot) and strip them for a clean term read.

### Skew and smile
Equity index vol is a **downward skew** (puts > calls) because crashes are faster and more feared than rallies — a departure from lognormal returns. Measures:
- **Risk-reversal (25Δ)** = IV(25Δ put) − IV(25Δ call): the skew's steepness / crash premium.
- **Butterfly (25Δ)** = ½[IV(25Δ put)+IV(25Δ call)] − IV(ATM): the smile's curvature / tail thickness.
Rank both against history. Single stocks often show a smile (both wings up); FX skew flips sign with the risk-on/off currency.

### The greeks
- **Delta (∂V/∂S):** directional exposure; hedge to isolate vol.
- **Gamma (∂²V/∂S²):** convexity of delta; long gamma = you get longer as it rallies, shorter as it falls (buy-low/sell-high on re-hedge). Peaks ATM, short-dated.
- **Vega (∂V/∂σ):** sensitivity to implied vol; peaks ATM, longer-dated. Long vega wins if IV rises.
- **Theta (∂V/∂t):** time decay; the rent on long gamma/vega. Long options pay theta, short options earn it.
- **Gamma-theta trade-off:** the daily theta bleed is the price of the gamma; you profit long gamma only if realized move > the implied breakeven ≈ IV × √(t) × spot.

### Structures and their vol view
- **Straddle/strangle:** pure long (or short) vol; direction-neutral at inception, long gamma+vega.
- **Calendar:** long term-structure slope (sell front, buy back) — vega-positive, benefits from front vol falling / back vol holding.
- **Risk-reversal:** trades skew (buy call/sell put or vice versa) — a directional + skew bet.
- **Butterfly / condor:** trades the smile curvature / range-bound view; short wings = short tail.
Always state the greek signature and the scenario (big move, vol spike, or time passing quietly) that defines the P&L.
