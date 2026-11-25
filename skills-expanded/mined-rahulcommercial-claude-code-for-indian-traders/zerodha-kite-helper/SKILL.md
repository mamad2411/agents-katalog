---
name: zerodha-kite-helper
description: Helps with Zerodha Kite Connect API — auth flow, fetching positions/holdings/orders, getting live quotes and historical candles. Read-only by default. Trigger when the user mentions Kite, Zerodha, KiteConnect, access_token, positions, or wants Indian equity / F&O market data.
---

# Zerodha Kite Helper

Wraps the common Kite Connect read paths so you don't keep re-explaining the auth dance.

## When to use

- User wants to fetch positions, holdings, orders, margins, or quotes from Kite.
- User is debugging the request-token → access-token exchange.
- User needs historical candles for backtesting.

## Auth flow (one-shot)

1. Login URL: `https://kite.zerodha.com/connect/login?api_key=<API_KEY>&v=3`
2. After login, Kite redirects to your registered URL with `?request_token=xxx`.
3. Exchange for access_token (valid till 6 AM next day):

```python
from kiteconnect import KiteConnect
kite = KiteConnect(api_key=API_KEY)
data = kite.generate_session(request_token, api_secret=API_SECRET)
access_token = data["access_token"]
kite.set_access_token(access_token)
```

Store `access_token` in a gitignored file. **Never** commit it.

## Common read calls

```python
kite.positions()         # net + day positions
kite.holdings()          # long-term holdings
kite.orders()            # today's orders
kite.margins()           # equity + commodity margins
kite.quote(["NSE:NIFTY 50", "NSE:RELIANCE"])
kite.historical_data(instrument_token, from_date, to_date, "5minute")
```

## Rate limits to respect

- 3 req/sec for quote, ohlc, ltp
- 10 req/sec for order placement (we don't place orders here)
- 1 req/sec for everything else

If you exceed, you get HTTP 429. Back off with exponential jitter.

## What this skill will NOT do

- **No live orders.** This skill never calls `kite.place_order()`. If user asks, redirect to paper-trade-runner.
- **No margin pledging or fund movement.**
- **No leaking access_token in logs.**

## Edge cases

- Access token expires daily at 6 AM IST — handle 403 by re-running auth flow.
- Market closed → quotes return last close. Check `last_trade_time` before assuming live data.
- F&O expiry day: instrument tokens for expired contracts get archived. Refresh the instrument dump weekly.
