---
name: pe-returns-analysis
version: 1.0.0
description: Model a private-equity deal's returns end to end — entry and exit enterprise value, leverage, the MOIC/IRR relationship, and a value-creation bridge decomposing return into EBITDA growth, multiple expansion, and debt paydown — with base/bull/bear cases and sensitivity tables.
author: matrixx0070
tags: [returns, moic, irr, lbo, value-creation-bridge, leverage, sensitivity]
capabilities: []
---

## When to use

Use this when you need a defensible number for what a deal returns — the equity multiple (MOIC) and the annualized rate (IRR) an investment is expected to produce, and the drivers behind it. Reach for it when you are pricing an entry, testing whether an exit thesis clears the fund's hurdle, sizing how much leverage the returns depend on, or decomposing a projected or realized return into its levers for an IC or LP. The output is a returns model: entry and exit valuation, a sources-and-uses view of leverage, base/bull/bear cases, a value-creation bridge, and sensitivity tables on the assumptions that move the answer most.

**Not for:** assessing a company's AI maturity and the return that AI could unlock (use pe-ai-readiness), running the full diligence workstream (use pe-dd-checklist), preparing the questions for management and expert calls (use pe-dd-meeting-prep), the fast go/no-go screen before any modeling (use pe-deal-screening), building the origination pipeline (use pe-deal-sourcing), writing the committee memo that this model feeds (use pe-ic-memo), tracking KPIs and covenants after close (use pe-portfolio-monitoring), turning the levers into an owned execution plan (use pe-value-creation-plan), or dissecting LTV/CAC and contribution margin (use pe-unit-economics).

## Method

1. Fix the entry. Set entry EBITDA and the entry EV/EBITDA multiple, then entry EV = EBITDA × entry multiple. Subtract net debt at close to get entry equity value — the sponsor's invested capital plus any co-invest and fees. **Decision:** decide whether you underwrite on LTM, NTM, or a normalized "adjusted" EBITDA, and hold that definition constant at entry and exit — mixing bases silently manufactures multiple expansion.
2. Build the leverage. Lay out sources and uses: how much debt (turns of EBITDA) versus equity funds the purchase. **Decision:** set the entry leverage (e.g. 4.0–6.0x) against what the credit market and cash flows actually support — more debt lifts IRR but raises covenant and refinancing risk, and the bear case must survive it.
3. Project the hold. Model revenue, EBITDA, capex, working capital, and free cash flow over the hold (typically 3–7 years). Sweep free cash flow to debt paydown (or track dividends/recaps if modeled) so exit net debt falls out of the operating case, not an assumption.
4. Fix the exit. Set exit EBITDA (from the operating case) and the exit multiple, then exit EV = exit EBITDA × exit multiple; exit equity value = exit EV − exit net debt. **Decision:** default the exit multiple to at or below entry — underwriting multiple expansion is a bet on the market, not on the business, and IC will discount it.
5. Compute the returns. MOIC = total value to equity / invested equity. Derive IRR from the equity cash flows and hold; the two are linked by MOIC ≈ (1 + IRR)^years, so a 2.0x over 4 years implies roughly a 19% IRR (rule-of-72 gives the doubling intuition). Report gross (deal-level) separately from net (after fees, carry, and fund expenses) — LPs earn net.
6. Build the value-creation bridge. Decompose the equity gain into EBITDA growth, multiple expansion/contraction, and debt paydown (deleveraging) plus any distributed cash flow, so the sources of return are explicit. **Decision:** if more than roughly half the return comes from multiple expansion or leverage rather than EBITDA growth, flag the deal as market-dependent, not operationally driven.
7. Run cases and sensitivities. Produce base, bull, and bear cases, then two-way sensitivity tables — exit multiple × EBITDA growth (or CAGR), and leverage × exit multiple — reporting MOIC and IRR in each cell. Identify the assumptions the answer is most fragile to.

## Example

A sponsor buys a services business at $50m LTM EBITDA on a 10.0x entry multiple: entry EV = $500m. It funds the deal with 5.0x leverage ($250m debt) and $260m of equity ($250m EV net of debt, plus ~$10m of fees). Over a 5-year hold, EBITDA grows to $80m (roughly 10% CAGR via commercial excellence and two bolt-ons), free cash flow sweeps net debt from $250m down to $120m, and the sponsor exits at a conservative 10.0x — flat to entry. Exit EV = $80m × 10.0x = $800m; exit equity = $800m − $120m = $680m. MOIC = $680m / $260m = 2.6x; over 5 years that is roughly a 21% gross IRR (2.6^(1/5) − 1). The value-creation bridge attributes the ~$420m equity gain to EBITDA growth (the largest slice), zero from multiple expansion (flat multiple, deliberately), and the remainder to deleveraging — an operationally driven return that survives IC scrutiny. The bear case (EBITDA flat at $50m, exit at 9.0x, slower paydown) still returns ~1.5x, clearing the fund's cost of capital; the bull case (12% CAGR, 11.0x exit) reaches ~3.4x.

## Pitfalls

- **Underwriting multiple expansion.** Assuming you sell higher than you bought is the easiest way to flatter a model and the first thing IC challenges. Default the exit multiple at or below entry and make any expansion an explicit, evidenced bet — otherwise the return is the market's, not yours.
- **Mismatched EBITDA definitions.** Using adjusted/pro-forma EBITDA at entry but a stricter number at exit (or vice versa) fabricates return. Hold one definition — LTM, NTM, or normalized — constant across entry, hold, and exit, and reconcile every add-back.
- **Leverage masquerading as skill.** High entry leverage inflates IRR but concentrates return in financial engineering and raises the odds the bear case breaches a covenant. Show the bridge so the leverage contribution is visible, and stress the downside against the debt.
- **Confusing gross and net.** Deal-level (gross) MOIC/IRR ignore management fees and carried interest; LPs receive net returns, which can be several IRR points lower. Report both and label which hurdle each is measured against.
- **A cash-flow-free exit.** Setting exit net debt as a plug rather than deriving it from projected free-cash-flow sweep breaks the deleveraging leg of the bridge and overstates equity value. Let the operating case drive paydown.

## Output format

```
# Returns Analysis — <company> — <date> — v<n>
Entry EBITDA: <$> (LTM | NTM | normalized)   Entry multiple: <x>   Hold: <n> yrs
Entry EV: <$>   Net debt at close: <$>   Invested equity: <$>

## Cases (gross unless noted)
| Case  | EBITDA CAGR | Exit EBITDA | Exit multiple | Exit net debt | Exit equity | MOIC | IRR |
|-------|-------------|-------------|---------------|---------------|-------------|------|-----|
| Bear  |             |             |               |               |             |      |     |
| Base  |             |             |               |               |             |      |     |
| Bull  |             |             |               |               |             |      |     |

Gross vs net (base): gross MOIC <x> / IRR <%> ; net MOIC <x> / IRR <%>

## Value-creation bridge (base, equity gain)
| Lever                         | $ contribution | % of gain |
|-------------------------------|----------------|-----------|
| EBITDA growth                 |                |           |
| Multiple expansion/(contraction) |             |           |
| Debt paydown (deleveraging)   |                |           |
| Free cash flow / dividends    |                |           |
| Total equity gain             |                |           |

## Sensitivity — MOIC / IRR
Exit multiple (cols) × EBITDA CAGR (rows)
|          | 8.0x | 9.0x | 10.0x | 11.0x |
|----------|------|------|-------|-------|
| 5%       |      |      |       |       |
| 8%       |      |      |       |       |
| 10%      |      |      |       |       |
| 12%      |      |      |       |       |

Leverage (cols) × exit multiple (rows) — same grid.

## Key drivers & fragility
- Answer most sensitive to: <assumption>
- Deal is <operationally driven | market/leverage dependent> because <bridge split>
```

## Reference

Substantive overview of PE returns mechanics. Figures are illustrative; every input must be grounded in diligence and the operating model, and net returns depend on the specific fund's fee and carry terms.

### The core valuation identities

The returns model rests on a short chain of identities applied at entry and exit:

| Quantity | Formula |
|----------|---------|
| Enterprise value (EV) | EBITDA × EV/EBITDA multiple |
| Equity value | EV − net debt (net debt = gross debt − cash) |
| Invested equity | Entry equity value + fees/transaction costs (+ co-invest) |
| MOIC (multiple of invested capital) | Total value to equity / invested equity |
| IRR | Discount rate that sets the NPV of equity cash flows to zero |

MOIC (also "multiple of money," MoM) is a cash-on-cash multiple that ignores timing; IRR annualizes and is timing-sensitive. They are two views of the same cash flows.

### The MOIC–IRR–hold relationship

For a single entry and single exit with no interim cash flows, MOIC and IRR are linked by the hold period:

- MOIC ≈ (1 + IRR)^years, equivalently IRR ≈ MOIC^(1/years) − 1
- Rule of 72: an investment doubling (2.0x MOIC) implies IRR ≈ 72 / years (e.g. ~14% over 5 years, ~24% over 3 years)

| MOIC | 3-yr hold | 5-yr hold | 7-yr hold |
|------|-----------|-----------|-----------|
| 1.5x | ~14% | ~8% | ~6% |
| 2.0x | ~26% | ~15% | ~10% |
| 2.5x | ~36% | ~20% | ~14% |
| 3.0x | ~44% | ~25% | ~17% |

The table shows why time is the enemy of IRR: the same 2.5x is a strong 36% IRR in three years but a mediocre 14% over seven. Interim distributions (dividend recaps, partial exits) raise IRR relative to MOIC by pulling cash forward.

### Gross vs net returns

| Measure | What it reflects | Who cares |
|---------|------------------|-----------|
| Gross (deal-level) | Return on invested equity before fund fees and carry | Deal team, IC |
| Net (fund-level, to LPs) | After ~2% management fee, ~20% carried interest over an ~8% preferred return/hurdle, and fund expenses | Limited partners |

The spread between gross and net is meaningful — a 25% gross IRR can land near 18–20% net depending on fee load, fund pacing, and the carry waterfall. Always state which basis a number is on.

### The value-creation bridge

The bridge decomposes the change in equity value from entry to exit into its sources. It is the single most scrutinized exhibit because it separates operational value creation from financial engineering and market beta:

| Lever | Mechanism | Quality of return |
|-------|-----------|-------------------|
| EBITDA growth | More revenue and/or higher margin → higher EV at any multiple | Highest — reflects real operating improvement |
| Multiple expansion | Selling at a higher EV/EBITDA than paid (scale, de-risking, mix shift, or hotter market) | Mixed — partly earned (de-risking), partly market timing |
| Debt paydown / deleveraging | Free cash flow reduces net debt, shifting EV from lenders to equity | Solid but financing-driven; depends on cash generation |
| Free cash flow / dividends | Interim distributions to equity during the hold | Real; improves IRR via timing |

A rough attribution: EBITDA-growth contribution ≈ (exit EBITDA − entry EBITDA) × entry multiple; multiple-expansion contribution ≈ (exit multiple − entry multiple) × exit EBITDA; deleveraging contribution ≈ reduction in net debt over the hold. The three plus interim cash flows reconcile to the total equity gain. IC generally rewards deals where EBITDA growth dominates the bridge.

### The effect of leverage

Leverage amplifies equity returns in both directions. Buying $500m of EV with $250m of debt means the equity ($250m) captures the full EV appreciation while the debt is repaid at par — so a given percentage rise in EV produces a larger percentage rise in equity. The cost: interest reduces free cash flow, covenants constrain operating flexibility, and in the bear case a modest EBITDA decline can breach leverage or interest-cover tests. Higher entry leverage therefore raises IRR and risk together; a robust model shows the return with leverage in the bridge and confirms the bear case services its debt.

### Cases and sensitivities

Underwrite three cases — base (the plan), bull (upside if levers over-deliver), and bear (downside that still must clear the hurdle or at least return capital) — varying EBITDA trajectory, exit multiple, and sometimes leverage and hold. Then run two-way sensitivity tables, because point estimates hide fragility:

- Exit multiple × EBITDA growth — the two largest swing factors on exit equity value.
- Leverage × exit multiple — isolates how much of the return is financing-dependent.

Report MOIC and IRR in each cell and name the assumption the answer is most fragile to. A deal whose base case clears the hurdle only on aggressive multiple expansion or maximum leverage is a market bet, not an operating thesis, and should be labeled as such.
