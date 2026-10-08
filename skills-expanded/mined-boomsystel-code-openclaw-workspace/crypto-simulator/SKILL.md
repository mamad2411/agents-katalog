---
name: crypto-simulator
description: Cryptocurrency backtesting and paper trading simulator. Test strategies (RSI Swing, DCA, MA Cross, Grid, HODL, Bollinger Bands, MACD, Mean Reversion) against real historical data from CoinGecko. Optimize parameters automatically. Use when user says "backtest", "crypto simulation", "trading strategy test", or "paper trade".
---

# Crypto Simulator

Backtest and simulate cryptocurrency trading strategies using real market data.

## Features

- **8 Built-in Strategies**: RSI Swing, DCA, MA Cross, Grid Trading, HODL, Bollinger Bands, MACD, Mean Reversion
- **10 Supported Coins**: BTC, ETH, SOL, DOGE, ADA, DOT, AVAX, LINK, MATIC, XRP
- **Parameter Optimizer**: Auto-find best parameters for any coin×strategy combo
- **Free API**: Uses CoinGecko free tier (no API key needed)
- **SQLite Cache**: Avoids redundant API calls
- **Full CLI + REST API**: Use from terminal or integrate with other tools

## Quick Start

```bash
# Install dependencies
cd {skill_dir}
npm install

# Build
npm run build

# Run backtest
node dist/cli.js backtest --coin bitcoin --strategy rsi_swing --days 90

# Compare all strategies for a coin
node dist/cli.js compare --coin ethereum --days 180

# Optimize parameters
node dist/cli.js optimize --coin bitcoin --strategy rsi_swing

# Start API server
node dist/cli.js serve --port 3002
```

## Strategies

| Strategy | Best For | Description |
|----------|----------|-------------|
| RSI Swing | Volatile markets | Buy when RSI < 30, sell when RSI > 70 |
| DCA | Long-term | Dollar cost averaging at fixed intervals |
| MA Cross | Trending markets | Buy/sell on moving average crossovers |
| Grid | Ranging markets | Place buy/sell orders at price grid levels |
| HODL | Bull markets | Buy and hold baseline |
| Bollinger Bands | Mean reversion | Trade based on Bollinger Band breakouts |
| MACD | Momentum | Follow MACD signal line crossovers |
| Mean Reversion | Ranging | Buy below mean, sell above mean |

## API Endpoints

- `GET /api/prices/:coinId` — Current & historical prices
- `POST /api/backtest` — Run backtest with parameters
- `GET /api/compare/:coinId` — Compare all strategies
- `POST /api/optimize` — Find optimal parameters

## Requirements

- Node.js 18+
- Internet connection (CoinGecko API)
- No API keys needed

## Configuration

Environment variables (optional):
- `PORT` — API server port (default: 3002)
- `CACHE_DIR` — SQLite cache directory (default: ./data)
