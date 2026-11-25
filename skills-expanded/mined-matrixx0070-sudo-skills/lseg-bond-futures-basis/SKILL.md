---
name: lseg-bond-futures-basis
version: 1.0.0
description: Analyze the basis between a deliverable government bond and its futures contract — gross basis, net basis, carry, implied repo rate, and the cheapest-to-deliver — to reason about hedging, roll, and relative richness. Educational quant workflow, not investment advice.
author: matrixx0070
tags: [lseg, fixed-income, futures, basis, ctd, repo, carry]
capabilities: []
---

# Bond Futures Basis Analysis

## When to use
Use this to decompose the relationship between a cash government bond and the bond-future that can deliver it: to compute gross and net basis, carry, and the implied repo rate, to identify the cheapest-to-deliver (CTD) issue, and to reason about whether the future is rich or cheap versus cash. Applies to Bund/Bobl/Schatz, Gilt, UST, JGB futures — any physically-settled bond future with a delivery basket and conversion factors.

**Not for:** outright duration positioning across a portfolio (lseg-fixed-income-portfolio), or curve-shape trades on the swap curve (lseg-swap-curve-strategy). This skill is about one future against its deliverable basket.

This is educational market analysis, not investment advice. Nothing here is a recommendation to trade.

## Method
1. **Pin the contract mechanics.** Note the delivery month, the delivery basket, each bond's conversion factor (CF), the notional coupon of the contract, and the day-count convention. The CF normalizes each deliverable to the notional coupon.
2. **Compute the gross basis** for each candidate: `Gross basis = Clean price of bond − (Futures price × CF)`. Quote in price points; it is always ≥ 0 near delivery for the CTD by no-arbitrage.
3. **Compute carry** to the delivery date: `Carry = coupon income accrued over the holding period − financing cost (repo) over the same period`. Positive when the coupon yield exceeds the repo rate (the normal upward-sloping case).
4. **Compute net basis**: `Net basis = Gross basis − Carry`. Net basis is the cost of the delivery option plus any richness; it is the number to compare across the basket.
5. **Compute the implied repo rate (IRR)** — the return from buying the bond, selling the future, and delivering: `IRR = [(Futures × CF + accrued at delivery − (bond price + accrued now)) / (bond price + accrued now)] × (360 or 365 / days)`. The bond with the **highest IRR is the CTD**.
6. **Cross-check CTD** two ways: highest IRR and lowest net basis should agree. If they disagree, re-check accrued-interest dates and the day-count. Note that CTD shifts with yield level (a rule of thumb: at yields above the notional coupon the market tends toward longer-duration/lower-CF issues; below, toward shorter).
7. **Interpret.** A large positive net basis on the CTD signals the future is cheap to cash (or the delivery option is valuable); near-zero net basis signals fair. State the delivery-option component you cannot strip out analytically as a residual to be aware of.

## Example
Bund future price 133.50, delivery in 60 days. Candidate bond: clean price 128.20, CF 0.945000, coupon 2.30% (semi-annual), current accrued 0.85, repo 3.40% (act/360).
- Gross basis = 128.20 − (133.50 × 0.945000) = 128.20 − 126.1575 = **2.0425**.
- Carry (60 days): coupon income = 2.30% × (60/365) × 100 ≈ 0.378; financing = (128.20 + 0.85) × 3.40% × (60/360) ≈ 0.731. Carry = 0.378 − 0.731 = **−0.353** (negative — repo exceeds running yield, an inverted-carry regime).
- Net basis = 2.0425 − (−0.353) = **2.3955**.
Interpretation: net basis is clearly positive, so the future is cheap to this bond and/or the delivery option is being priced. To confirm CTD, compute IRR for every basket bond and pick the max; do not declare CTD from one issue.

## Pitfalls
- **Wrong accrued-interest dates.** Basis is dominated by accrued at *both* the trade date and the delivery date — use the contract's exact last-delivery day, not month-end.
- **Mixing day-counts.** Repo is usually act/360, the bond coupon act/act or 30/360 — a mismatch silently corrupts carry.
- **Calling the CTD from gross basis.** Gross basis ignores carry; the CTD is the highest-IRR / lowest-net-basis issue, which can differ.
- **Ignoring the delivery option.** Net basis embeds the short's timing and quality (switch) option; a positive net basis is not pure "richness" you can arbitrage away.
- **Assuming CTD is static.** A parallel yield move can switch the CTD and break a basis position — re-run the basket after large rate moves.
- **Sign confusion on carry** in an inverted regime — when repo > running yield, carry is negative and *widens* net basis.

## Output format
```
Contract: <future> <delivery month> | Futures price: <..> | Days to delivery: <..>
Basket (per bond):
  | bond | clean px | CF | accrued | gross basis | carry | net basis | IRR% |
CTD: <bond>  (highest IRR = <..>%, lowest net basis = <..>)  [both criteria agree? yes/no]
Regime: carry <positive/negative>, repo <..>% vs running yield <..>%
Read: future <rich/cheap/fair> vs cash; delivery-option caveat: <..>
NOT investment advice — educational analysis only.
```

## Reference

### The core identities
- **Gross basis** = P_bond − (F × CF), in price points.
- **Carry** = accrued coupon over holding period − repo financing over holding period.
- **Net basis** = Gross basis − Carry = the delivery-option value + residual richness.
- **Implied repo rate (IRR)** = annualized return of the cash-and-carry: buy bond, sell CF futures, deliver. The **CTD maximizes IRR**.

### Implied repo rate, expanded
```
Invoice at delivery = F × CF + accrued_at_delivery
Cost today          = P_bond + accrued_now
IRR = (Invoice − Cost) / Cost × (basis_days_per_year / days_to_delivery)
```
Use act/360 for euro/USD repo, act/365 for GBP. IRR > actual term repo ⇒ cash-and-carry is profitable (future cheap); IRR < repo ⇒ reverse cash-and-carry.

### Conversion factor intuition
CF ≈ price of the bond at delivery if it yielded the contract's notional coupon. CF > 1 for coupons above the notional, < 1 below. The CF is fixed by the exchange for the contract; use the published value, do not re-derive it casually.

### Why the CTD changes with yields
The CTD is the bond that is cheapest to buy and deliver. Because CFs are computed at a single notional yield, when market yields rise above the notional coupon, higher-duration (typically longer-maturity, lower-CF) bonds become relatively cheaper to deliver; when yields fall below it, the shorter/higher-CF end becomes cheapest. This is the embedded **switch option** the short owns.

### Delivery options (why net basis isn't free money)
The short position in the future holds: the **quality/switch option** (deliver whichever bond is cheapest at expiry), the **timing option** (choose the delivery day in the month), and the **wildcard option** (deliver after the futures settlement price is fixed). These options have positive value to the short, which is why the CTD's net basis is positive even in a fair market — it is the price of the options, not an arbitrage.

### Duration hedging with the future
To hedge a cash bond position with the future:
`Number of contracts = (BPV_position / BPV_CTD) × CF_CTD`
where BPV is the basis-point value (DV01). Hedge on the CTD because that is what drives the future near delivery. Re-hedge if the CTD switches.
