---
name: risk-decompose
description: >
  Decompose a US stock's risk into market, sector, subsector, and stock-specific
  (residual/idiosyncratic) components using the RiskModels ERM3 cascade (L1/L2/L3),
  with the tradeable ETF hedge ratios each layer implies. Use when asked what is
  driving a name's risk, how idiosyncratic it is, or what an ETF hedge of a given
  leg would mechanically neutralize.
argument-hint: "[ticker]"
---

# Risk decomposition (ERM3 L1/L2/L3)

Decompose the risk of a single US equity into a nested cascade and report the ETF
hedge ratios it implies. This skill is a thin wrapper over the hosted RiskModels
MCP — it calls live tools and reports their outputs. It computes nothing itself.

## What to call

Resolve the symbol first if the user gave a company name (`riskmodels_search`),
then:

- **`riskmodels_get_stock_snapshot`** — the latest snapshot (hedge ratios, ER fractions,
  vol, close) with the L1/L2/L3 `hedge_levels` block side by side (hedge ratios +
  explained-risk fractions + the ETF legs at each depth). Best for "how does the
  decomposition deepen from market-only to subsector?" and for the current numbers.
- **`riskmodels_decompose`** — the L3 four-bet decomposition (market / sector /
  subsector / residual) for one name. Best for "what is driving this stock's risk?"

Fan out independent calls in one turn.

## How to read the outputs

- **Explained risk (`*_er`)** are variance fractions that sum to ~1.0 at L3
  (`l3_mkt_er + l3_sec_er + l3_sub_er + l3_res_er`). Use these — not hedge-ratio
  signs — to say where variance lives. A high residual ER (>0.5) means much of the
  risk is stock-specific and not hedgeable with sector/market ETFs.
- **Hedge ratios (`*_hr`)** are model outputs: dollars of an ETF leg that mechanically
  neutralize $1 of a given layer of risk. Report them as math, e.g. "$0.62 of SPY per
  $1 of position neutralizes the market leg."
- **A negative L3 market hedge ratio is not "negative market exposure."** At L2/L3 the
  sector and subsector ETF legs already carry market beta; the SPY leg often offsets
  beta embedded in those legs (orthogonalization), not a separate short-macro story.
  Never infer market stance from the sign of `l3_market_hr` — read `l3_mkt_er`.

## Boundary

You are an analyst, not an investment adviser. Report the decomposition and what each
hedge leg would mechanically neutralize; never recommend a trade, rebalance, or
assess whether the position is suitable. Always call the tools before stating any
number — never invent figures.

## Example prompts

- `/risk-decompose NVDA`
- "How idiosyncratic is PLTR — how much of its risk is stock-specific?"
- "Show me the L1 vs L2 vs L3 decomposition for XOM and what each ETF leg hedges."
