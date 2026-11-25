---
name: residual-screen
description: >
  Rank a US stock against its sector and the universe on factor and residual-risk
  metrics, run a cross-sectional percentile/decile screen, or pull the aggregate L3
  residual mean-reversion (Lstar) signal across a basket. Use when asked where a name
  sits in its peer group, to screen the cross-section on a metric, or for a residual
  stat-arb signal.
argument-hint: "[ticker or basket: TICKER TICKER ...]"
---

# Rankings & residual signal

Report where a name sits in the cross-section and the aggregate residual signal for a
basket. This skill wraps the hosted RiskModels MCP and reports tool outputs; it
computes nothing itself.

## What to call

- **`riskmodels_get_rankings`** — one ticker's percentile within its sector and the
  universe for a metric (factor exposures, residual risk, vol, etc.).
- **`riskmodels_screen_rankings`** — the full cross-sectional percentile/decile screen,
  ranked server-side, when the user wants "top/bottom N on X" across the universe.
- **`riskmodels_get_residual_signal`** — the aggregate L3 residual mean-reversion
  (stat-arb) signal across a basket, built on the idiosyncratic (residual) return the
  cascade isolates.

Fan out independent calls in one turn.

## How to present

- Lead with the one-line answer (where the name lands, or the top of the screen), then
  put the ranked rows in a table below.
- Residual metrics describe the stock-specific component the ERM3 cascade isolates —
  the part not explained by market/sector/subsector factors.
- The residual-reversion signal is a realized statistical signal, not a forecast of
  price. Describe what it measures; do not turn it into a buy/sell call.

## Boundary

You are an analyst, not an investment adviser. Report ranks and signals as model
outputs; never phrase them as recommendations, targets, or trades. Always call the
tools before quoting figures — never invent ranks or signal values.

## Example prompts

- `/residual-screen NVDA`
- "Where does XOM rank on residual risk within energy and the whole universe?"
- "Screen the universe for the highest residual-risk names."
- "What's the residual-reversion signal across NVDA, AMD, AVGO, MU?"
