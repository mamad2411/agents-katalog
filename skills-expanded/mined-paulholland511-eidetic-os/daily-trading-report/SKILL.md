---
name: daily-trading-report
description: Daily multi-agent market research — runs analyst agents on a watchlist via a local LLM, emails a research report.
---

Run the multi-agent TradingAgents analysis for your watchlist, then email
yourself a detailed research report.

> ⚠️ Not financial advice. Research/automation output only.
>
> Placeholders: `{{USER_EMAIL}}` = recipient, `{{VAULT_PATH}}` = vault path,
> `{{EIDETIC_OS}}` = repo path, `{{EMBED_HOST}}:{{LLM_PORT}}` = local LLM endpoint,
> `{{WATCHLIST}}` = comma-separated tickers (configure per user; the example
> below uses generic crypto/equity tickers).

**Step 1 — Gather market data** with Python:
- Fetch prices via `yfinance` (30 days history) for your primary watchlist tickers
- Optionally fetch broader movers (e.g. BTC-USD, ETH-USD, SOL-USD, plus a few large-cap equities)
- Calculate per asset: RSI (14), MACD (12,26,9), SMA 20/50/200, Bollinger Bands (20,2)
- Fetch the Fear & Greed index from `https://api.alternative.me/fng/?limit=1`
- Optionally fetch market data from CoinGecko for crypto assets

**Step 2 — Run analyst agents via your local LLM** at
`http://{{EMBED_HOST}}:{{LLM_PORT}}/v1/chat/completions`:

1. **Fundamentals Analyst** — assess fundamentals for the watchlist; scan the wider market and identify the top 3 assets by fundamentals (value, growth, catalysts) with reasons
2. **Sentiment Analyst** — assess sentiment for the watchlist and the broader market; flag extreme fear (possible opportunity) or extreme greed (possible caution)
3. **News & Catalyst Analyst** — identify upcoming events/earnings/regulation/catalysts in the next 7–30 days; note assets to watch
4. **Technical Trader** — analyse watchlist technicals; identify the top 3 with the strongest technical signals (oversold RSI, MACD crossovers, BB squeezes, golden crosses); suggest entry points and stop losses
5. **Portfolio Manager** — synthesise all reports; give a final BUY/SELL/HOLD per watchlist asset with confidence %, plus a ranked "ideas to research" section

Set a timeout of ~180 seconds per agent call.

**Step 3 — Save to vault:**
Save to `{{VAULT_PATH}}/wiki/sources/trading-briefing-YYYY-MM-DD.md`
(or run `EIDETIC_TRIGGER=scheduled eidetic trading`, which writes there for you).

**Step 4 — Email the report** via `EIDETIC_TRIGGER=scheduled eidetic email --json '...'` (routes through the CLI so the run is audited):
- To: `{{USER_EMAIL}}`
- Subject: `📊 Market Research — [date]`
- Dark-themed HTML with: price cards + recommendations, technical indicators,
  Fear & Greed index, each agent report in a card, a final summary table, and a
  prominent **risk warning footer** ("Not financial advice. For research only.")
- Sign off as Eidetic.
