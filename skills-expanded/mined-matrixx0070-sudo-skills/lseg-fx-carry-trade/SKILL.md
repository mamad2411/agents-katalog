---
name: lseg-fx-carry-trade
version: 1.0.0
description: Analyze FX carry — interest-rate differentials, forward points, hedged vs unhedged returns, carry-to-vol, and crash/skew risk — to reason about currency-pair carry positioning and its risk. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, fx, carry, forwards, cip, carry-to-vol, risk]
capabilities: []
---

# FX Carry Trade Analysis

## When to use
Use this to evaluate the carry available in a currency pair or a basket: the interest-rate differential, the forward points implied by covered interest parity, the expected carry return net of the forward drag, the carry-to-volatility ratio, and the crash/skew risk that makes carry a "picking up pennies" strategy. Works for single pairs and for ranked G10/EM carry baskets.

**Not for:** rates-curve views on a single currency (lseg-swap-curve-strategy), broad macro regime monitoring (lseg-macro-rates-monitor), or option-vol surface analysis (lseg-option-vol-analysis) — though carry risk is fundamentally an options/skew story, so cross-reference it.

This is educational analysis, not investment advice.

## Method
1. **Get the rate differential.** Carry ≈ (funding-currency rate − investment-currency rate is *negative* carry; invest high-yield, fund low-yield for positive). Use comparable-tenor money-market or OIS rates, same day-count.
2. **Check covered interest parity (CIP).** Forward points should equal the differential: `F = S × (1+r_quote·τ)/(1+r_base·τ)`. Compute the CIP-implied forward and compare to the market forward — the gap is the **cross-currency basis** (a real, persistent dislocation, not free arbitrage).
3. **Compute the carry return correctly.** Unhedged expected carry over horizon τ ≈ rate differential − expected spot depreciation of the high-yielder. The **forward already prices the differential** (that's CIP), so a pure forward position earns carry only if spot does *not* move to the forward — i.e. carry is a bet against uncovered interest parity (UIP).
4. **Normalize by volatility.** Compute **carry-to-vol** = (annualized carry) / (annualized FX vol). This is the Sharpe-like screen; 3% carry at 6% vol (0.5) beats 5% carry at 15% vol (0.33).
5. **Quantify crash risk.** Carry currencies have negative skew — they "go up by the stairs, down by the elevator." Read the FX risk-reversal (25-delta) as the market's skew price; a deeply negative risk-reversal on the high-yielder signals expensive crash insurance and crowded carry.
6. **Rank / size (basket).** Rank pairs by carry-to-vol, go long the top / short the bottom, size inversely to vol so each contributes equal risk. Note correlation — carry trades are correlated (they all sell off together in risk-off).
7. **State the drawdown risk explicitly.** Carry's return distribution is fat-left-tailed; report the historical max drawdown and the fact that positive carry accrues slowly and reverses violently.

## Example
Long MXN / short JPY, 3-month. MXN 3m rate ≈ 10.8%, JPY ≈ 0.4% → differential ≈ **+10.4% annualized carry**. Forward points confirm via CIP (small negative cross-currency basis). 3m implied vol ≈ 9.5% → **carry-to-vol ≈ 1.09** — attractive on the screen. BUT the 25-delta risk-reversal favors MXN puts by 2.8 vol points (market pricing MXN crash risk), and the pair's historical max drawdown in risk-off episodes exceeds −15% in weeks. So the 1.09 ratio understates tail risk. Read: carry is real and well-compensated on average, but this is a short-vol / short-skew position — size for the crash, not the average. Illustrative — NOT advice.

## Pitfalls
- **Double-counting carry via the forward.** Buying the high-yielder forward does not add carry on top of spot's differential — the forward *is* the differential (CIP). Carry P&L comes from spot failing to converge to the forward (UIP violation).
- **Ignoring the cross-currency basis.** For funded/hedged trades the basis is a real cost or pickup, especially in USD funding stress — don't assume clean CIP.
- **Screening on raw carry, not carry-to-vol.** High nominal carry usually just means high vol; normalize.
- **Treating carry as normally distributed.** It has strong negative skew and fat left tails — VaR from a normal assumption badly understates crash risk.
- **Crowding blindness.** When everyone is in the same carry trade, positioning unwinds amplify the crash — watch risk-reversals and positioning data.
- **EM settlement/liquidity gaps** — NDFs, capital controls, and holiday calendars change the realized return.

## Output format
```
Pair / basket: <long high-yield / short low-yield> | Horizon: <..>
Rate differential: <r_high − r_low> = <..>% annualized (tenor/day-count noted)
CIP check: implied fwd <..> vs market fwd <..> → cross-ccy basis <..>bp
Carry return: <..>% (note: earned only if spot ≠ forward — a UIP bet)
Volatility: <..>% | Carry-to-vol: <..>
Skew/crash: 25Δ risk-reversal <..> vol pts | historical max drawdown <..>%
Sizing: inverse-vol, correlation caveat <..>
Read: carry <attractive/thin> per unit risk; tail-risk warning: <..>
NOT investment advice — educational analysis only.
```

## Reference

### Covered interest parity (CIP)
`F = S × (1 + r_quote·τ) / (1 + r_base·τ)` (quote = price currency, e.g. the "quote" in EURUSD is USD). Forward points = F − S. CIP is enforced by arbitrage for freely-tradable currencies, so the forward mechanically embeds the rate differential. Persistent deviations = the **cross-currency basis**, driven by USD funding demand, bank balance-sheet costs, and regulation — real, not arbitrageable for most participants.

### Uncovered interest parity (UIP) and why carry works
UIP claims the high-yielder should depreciate by exactly the differential, making carry zero in expectation. Empirically UIP fails at short/medium horizons — high-yielders depreciate *less* than UIP predicts (often appreciate), so carry earns a positive average return. That excess return is compensation for **crash risk**, not a free lunch (the "forward premium puzzle").

### Carry-to-vol (the screen)
`Carry-to-vol = annualized rate differential / annualized FX volatility`. A Sharpe-like ranking. Use realized or implied vol consistently. In a basket, size positions inversely to vol so each pair contributes equal risk budget; then account for the high positive correlation among carry pairs (they are one macro factor).

### Skew, risk-reversals, and the crash
FX **risk-reversal** = IV(call) − IV(put) at a delta (e.g. 25Δ). A negative risk-reversal on the high-yielder means puts (crash protection) are bid — the market prices asymmetric downside. Carry returns have **negative skew and excess kurtosis**; the strategy is economically short a put on the high-yielder. Monitor risk-reversals as a real-time crash-risk and crowding gauge.

### Hedged vs unhedged
- **Unhedged:** full spot exposure; earns the differential if UIP fails, bears the crash.
- **Fully hedged (rolled forwards):** locks the forward, so it earns only the cross-currency basis — carry is hedged away by construction. "Carry" as a strategy is inherently an unhedged/partially-hedged spot bet.

### Basket construction and factor risk
Long top-carry / short bottom-carry across G10 or EM diversifies idiosyncratic FX moves but concentrates the **carry factor** — highly correlated to global risk appetite (VIX, credit spreads). Treat aggregate carry exposure as a single risk-on beta and stress it against a risk-off shock, not as independent pair bets.
