---
name: alpha
description: Fetch and analyze stock market data using Alpha Vantage API. Use when user asks for stock market data, financial analysis, or /alpha.
---

# Alpha Vantage Skill

Fetches real-time stock market data from Alpha Vantage and creates a comprehensive digest with AI-powered analysis.

## Usage

```bash
python3 _scripts/alpha_vantage.py
```

With custom stocks:
```bash
python3 _scripts/alpha_vantage.py --stocks AAPL MSFT GOOGL
```

## Configuration

`.env` — `ALPHAVANTAGE_API_KEY` from https://www.alphavantage.co/

## Default Stocks

AAPL, GOOGL, MSFT, TSLA, AMZN

## Output

`Sources/Alpha Vantage Digest - YYYY-MM-DD.md` (market overview, stock table, AI analysis with [[wikilinks]])
