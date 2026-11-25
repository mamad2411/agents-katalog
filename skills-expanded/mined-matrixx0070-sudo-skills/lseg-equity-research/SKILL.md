---
name: lseg-equity-research
version: 1.0.0
description: Build a structured equity research read on a single company — business model, drivers, valuation (multiples + DCF), scenario tree, and risks — grounded in disclosed financials with explicit assumptions. Educational analytical workflow, not investment advice.
author: matrixx0070
tags: [lseg, equity, research, valuation, dcf, multiples]
capabilities: []
---

# Equity Research

## When to use
Use this to produce a disciplined, assumption-transparent research note on one listed company: characterize the business, quantify the two or three drivers that move the model, value it via comparable multiples and a DCF, frame bull/base/bear scenarios, and lay out the risks and what would falsify the thesis.

**Not for:** the fast pre-earnings expectations map (spg-earnings-preview-beta), the one-page company snapshot (spg-tear-sheet), or top-down macro positioning (lseg-macro-rates-monitor). This is the full company-level analytical write-up.

This is educational analysis, not investment advice. It does not tell anyone to buy or sell.

## Method
1. **Frame the business.** What does the company sell, to whom, and how does it make money (unit economics, revenue mix, recurring vs one-off)? Name the competitive moat and its durability.
2. **Isolate the 2–3 drivers.** Almost every equity story reduces to a few variables — volume/price, take-rate, subscriber net-adds, gross-margin trajectory. Build the model so these are explicit inputs, not buried.
3. **Reconstruct the financials.** Revenue → gross margin → operating margin → FCF, three years historical and an explicit forecast. Every forecast line must trace to a stated driver assumption.
4. **Value two ways.**
   - **Relative:** EV/EBITDA, P/E, EV/Sales, FCF yield vs a named peer set, adjusting for growth and margin (a PEG or growth-adjusted read, not raw multiples).
   - **Intrinsic:** a DCF — forecast FCF, discount at WACC, add a terminal value (Gordon growth or exit-multiple), bridge EV → equity → per-share.
5. **Reconcile the two.** If DCF and multiples disagree sharply, find why (the market is pricing a different growth/margin path than your model) — that gap *is* the thesis.
6. **Build the scenario tree.** Bull/base/bear, each with a coherent driver set and an implied value; assign rough probabilities and compute a probability-weighted value. A point target with no scenario spread hides the risk.
7. **State risks and falsifiers.** What breaks the thesis (a driver reversing, a margin assumption failing), and what observable would you watch. End with the weakest assumption.

## Example
SaaS company, base case: 22% revenue CAGR (driver: net revenue retention 118% + new-logo adds), gross margin expanding 74%→78%, FCF margin 18%→26%. DCF at WACC 9.5%, terminal growth 3.5% → ~$142 intrinsic. Peers trade 8× EV/Sales; applying a growth+margin-adjusted 7.2× to forward sales → ~$128. The $14 gap comes from the DCF crediting more margin expansion than the peer multiple implies — so the thesis reduces to "does FCF margin reach 26%?". Scenario tree: bull $175 (30%, NRR holds >120%), base $135 (50%), bear $85 (20%, NRR falls to 105% and margin stalls) → prob-weighted ≈ $131. Weakest assumption: the terminal margin. Illustrative only — NOT a recommendation.

## Pitfalls
- **Forecasting lines with no driver.** "Revenue grows 15%" with no volume/price/retention mechanism is a wish, not a model.
- **Terminal value doing all the work.** If >75% of DCF value is in the terminal, the valuation is a bet on the exit assumption — disclose the share and stress it.
- **Raw multiple comparison** across different growth/margin profiles — always growth- and margin-adjust, or the "cheap" name is cheap for a reason.
- **WACC hand-waving.** Show the cost of equity (CAPM), cost of debt, and weights; a 1% WACC change swings the DCF materially.
- **A point target without a scenario spread** — hides the asymmetry that is the whole point.
- **Ignoring dilution and SBC** — stock-based comp and share-count creep quietly erode per-share value.

## Output format
```
Company: <name/ticker> | Sector: <..> | Price: <..> | Mkt cap / EV: <..>
Business: <model, revenue mix, moat>
Key drivers (2–3): <driver: current → forecast, source>
Financial forecast: rev/GM%/OM%/FCF, 3y hist + 3y fcst (each line ← which driver)
Valuation:
  Relative: <EV/EBITDA, P/E, EV/Sales vs peers, growth-adjusted> → <value>
  DCF: WACC <..>%, term growth/exit <..>, terminal % of value <..> → <value>
  Reconciliation: <why the two differ = the thesis>
Scenario tree: bull <val,prob> / base <..> / bear <..> → prob-weighted <..>
Risks + falsifiers: <..> | Weakest assumption: <..>
NOT investment advice — educational analysis only.
```

## Reference

### WACC / cost of capital
- **Cost of equity (CAPM):** `Re = Rf + β × ERP` (risk-free + beta × equity-risk-premium). Add a size/idiosyncratic premium for small caps if warranted.
- **Cost of debt:** after-tax = `Rd × (1 − tax rate)`.
- **WACC:** `E/(D+E)·Re + D/(D+E)·Rd·(1−t)`, using market values of debt and equity.

### DCF mechanics
```
FCF = EBIT×(1−tax) + D&A − capex − ΔNWC
EV  = Σ FCF_t / (1+WACC)^t + TV / (1+WACC)^n
TV  = FCF_{n+1} / (WACC − g)   [Gordon]  OR  EBITDA_n × exit multiple
Equity = EV − net debt − minorities − pension deficit + associates
Per share = Equity / fully-diluted shares (incl. options, RSUs, convert dilution)
```
Sanity-check the terminal growth `g` against long-run nominal GDP; `g` ≥ WACC is nonsense.

### Multiples — when to use which
- **P/E:** mature, positive-earnings, comparable capital structures. Distorted by leverage and one-offs.
- **EV/EBITDA:** capital-structure-neutral; the default cross-company multiple. Watch capex intensity (EBITDA flatters asset-heavy names).
- **EV/Sales:** pre-profit / high-growth; pair with a gross-margin adjustment or it's meaningless.
- **FCF yield:** the cash reality check; hard to game.
Always **growth-adjust** (PEG-style) and **margin-adjust** before calling a name cheap or expensive.

### Scenario probabilities and asymmetry
Assign coherent driver sets, not just ±20% on the target. Compute the probability-weighted value and the **skew** (is the upside larger than the downside?). A stock can look fully valued at base yet attractive on asymmetry, or vice versa — the spread is the information.

### Quality-of-earnings checks
- Cash conversion: FCF vs net income over time (persistent gap = accrual quality risk).
- Revenue recognition and DSO trends (channel stuffing shows as rising receivables).
- SBC as a % of revenue and its effect on diluted share count.
- Non-GAAP vs GAAP bridge — what is being added back, and is it truly one-off?
