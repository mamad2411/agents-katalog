---
name: vibetrader
description: Create and manage rule-based trading bots (stocks, ETFs, crypto, options) in plain English, backtest them, and run them on paper, live, or as signal bots that tell you what to trade at any brokerage. Uses the VibeTrader MCP server.
version: 1.1.0
license: MIT-0
metadata:
  openclaw:
    requires:
      env: [VIBETRADER_API_KEY]
---

# VibeTrader

Build trading bots by describing them, backtest them, and run them around the clock, from your agent.

## Setup

1. Create a key at https://vibetrader.markets/settings → **API keys**. Choose what it may do:
   - **See**: your bots, portfolio, trades, signals and backtests. Always included.
   - **Manage bots and signals**: create, edit, start, pause and delete paper bots and signal bots, and record trades you made for a signal.
   - **Place orders and run live bots**: buy and sell at your connected brokerage, and create or start bots that trade real money.
2. Put the key in your OpenClaw config (`~/.openclaw/openclaw.json`). The skill reads it from the environment:

   ```json
   {
     "skills": { "entries": { "vibetrader": { "env": { "VIBETRADER_API_KEY": "vt_your_key_here" } } } }
   }
   ```

3. Add the VibeTrader MCP server. It sends the key as a header on every request:

   ```json
   {
     "mcp": {
       "servers": {
         "vibetrader": {
           "url": "https://mcp.vibetrader.markets/mcp",
           "transport": "streamable-http",
           "headers": { "Authorization": "Bearer ${VIBETRADER_API_KEY}" }
         }
       }
     }
   }
   ```

   **Or sign in instead of using a key:** set `"auth": "oauth"` on the server (and drop `headers`), then run `openclaw mcp login vibetrader`. You sign in to VibeTrader in the browser and choose the permissions there.

The key always goes in the request header. **Never paste it into chat:** the hosted server no longer has an `authenticate` tool.

## What it can do

- **Bots:** create from plain English, list, inspect, start, pause, update, delete, and preview how often a bot would trigger.
- **Backtests:** run them, list them, open results, and run a quick covered-call backtest.
- **Portfolio:** account summary, positions, trade history, and per-bot trades and daily stats.
- **Market:** quotes, market status, and the indicator catalog.
- **Orders:** `place_order` and `close_position` at your VibeTrader-connected Alpaca account. Needs **Place orders and run live bots**.
- **Signal mode:** a bot that watches and decides but sends you each entry and exit instead of trading, so you can trade wherever you hold the account:
  - `set_signal_mode` turns it on;
  - `list_open_signals` shows what to do now;
  - `report_signal` records the trade you made so the bot tracks your position and sends the exits.

## Examples

- "Create a bot that buys AAPL when RSI(14) drops below 30 and sells above 70, $500 per trade"
- "Backtest my NVDA momentum bot over the last year"
- "Which of my bots made money this week?"
- "Put my SPY dip bot in signal mode and show me its open signals"
- "I bought 10 shares for the AAPL signal at $231.40, record it"

## Safety

- Paper trading is the default. Real money needs a live brokerage connection, VibeTrader's live-trading switch, and a key or connection with **Place orders and run live bots**.
- Tools that place orders, start bots or delete are marked destructive, so your agent should confirm them with you.
- Revoke a key or disconnect an app any time in Settings.

Docs: https://vibetrader.markets/docs · Support: https://vibetrader.markets/contact
