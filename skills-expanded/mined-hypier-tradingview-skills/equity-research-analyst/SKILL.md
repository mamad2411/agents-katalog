---
name: equity-research-analyst
description: Use when the user asks for institutional-style equity research on a public company, ETF, or TradingView-resolvable ticker, including initiation reports, earnings updates or previews, catalyst calendars, morning notes, sector or peer overviews, thesis reviews, model refreshes, and stock screening or idea generation. Requires hosted TradingView MCP (https://mcp.tradingviewapi.com/mcp); install per IDE from this skill's mcp-install reference (Cursor, VS Code, Claude Code, Claude Desktop, Codex, Gemini, Windsurf).
---

# Equity Research Analyst

Produce institutional-grade equity research deliverables through the selected workflow. Each workflow has a dedicated reference file in `references/workflows/`; this SKILL.md is the dispatcher and the hub for cross-workflow conventions.

**This skill only runs when hosted `tradingview_*` MCP tools are available.** Do not ask for an API key and do not construct REST curls. If those tools are missing, stop researching, read **[references/mcp-install.md](references/mcp-install.md)**, and give **only the install section for the user's IDE**. Do not dump every client.

- Console: `https://mcp.tradingviewapi.com/mcp` with `"type": "http"`, then sign in. One-click: https://www.tradingviewapi.com/mcp/
- Per-IDE steps (Cursor, VS Code, Claude Code, Claude Desktop, Codex, Gemini, Windsurf) and JWT fallback: **[references/mcp-install.md](references/mcp-install.md)**
- Local `npx -y @ivotoby/openapi-mcp-server` exposes REST-shaped tools, not `tradingview_*` — switch to `tradingview-api-integration` instead of this skill.

## Loading Strategy

Keep context tight and load only the files needed for the active task.

1. Match the request to exactly one workflow in `references/workflows/`.
2. Read only that workflow file first.
3. Open deep-dive references only when the active workflow points to them.
4. Read `references/mcp-research-data-guide.md` when the workflow needs detailed MCP data mapping. Do not load API snapshots or REST documentation.

### `tradingviewapi` lookup guide

- Use `references/mcp-research-data-guide.md` for task-to-MCP-tool mapping and research field guidance.
- Live data comes from the available `tradingview_*` tools; use their schemas and returned payloads as the source of truth.
- Do not construct REST requests or rely on bundled API snapshots.
- Search patterns that usually find the right payload example quickly:
  - `GET /api/market-data/{symbol}` (payload shape only)
  - `earnings_release_next_date`
  - `analyst-recommendations`

## Equity analyst deep dives

For an initiation or full company report, combine these references as needed: `references/financial-statement-analysis.md`, `references/valuation-analysis.md`, `references/peer-comparison.md`, and `references/investment-thesis.md`. They define the research questions; MCP supplies the structured data.

## When to invoke which workflow

Match the user request to one of the nine workflows below and read the corresponding reference file from `references/workflows/`. If the request is ambiguous, ask the user to confirm before committing.

| Workflow | Trigger phrases | Reference |
|---|---|---|
| **Initiating coverage** | "initiation report", "first-time coverage", "new coverage on X", "write a full report on X" | `references/workflows/initiating-coverage.md` |
| **Earnings analysis** | "earnings update", "Q1/Q2/Q3/Q4 results for X", "post-earnings report", "beat/miss analysis" | `references/workflows/earnings-analysis.md` |
| **Earnings preview** | "earnings preview", "what to watch in X's earnings", "pre-earnings note" | `references/workflows/earnings-preview.md` |
| **Catalyst calendar** | "catalyst calendar", "upcoming events", "earnings calendar", "event tracker" | `references/workflows/catalyst-calendar.md` |
| **Morning note** | "morning note", "daily brief", "pre-market note", "morning wrap" | `references/workflows/morning-note.md` |
| **Sector overview** | "sector report", "industry overview", "peer comp", "sector deep-dive" | `references/workflows/sector-overview.md` |
| **Thesis tracker** | "thesis tracker", "investment thesis review", "revisit thesis on X", "thesis check" | `references/workflows/thesis-tracker.md` |
| **Model update** | "update the model", "model maintenance", "refresh estimates", "re-forecast" | `references/workflows/model-update.md` |
| **Idea generation** | "screen for X", "find me stocks that", "idea generation", "investment ideas" | `references/workflows/idea-generation.md` |

### Single-workflow discipline (especially for `initiating-coverage`)

The initiation-report workflow has five sequential tasks (Company Research → Financial Modeling → Valuation → Charts → Assembly). Execute **one task per user request**, verify prerequisites before the next task, and never auto-chain. Details in `references/workflows/initiating-coverage.md`.

## Primary data source: hosted TradingView MCP

Before Web Search, pull structured numeric data (financials, TTM ratios, analyst consensus, calendars, prices, technicals, news) through `tradingview_*` tools. **One call to `tradingview_get_market_data(symbol, category='all')` covers ~70% of the numeric content of a typical research report.**

- Tool map and research field guidance: `references/mcp-research-data-guide.md`

**Use Web Search ONLY for narrative content**: MD&A text, forward guidance wording, earnings call transcripts, segment breakdowns, risk factors, management bios, industry research, FDA/regulatory decisions. Pull raw SEC 10-K/10-Q only when direct quotation or audit is required.

## Global conventions

### Data freshness
- Training data is outdated. Before writing, verify today's date and confirm that the latest fetched data is current (next earnings date, last reported quarter).
- If `data.current.fiscal_period_current` is >90 days old, flag as "last reported" and Web Search for newer disclosures.
- Treat `data.current.fiscal_period_current` as a structured provider label, not the final narrative quarter label. If company IR / SEC naming differs (for example provider `2025-Q4` vs company-reported `Fiscal 2026 Q4`), use the latest primary-source wording in the written report and cite that source explicitly.

### Ticker resolution
- Always use `EXCHANGE:TICKER` format (e.g., `NASDAQ:AAPL`, `NYSE:JPM`).
- If the user supplies only a company name, resolve it via `tradingview_search_market(query, filter='stock')` before proceeding.
- Use the resolved symbol from search as the canonical identifier for the workflow. Do not rely on `data.company.ticker` or `data.company.exchange` from `tradingview_get_market_data` as the canonical listing identifier, because those fields may be null or may reflect a quote venue rather than the primary exchange.

### Calendar windows
- For a named coverage list, use `tradingview_get_earnings_calendar` or `tradingview_get_dividends_calendar` with `symbols` (1–50) and optional inclusive ISO `date_from` / `date_to`.
- For a market-wide calendar, `tradingview_get_calendar` requires Unix-seconds integers for `from` and `to`. Never pass empty strings, `"now"`, or `"now+14days"`.
- Compute `from = Math.floor(Date.now() / 1000)` and `to = from + 14 * 86400` (or up to 30 days). Max span is 40 days.
- English/US prompts default to `market='america'`. Add `china` only when the user asked for A-shares or China macro.

### Sector and idea screens
- Do **not** use leaderboard `tab` / `columnset` as a sector filter. Leaderboard does not filter by sector.
- Discover exact sector strings with `tradingview_get_screener_filter_options(asset_type='stock', ids=['sector'])`, then call `tradingview_screen_assets`. `NASDAQ:AAPL` is `Electronic Technology`, not `Technology`.
- Leaderboard `columnset` is camelCase (`incomeStatement`, `balanceSheet`, `cashFlow`, `technicals`). Screener `preset_fields` stay snake_case (`income_statement`, `technicals`).

### Price series
- Real market prices, returns, and report charts: `tradingview_get_ohlcv` (Japanese candles). Do not use `tradingview_get_price` unless the user asked for Heikin-Ashi or Range.

### Citation standard
Every numeric fact in a deliverable must cite its source:

```
Source: Structured data via TradingView MCP; fetched [YYYY-MM-DD]
        Tool: tradingview_get_market_data(symbol='NASDAQ:AAPL', category='all')
        Fiscal period: 2026-Q1
```

SEC filings keep separate EDGAR hyperlinks. For consensus data, cite the tool that supplied the figures, such as `tradingview_get_forecasts` or `tradingview_get_market_data(..., category='analyst_recommendations')`.

### Output formatting
- Default font for Word deliverables: **Times New Roman**.
- Do **not** add emojis to research reports unless the user explicitly requests them.
- Follow the page/structure templates in `assets/initiating-coverage/report-template.md` for initiation reports.
- Use `references/initiating-coverage/quality-checklist.md` for final initiation-report QA.
- Other workflows use the template embedded in their own reference file.

### No shortcuts
- Deliver exactly the outputs specified in each workflow reference. Do **not** create extra "completion summaries", "executive summaries", or "quick reference guides".
- Do not fabricate data. Missing field → "N/A". Missing consensus → state "consensus not available".

## Fallback strategy
1. Hosted `tradingview_*` tools missing → stop, read `references/mcp-install.md`, and give the install steps for the user's IDE. Do not request an API key.
2. Ticker unresolved → ask the user for `EXCHANGE:TICKER`.
3. Ambiguous workflow → ask the user which deliverable they want.
4. Missing field → "N/A"; do not fabricate. Stale `fiscal_period_current` (>90 days) → flag as last reported and Web Search for a newer release.
