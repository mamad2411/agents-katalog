---
name: cost-of-capital
description: >
  Compute a CAPM cost of equity, strict reported-data cost of debt / book-weight WACC,
  a separately labeled PIT-lagged high-quality-market proxy when strict debt cost is
  unavailable, and equity-charge economic profit for a US equity. Includes caller-set
  ERP / risk-free tenor inputs and an ERP × rf-tenor sensitivity
  grid. Use when asked for a name's WACC, cost of equity, hurdle rate, or economic
  profit / EVA.
argument-hint: "[ticker] [erp?] [rf_tenor?]"
---

# Cost of capital (CAPM mode)

Report a name's cost of capital from its PIT fundamentals. Cost of equity is CAPM:
risk-free rate at the chosen tenor plus the reported valuation beta times the
equity-risk-premium request assumption. WACC uses book-value weights. This skill wraps
the hosted RiskModels MCP and reports its outputs — it computes nothing itself.

## What to call

- **`riskmodels_get_fundamentals`** — the cost-of-capital layer rides on this tool.
  Relevant params:
  - **`erp`** — the equity risk premium request assumption. If the user did not give
    one, ask for it or report across the grid; state the ERP used in every answer.
  - **`rf_tenor`** — Treasury constant-maturity tenor for the risk-free rate
    (`3m|1y|2y|5y|10y|30y`, default `10y`, the long-duration valuation convention).
  - **`tax_rate`** — applied to the WACC debt shield (default 0.21).
  - **`grid=true`** with `erp_grid` / `rf_tenor_grid` — returns the sensitivity table
    of `cost_of_equity`, strict `wacc`, parallel `wacc_imputed`, and `economic_profit` across every ERP × tenor cell,
    instead of a single scalar. Prefer the grid when the user has not fixed an ERP.

## Reading the response

- **`cost_of_equity`** = `rf_rate` + `beta_market` × `erp` (CAPM). Because
  the valuation beta can be low or negative for defensive names, `cost_of_equity`
  can fall below the risk-free rate — state it plainly rather than "correcting" it.
- **`cost_of_debt` / `wacc`** are strict reported-data fields. If positive trusted
  SEC debt lacks usable TTM interest expense, both remain null — never read null as 0%.
- **`cost_of_debt_imputed` / `wacc_imputed`** are separate proxy fields. Use them only
  when `cost_of_debt_imputation.status == "used"`, label them **PIT-lagged
  high-quality-market proxy**, and report the provenance. The stored spread is monthly
  `HQMCB10YR - GS10`, then added to the separate period-end 10-year Treasury rate.
  The reference month becomes eligible on day 10 of the following month. It covers
  the A/AA/AAA high-quality market; it is not an issuer rating or issuer bond yield.
- Both WACC fields use **book-value** weights (balance-sheet equity and debt). The
  textbook convention is market-value weights; say so, and note the user can reweight
  if they have market caps.
- **`economic_profit`** scales with book equity; pair it with `roe_ttm − cost_of_equity`
  (the equity-charge spread). It is not NOPAT minus WACC times invested capital.
- A short `rf_tenor` (3m/1y) should be paired with a bill-basis ERP, or cost of
  capital is understated. Surface the tenor you used.

## Boundary

These are model outputs from realized fundamentals and request assumptions —
not a valuation opinion, price target, or recommendation. You are an analyst, not an
investment adviser. Always state the ERP, tenor, and tax rate behind any number, and
call the tool before quoting figures.

## Example prompts

- `/cost-of-capital AAPL 0.05 10y`
- "What's MSFT's WACC at a 4.5% and 5.5% ERP across the 5y and 10y risk-free?"
  (use the grid)
- "Show NVDA's cost of equity and economic profit; I'll use a 5% ERP."
