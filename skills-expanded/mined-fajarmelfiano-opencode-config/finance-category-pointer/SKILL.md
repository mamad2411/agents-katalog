---
name: finance-category-pointer
description: "Pointer to a library of 19 specialized Finance skills. Use when working on finance-related tasks."
risk: none
---

# Finance Capability Library 🎯

This is a **pointer skill**. The 19 specialized Finance skills are stored in a hidden vault to keep your startup context minimal.

## Available skills in this category

- **axonx** — Develop AxonX research plugins and operate quantitative research tasks through CLI or MCP, inspecting execution status, logs, artifacts, and lineage.
- **equibles** — Query Equibles for US stock market data: SEC filing search, XBRL financial statements, earnings call transcripts, insider and 13F holdings, and daily prices.
- **fxmacrodata** — Query FXMacroData for official-source macro indicators, release calendars, central-bank policy rates, FX rates and CFTC positioning across 22 currencies.
- **longbridge** — 125+ agent skills for Longbridge Securities — real-time quotes, charts, fundamentals, portfolio analysis, options, and more for HK/US/A-share/SG markets. Trilingual: Simplified Chinese, Traditional Chinese, English.
- **longbridge-content** — Latest news articles, regulatory filings, community discussion topics for listed stocks, and SEC EDGAR filing analysis (10-K/10-Q/8-K/proxy/Form 4) via Longbridge.
- **longbridge-derivatives** — Curated upstream guidance for Longbridge Derivatives; use when the workflow matches the user goal.
- **longbridge-fundamentals** — Financial statements, business segments, dividends, valuation multiples (PE/PB/PS), industry comparison, operating data, corporate actions, company and executive profiles, cross-stock comparison, and valuation ranking via Longbridge.
- **longbridge-market-data** — Real-time quotes, K-line charts, order book, trade ticks, intraday capital flow, market sentiment temperature, trading session schedule, security lists, exchange rates, and IPO calendar for HK/US/A-share/SG via Longbridge. Also covers ADR premium and FX carry frameworks.
- **longbridge-quant** — Curated upstream guidance for Longbridge Quant; use when the workflow matches the user goal.
- **options-flow-analyzer** — Real vs lottery call separation for options P/C ratio analysis — prevents signal inversion from deep OTM noise
- **traderspy-market-briefing** — Crypto market briefing from live TraderSpy data: majors, funding, open interest, top-trader lean, fresh AI signals and screener movers. Use for "what's happening in crypto" or a recap.
- **traderspy-market-screener** — Scan the most-traded crypto futures pairs for up to 3 technical conditions in one TraderSpy call, compare coins, and backtest what followed a condition. Use for "which coins are oversold".
- **traderspy-position-check** — Health-check crypto futures positions the user describes, with TraderSpy data: liquidation and stop distance, multi-timeframe read, funding and top-trader side. Reports only; never tells the user to close or add.
- **traderspy-smart-money** — Track what top crypto futures traders hold on Binance, Hyperliquid, Bybit and OKX with TraderSpy: elite leaderboard, positions, trader profiles and history. Use for "what are whales doing".
- **traderspy-technical-analysis** — Read one crypto futures pair with TraderSpy: 19 indicators on up to 3 timeframes in one call, key levels, funding, open interest and positioning. Use for "analyse BTC" or "is SOL oversold".
- **traderspy-trading-signals** — Fetch and explain TraderSpy's AI crypto futures signals: entry, take-profit ladder, stop, triggers, status against the live price, and how recent signals resolved. Use for "latest signals".
- **warren-buffett** — Agente que simula Warren Buffett — o maior investidor do seculo XX e XXI, CEO da Berkshire Hathaway, discipulo de Benjamin Graham e socio intelectual de Charlie Munger.
- **xvary-stock-research** — Thesis-driven equity analysis from public SEC EDGAR and market data; /analyze, /score, /compare workflows with bundled Python tools (Claude Code, Cursor, Codex).
- **yield-intelligence** — Passive income portfolio analysis — activate when user asks about dividend yields, Treasury rates, REIT income, monthly passive income goals, or portfolio yield optimization. Scans 4 asset classes, ranks by risk-adjusted return, and builds allocations targeting a specific monthly income.

## How to load a skill

1. Identify the skill name above matching your task.
2. Use `read` to load its `SKILL.md` from the vault:
   `/home/melfiano/.config/opencode/skill-libraries/finance/<skill-name>/SKILL.md`
3. Follow those instructions to complete the request.

**Vault path:** `/home/melfiano/.config/opencode/skill-libraries/finance`

> Do not guess best practices — always read from the vault first.

> ⚠️ **Anti-loop guard**: Do NOT invoke skills recursively or check for applicable skills before every response. Each skill should be loaded at most once per user request. If you have already identified and loaded the relevant skill for this task, proceed with execution — do not re-scan for skills.
