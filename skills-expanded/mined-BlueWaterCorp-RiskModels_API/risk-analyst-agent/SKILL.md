---
name: risk-analyst-agent
description: Build agents on RiskModels L3 risk data via MCP and the artifact registry. Use when wiring Cursor/Claude to decompose equities, render deterministic fund/filer panels, or document a Risk Analyst example.
---

# Risk Analyst Agent (RiskModels substrate)

## Discovery

1. Read https://riskmodels.app/llms.txt
2. Install MCP and the five skills: `RISKMODELS_API_KEY=… npx -y riskmodels@latest install`
3. Prefer MCP tools `riskmodels_*` over inventing REST paths

## Core tools

| Goal | Tool |
|------|------|
| Single-name L3 snapshot | `riskmodels_decompose` or chat `get_risk_metrics` |
| Compare names | `riskmodels_compare` |
| Weighted portfolio | `riskmodels_get_portfolio_risk_snapshot` / `compute_portfolio_risk_index` |
| Deterministic chart/table JSON | `riskmodels_render_artifact` |
| Resolve fund | `search_funds` → `BW-FUND-…` |
| Resolve 13F filer | `search_filers` → `BW-FILER-…` |

## render_artifact contract

- **slug**: `top_holdings_erm_stacked`, `cumulative_return_strip`, `narrative_profile`, `narrative_perf_insight`, `narrative_risk_insight`, plus filer panels (`entity_header`, `risk_summary_panel`, …)
- **subject_id**: `BW-FUND-*`, `BW-FILER-*`, or `BW-PORTFOLIO-*` with `subject_payload.positions` for pasted books
- **as_of**: `latest` for funds; filers often need explicit `YYYY-MM-DD`
- **format**: `json` for chat (default); `png`/`svg` return base64

## Rules

- Fan out independent ticker/fund calls in **one** tool round when possible (API executes them in parallel).
- Never fabricate metrics — call tools first.
- Hedge ratios are **dollars of ETF per $1 of stock**; ER values are variance fractions in `[0,1]`.
- Do not recommend trades; show decomposition and mechanical hedge math only.

## Reference

Full README: `examples/agents/risk-analyst-agent/README.md` in RiskModels_API.
