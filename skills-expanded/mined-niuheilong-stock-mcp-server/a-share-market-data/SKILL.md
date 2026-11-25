---
name: a-share-market-data
description: Answer questions about mainland China A-share stocks (Shanghai, Shenzhen, Beijing) using live quotes, historical K-line bars and ticker search. Use when the user asks about a Chinese listed company, a 6-digit A-share ticker, 上证/深证/创业板/科创板/北交所, market indices, price moves, volume, valuation multiples, or wants a quick market briefing. Do not use for US/HK stocks, crypto, or macro forecasting.
license: MIT
---

# A-share market data

You have access to the **Qinglong** MCP server, which returns real-time mainland
China A-share data from Tencent Finance's public endpoints.

## Prerequisite check

The MCP server exposes these tools:

| Tool | Use it for |
|---|---|
| `get_stock_quote` | One ticker: price, change, high/low, volume, turnover, PE, PB, cap, limit prices |
| `get_stock_quotes` | 2–50 tickers at once (watchlists, comparisons) |
| `get_stock_kline` | Price history: `period=day/week/month`, `count` 1–320, `adjust=qfq/hfq/none` |
| `search_stock` | Resolve a name or pinyin to a ticker before querying |
| `get_market_indices` | SSE Composite, SZSE Component, ChiNext, STAR 50, CSI 300 |
| `check_data_source` | Upstream is reachable (use before blaming the data) |

If none of these tools are available, tell the user to install the server:

```bash
claude mcp add qinglong -- uvx --from git+https://github.com/niuheilong/stock-mcp-server qinglong-mcp
```

Then ask them to restart the agent. Do not guess prices.

## Workflow

1. **Resolve the ticker.** If the user gives a name or pinyin, call `search_stock`
   first. Never assume a code from memory — codes get confused (e.g. 600410 vs 000410).
2. **Pick the smallest tool that answers the question.** One price → `get_stock_quote`.
   Several → `get_stock_quotes`. Trend/technical question → `get_stock_kline`.
   "How is the market" → `get_market_indices`.
3. **Fetch before you describe.** Every numeric claim must come from a tool result in
   this turn. If a call errors, report the error — never fill the gap with memory.
4. **State the timestamp.** Include the `quote_time` from the response. If it is far
   behind the current time, say the market is likely closed or the feed is stale.

## Reading the numbers

- **Units**: price in CNY; `volume_lots` in lots (1 lot = 100 shares);
  `amount_10k_cny` in 10k CNY; `market_cap_100m_cny` in 100m CNY.
- **Price limits**: ±10% for main-board stocks, ±20% for ChiNext (300xxx) and
  STAR (688xxx), ±30% for Beijing Stock Exchange (4xxxxx/8xxxxx), ±5% for ST stocks.
  If `price == limit_up` or `price == limit_down`, say the stock is at the limit.
- **Turnover** (`turnover_percent`): under 1% is quiet, 1–3% normal, above 5% is
  heavy activity. Combine it with the day's `change_percent` — a big move on low
  turnover is weak conviction.
- **Volume context**: compare today's `volume_lots` with the average of the last
  20 bars from `get_stock_kline`. Only call a move "volume-confirmed" if the ratio
  is roughly ≥1.5×.
- **Valuation**: `pe_ttm` is meaningless for loss-making companies — if it is
  negative or absurdly high, say so instead of quoting it as a multiple. Compare
  `pb` within the same industry, never across sectors.
- **Suspensions**: an empty or stale quote usually means the stock is halted. Say
  "可能停牌/无行情" rather than presenting an old price as current.

## Output shape

For a single-stock question, answer in this order, compactly:

1. **Name (code)** — price, change %, timestamp
2. **Day range** — open / high / low, volume vs 20-day average
3. **Valuation** — PE(TTM), PB, market cap (only if meaningful)
4. **Context** — recent trend from the last 5–20 closes
5. **Caveat** — market state (open/closed), data source delay

Keep it to a short table or 4–6 lines. Users asking about A-shares usually want the
numbers, not an essay.

## Hard rules

- **Never give buy/sell/hold advice or price targets.** You may describe what the
  data shows; you may not recommend a position.
- **Never invent** a price, percentage, financial metric or news item.
- If the user asks "why" a stock moved, you do **not** have news data — say the
  data feed does not include news, and offer the price/volume facts you do have.
- Do not present this data as exchange-grade or real-time tick data; it is delayed
  by seconds and is for research only.

## Example

User: *"贵州茅台今天怎么样？"*

```
search_stock("贵州茅台")            → sh600519
get_stock_quote("sh600519")        → price 1680.00, +2.35%, high 1692.00, low 1641.10
get_stock_kline("sh600519","day",20) → compare volume with 20-day average
```

Answer:

| Item | Value |
|---|---|
| 贵州茅台 (600519) | ¥1,680.00 · **+2.35%** · 14:32 |
| Day range | 开 1,645.00 / 高 1,692.00 / 低 1,641.10 |
| Volume | 12.5万手（约 1.4× 20日均量） |
| Valuation | PE(TTM) 28.5 · PB 8.1 · 市值 2.11万亿 |

> 数据来自腾讯财经公开接口，有秒级延迟；行情数据不构成投资建议。
