---
name: mongodb-financial-analysis
description: >-
  Analyze Indian market financial data from local MongoDB via MCP for intraday,
  short-term, and long-term price targets. Use when querying OHLCV candles,
  computing support/resistance, setting trade targets, or generating multi-timeframe
  analysis reports from MongoDB.
---

# MongoDB Financial Analysis

Analyze NSE/BSE market data stored in local MongoDB using the MongoDB MCP server. Produces structured analysis with price targets across three horizons: **intraday**, **short-term**, and **long-term**.

**Prerequisite:** MongoDB MCP must be connected. If not, use the **mongodb-local-mcp** skill first.

## Time Horizon Definitions

| Horizon | Holding period | Data source | Primary use |
|---------|---------------|-------------|-------------|
| **Intraday** | Same session (exit by 3:30 PM IST) | `candles_intraday` (1m/5m/15m) | Scalping, day trading, F&O intraday |
| **Short-term** | 1–20 trading days | `candles_daily` (20–60 days) | Swing trades, momentum, post-earnings |
| **Long-term** | 1–12+ months | `candles_daily` / `candles_weekly` (6mo–5yr) | Position trades, investment targets |

All prices in **INR (₹)**. Trading hours: 9:15 AM – 3:30 PM IST.

## Workflow

When the user requests analysis, determine scope and follow the matching workflow.

```
Task Progress:
- [ ] Step 1: Discover schema (if not already known)
- [ ] Step 2: Fetch required candle data via MCP
- [ ] Step 3: Run horizon-specific analysis
- [ ] Step 4: Compute support, resistance, and targets
- [ ] Step 5: Present report using template
```

### Step 1: Discover Schema

Unless schema is known from a prior session:

1. `list-collections` on the trading database
2. `collection-schema` on candle collections
3. Sample 5 documents with `find` to confirm field names

See [../mongodb-local-mcp/references/schema-conventions.md](../mongodb-local-mcp/references/schema-conventions.md) for expected layout.

### Step 2: Fetch Data

Use MCP `find` or `aggregate`. Minimum data requirements:

| Horizon | Fetch |
|---------|-------|
| Intraday | All bars for current/requested session, interval 5m (or 15m) |
| Short-term | Last 60 daily candles |
| Long-term | Last 252 daily candles (1 year) or 104 weekly candles (2 years) |

**Example find (daily, last 60 bars):**

```json
{
  "database": "trading",
  "collection": "candles_daily",
  "filter": { "symbol": "RELIANCE", "exchange": "NSE" },
  "sort": { "timestamp": -1 },
  "limit": 60
}
```

Sort results chronologically (oldest first) before computing indicators.

---

## Analysis Type 1: Intraday Targets

Use when: "intraday levels", "today's target", "day trade setup", same-session exit.

### Data

- Collection: `candles_intraday`
- Interval: `5m` preferred (use `1m` for scalping, `15m` for broader intraday)
- Scope: Current session or specified `tradeDate`

### Compute

| Level | Method |
|-------|--------|
| **Day open** | First bar's open |
| **Day high / low** | Max high / min low of session |
| **VWAP** | Σ(typical price × volume) / Σ(volume), typical = (H+L+C)/3 |
| **Pivot (classic)** | P = (prevHigh + prevLow + prevClose) / 3; R1 = 2P − prevLow; S1 = 2P − prevHigh |
| **Intraday ATR** | ATR(14) on 5m bars × 1.0–1.5 for stop distance |
| **Opening range** | High/low of first 15–30 minutes |

### Target Rules

| Target | Calculation |
|--------|-------------|
| **T1 (conservative)** | Nearest intraday S/R or VWAP band (±0.3% from VWAP) |
| **T2 (moderate)** | Day high/low extension or pivot R1/S1 |
| **T3 (aggressive)** | 1× intraday ATR beyond breakout level |
| **Stop-loss** | Below opening range low (long) or above opening range high (short); max 0.5–1% from entry |

### Direction Bias

Score these signals (+1 bullish, −1 bearish, 0 neutral):

- Price above/below VWAP
- Higher highs + higher lows vs lower highs + lower lows (last 6 bars)
- Volume expansion on up moves vs down moves
- Position relative to day open and pivot P

**Bias:** Sum ≥ +2 → bullish; ≤ −2 → bearish; else neutral/range-bound.

---

## Analysis Type 2: Short-Term Targets

Use when: "swing trade", "1–2 week target", "short-term view", 5–20 day holding.

### Data

- Collection: `candles_daily`
- Lookback: 60 trading days

### Compute

| Indicator | Period | Use |
|-----------|--------|-----|
| SMA 20 | 20 days | Short-term trend, dynamic S/R |
| SMA 50 | 50 days | Intermediate trend filter |
| RSI 14 | 14 days | Overbought (>70) / oversold (<30) |
| ATR 14 | 14 days | Stop and target distance |
| Swing highs/lows | Last 20 days | Key S/R levels |
| 20-day high/low | 20 days | Breakout/breakdown reference |

**Swing high:** A day whose high exceeds the highs of the 2 days before and after.
**Swing low:** A day whose low is below the lows of the 2 days before and after.

### Target Rules

| Target | Calculation |
|--------|-------------|
| **T1** | Nearest swing S/R or 20 SMA (first profit book) |
| **T2** | Previous swing high (long) or swing low (short) |
| **T3** | Measured move: breakout height projected from breakout point |
| **Stop-loss** | Below recent swing low (long) or 1.5× ATR(14) |

### Trend Filter

- **Bullish swing:** Close > 20 SMA > 50 SMA, RSI 40–65
- **Bearish swing:** Close < 20 SMA < 50 SMA, RSI 35–60
- **Avoid:** RSI > 75 (extended) or < 25 (falling knife) unless mean-reversion setup

---

## Analysis Type 3: Long-Term Targets

Use when: "investment target", "6-month view", "long-term levels", position sizing.

### Data

- Collection: `candles_daily` (252+ days) or `candles_weekly` (104+ weeks)
- Optional: `fundamentals` for valuation context

### Compute

| Indicator | Period | Use |
|-----------|--------|-----|
| SMA 50 / 200 | 50, 200 days | Golden/death cross, trend |
| 52-week high/low | 252 days | Structural S/R |
| Trend channel | 6-month regression | Upper/lower bounds |
| Fibonacci ext | From major swing low → high | 1.272, 1.618 extensions |
| Relative strength | vs Nifty 50 same period | Leadership/laggard |

**52-week metrics:**

- Distance from 52w high: `(52wHigh − close) / 52wHigh × 100`
- Distance from 52w low: `(close − 52wLow) / 52wLow × 100`

### Target Rules

| Target | Calculation |
|--------|-------------|
| **T1** | 52-week high (if in uptrend) or upper trend channel |
| **T2** | Fib 1.272 extension of last major swing |
| **T3** | Fib 1.618 extension or measured move from base |
| **Stop / invalidation** | Close below 200 SMA (long-term longs) or 52-week low breach |

### Fundamental Overlay (if `fundamentals` exists)

Query latest snapshot via MCP `find`. Add context:

- PE vs sector median → expensive/cheap
- ROE trend → quality filter
- Promoter holding change → governance signal

Do not replace technical targets with fundamental price targets unless user asks for valuation-based targets.

---

## Multi-Timeframe Report

When the user asks for full analysis (no specific horizon), run all three and synthesize.

**Alignment scoring:**

| Alignment | Condition | Implication |
|-----------|-----------|-------------|
| **Strong** | All three horizons same direction | Higher conviction |
| **Mixed** | Intraday vs daily conflict | Wait for alignment or trade smaller size |
| **Divergent** | Long-term up, short-term down | Pullback in uptrend (buy dips) or vice versa |

Output using [assets/multi-timeframe-report-template.md](assets/multi-timeframe-report-template.md).

---

## MCP Aggregation Examples

### VWAP for intraday session

```javascript
[
  { $match: { symbol: "RELIANCE", interval: "5m", tradeDate: "2026-06-20" } },
  { $sort: { timestamp: 1 } },
  { $group: {
      _id: null,
      vwap: { $avg: { $divide: [{ $add: ["$high", "$low", "$close"] }, 3] } },
      dayHigh: { $max: "$high" },
      dayLow: { $min: "$low" },
      totalVolume: { $sum: "$volume" }
  }}
]
```

### 20-day SMA (short-term)

```javascript
[
  { $match: { symbol: "TCS", exchange: "NSE" } },
  { $sort: { timestamp: -1 } },
  { $limit: 20 },
  { $group: { _id: null, sma20: { $avg: "$close" } } }
]
```

### 52-week high/low (long-term)

```javascript
[
  { $match: { symbol: "INFY", exchange: "NSE" } },
  { $sort: { timestamp: -1 } },
  { $limit: 252 },
  { $group: {
      _id: null,
      high52w: { $max: "$high" },
      low52w: { $min: "$low" },
      latestClose: { $first: "$close" }
  }}
]
```

Adapt collection/field names to discovered schema.

---

## Output Rules

1. Always state **data source** (collection, date range, bar count)
2. Show **current price** and **analysis timestamp**
3. List **3 targets + stop-loss** per horizon with ₹ values
4. Include **risk:reward** ratio for each setup (min 1:1.5 preferred)
5. Note **circuit limit** proximity for individual stocks (within 2% of upper/lower circuit)
6. Add disclaimer: educational analysis, not SEBI-registered advice

## Supplementary Data

If MongoDB data is insufficient:

- Use **india-stock-analysis** skill with Groww/Kite MCP for live LTP and fundamentals
- Use **technical-analyst** skill for chart image analysis
- Use web search for earnings dates, corporate actions, news catalysts

## Additional Resources

- Query patterns: [../mongodb-local-mcp/references/mcp-tools.md](../mongodb-local-mcp/references/mcp-tools.md)
- Schema conventions: [../mongodb-local-mcp/references/schema-conventions.md](../mongodb-local-mcp/references/schema-conventions.md)
- Report template: [assets/multi-timeframe-report-template.md](assets/multi-timeframe-report-template.md)
- Target methodology detail: [references/target-methodology.md](references/target-methodology.md)
