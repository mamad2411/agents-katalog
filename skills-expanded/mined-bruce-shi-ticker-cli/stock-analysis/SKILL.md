---
name: stock-analysis
description: Analyze stocks and cryptocurrencies using Yahoo Finance data.
homepage: https://finance.yahoo.com
metadata: {"clawdbot":{"emoji":"📈","requires":{"bins":["npx"],"env":[]}}}
---

# Stock Analysis Skill

A powerful CLI tool for trading analysis that provides stock quotes, charts, technical indicators, news, and more.

## Basic Usage

```bash
npx ticker-cli <command> [options]
```

## Available Commands

| Command | Description |
|---------|-------------|
| `quote` | Get real-time stock quotes |
| `chart` | Get chart/historical data |
| `indicator` | Calculate technical indicators (SMA, EMA, RSI, MACD, BB) |
| `summary` | Get comprehensive quote summary |
| `news` | Get latest stock news |
| `insights` | Get stock insights and analysis |
| `options` | Get options chain data |
| `recommendations` | Get analyst recommendations |
| `screener` | Screen stocks (most actives, gainers, losers, etc.) |
| `search` | Search for stock symbols |

## Quick Examples

```bash
# Get quote for single or multiple stocks
npx ticker-cli quote AAPL
npx ticker-cli quote AAPL MSFT GOOGL

# Get historical chart data
npx ticker-cli chart AAPL -p 1mo
npx ticker-cli chart AAPL --start 2025-01-01 --end 2025-12-31

# Calculate technical indicators
npx ticker-cli indicator AAPL sma -p 3mo
npx ticker-cli indicator AAPL rsi -p 3mo
npx ticker-cli indicator AAPL macd -p 6mo
npx ticker-cli indicator AAPL sma -p 1mo -i 1h

# Get news and insights
npx ticker-cli news AAPL --limit 20
npx ticker-cli insights AAPL

# Screen stocks
npx ticker-cli screener -q most_actives
npx ticker-cli screener -q day_gainers
```

## Report Generation Guides

For detailed instructions on generating reports, see the references folder:

- **Daily Reports**: See [references/daily-report.md](references/daily-report.md) for pre-market, mid-market, and post-market report generation
- **Weekly Reports**: See [references/weekly-report.md](references/weekly-report.md) for weekly analysis reports

## Technical Indicators Reference

| Indicator | Description | Default Length |
|-----------|-------------|----------------|
| `sma` | Simple Moving Average | 20 |
| `ema` | Exponential Moving Average | 20 |
| `rsi` | Relative Strength Index | 14 |
| `macd` | Moving Average Convergence Divergence | 12/26/9 |
| `bb` | Bollinger Bands | 20 |

## Screener Queries

Available predefined queries:
- `most_actives` - Most actively traded stocks
- `day_gainers` - Top gainers of the day
- `day_losers` - Top losers of the day
- `undervalued_growth_stocks` - Undervalued stocks with growth potential
- `undervalued_large_caps` - Undervalued large cap stocks
- `growth_technology_stocks` - Growing tech stocks
- `top_mutual_funds` - Top performing mutual funds
