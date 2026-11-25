---
name: tradingview-quantitative
description: Use TradingView MCP data to conduct structured quantitative research across individual equities, option overlays, ETF holdings look-through, opportunity discovery, market and macro context, event studies, portfolios, and signal validation. Use this skill when the task requires combining multiple data types into an evidence-based analysis.
---

# TradingView Quantitative Research

Use available TradingView MCP tools as a data layer. This skill defines how to frame the research question, combine data, test competing explanations, and communicate conclusions. Do not reproduce MCP API documentation or treat a single indicator as an analysis.

## Choose a research mode

- **Equity research**: one company’s trend, catalysts, valuation, and invalidation risks. Read `references/equity-research.md`.
- **Options and ETF structure**: listed chain vs live contract quote; fund AUM and holdings vs related ETF tickers. Read `references/options-and-etf.md`.
- **Opportunity discovery**: turn an investment hypothesis into a multi-factor candidate search. Read `references/opportunity-screening.md`.
- **Market and macro research**: explain regime, breadth, rotation, macro drivers, and cross-asset implications. Read `references/market-macro-research.md`.
- **Event study**: measure an event’s effect before and after it occurs. Read `references/event-study.md`.
- **Portfolio and risk**: evaluate exposures, concentration, correlation, drawdown, and position risk together. Read `references/portfolio-risk.md`.
- **Signal validation**: test whether a technical, fundamental, or event rule has historical evidence. Read `references/signal-validation.md`.
- **Strategy research and backtesting**: turn a rule into a measurable strategy and test robustness. Read `references/strategy-research.md`.
- **Trade execution**: assess liquidity, spread, slippage, and whether a signal is executable. Read `references/execution-analysis.md`.
- **Monitoring and triggers**: turn strategy, portfolio, and event conditions into state-change alerts. Read `references/monitoring-and-alerts.md`.

Use `references/analysis-framework.md` for shared evidence, uncertainty, and scoring rules, and `references/output-templates.md` for the chat summary. For a formal report, also read `references/visual-report.md` and write a portable HTML research board. Do not treat a Cursor canvas as the deliverable.

If the required TradingView MCP tools are not available, read `references/mcp-install.md` first to configure and verify the hosted MCP connection.

## Operating rules

1. Resolve the instrument, market, currency, timeframe, and user objective before collecting data.
2. Build a small evidence plan, then combine relevant MCP data sources.
3. Keep facts, derived metrics, interpretations, and recommendations visibly separate.
4. Record the analysis timestamp, data window, market session, missing fields, and assumptions.
5. Cross-check important conclusions with an independent data type. State conflicts or stale data.
6. Prefer conditional conclusions with invalidation conditions over unconditional buy/sell labels.
7. Respect rate limits and use the smallest dataset that answers the question.
8. If required MCP tools are unavailable, explain that the analysis cannot run; do not guess or fabricate data.
9. Formal reports write JSON, then `scripts/render_research_board.py`, then a short chat summary with the HTML path. Skip the board for quote lookups or when files cannot be written.

## Scope

This is a research and decision-support workflow. It does not provide personalized investment advice or guarantee returns.
