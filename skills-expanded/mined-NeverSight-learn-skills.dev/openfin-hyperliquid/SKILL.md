---
name: openfin-hyperliquid
description: >-
  Complete Hyperliquid playbook — perpetuals and spot trading, margin/leverage,
  TWAP, real-time WebSocket data, and historical candles. Use for any
  Hyperliquid task. Trading triggers&#58; place perp/spot orders (Gtc/Ioc/Alo),
  market-like fills, take-profit/stop-loss grouping, modify or cancel orders,
  batch cancels, TWAP orders (place/track fills/terminate), change leverage
  (cross vs isolated), adjust isolated margin, transfer USDC between spot and
  perp accounts (usd_class_transfer), get the EVM deposit address to fund
  Hyperliquid. Data triggers&#58; read account summary (perp margin, positions,
  liquidation price, unrealized PnL), spot balances, portfolio, open orders,
  historical orders, single order status, fills (latest or by time window),
  funding history, rate limits, market metas (perp + spot, szDecimals),
  perp-only metas (returns universes across all perp DEXs — includes HIP-3
  tokenized equity perps like NVDA, TSLA on the `xyz` dex alongside crypto
  perps), spot-only metas, mid prices for all coins, L2 orderbook per
  coin, spot token details, allDexsAssetCtxs snapshot (funding/OI/mark prices
  across assets). Real-time WebSocket&#58; wss://api.hyperliquid.xyz/ws with
  channels allMids, allDexsAssetCtxs (backend manages a shared subscription —
  agent can subscribe/unsubscribe and read the cached snapshot), l2Book,
  trades, candle, orderUpdates, userFills, userFundings. Historical OHLCV
  candles via direct POST https://api.hyperliquid.xyz/info {type:
  'candleSnapshot'} — supports 1m/3m/5m/15m/30m/1h/2h/4h/8h/12h/1d/3d/1w/1M
  intervals up to 5000 candles. Covers all routes under /agent/trading/*
  (market/metas|mids|perp-metas|spot-metas|l2-book|token|all-dexs-asset-ctxs,
  deposit-address, account, account/spot, portfolio, rate-limit, orders,
  orders/details, orders/history, orders/:oid/status, twap, twap/fills,
  twap/:id, fills, fills/by-time, funding, leverage, margin, transfer).
  Triggers on mentions of Hyperliquid, "HL", perp, perpetual, funding rate,
  TWAP, isolated margin, cross margin, "deposit to Hyperliquid", "HIP-3",
  "HLP", or "HL vault". Prerequisite&#58; openfin-setup.
---

# Hyperliquid Perps & Spot

Playbook for trading perpetuals and spot on Hyperliquid through OpenFinance,
plus the real-time WebSocket for market data.

## Prerequisite

1. User completed `openfin-setup` (API key + EVM wallet delegation).
2. For trading: USDC in the user's wallet, then deposit USDC into the
   Hyperliquid account via `GET /agent/trading/deposit-address` (send USDC
   to that deposit address; chain routing is handled automatically).
3. For perp orders specifically: margin must be in the **perp account**, not
   spot. Transfer with `POST /agent/trading/transfer`.

## Accounts & funding

- **`GET /agent/trading/account`** — Perpetual account summary. Returns
  `marginSummary` (accountValue, totalMarginUsed, totalNtlPos, totalRawUsd,
  withdrawable) and a list of open positions with `entryPx`, `positionValue`,
  `returnOnEquity`, `unrealizedPnl`, `liquidationPx`, `leverage`, and `size`
  for each asset.
- **`GET /agent/trading/account/spot`** — Spot account summary. Returns a
  list of token balances with `coin` name, token ID, hold amount, total
  amount, and entry notional value per token held.
- **`GET /agent/trading/portfolio`** — Full portfolio view combining perp
  positions and spot balances in a single response (margin + equity + PnL +
  positions + token holdings with amounts and values).
- **`GET /agent/trading/rate-limit`** — Current Hyperliquid API rate-limit
  status for the wallet. Returns cumulative volume traded, API calls used,
  and remaining allowed calls in the window.
- **`GET /agent/trading/deposit-address`** — Deposit address mapped to the
  authenticated wallet's Hyperliquid account. Send USDC to this address to
  fund the Hyperliquid account; chain routing to Hyperliquid is handled automatically.
- **`POST /agent/trading/transfer`** body `{amount, toPerp}` — Transfer USDC
  between the perp and spot accounts. Required before spot trading (funds
  must be in spot wallet to buy tokens) or before perp trading (funds in
  perp wallet). `toPerp: true` = spot → perp; `false` = perp → spot.

## Market data (REST)

- **`GET /agent/trading/market/mids`** — Mid prices (midpoint between best
  bid and ask) for every listed asset. Returns a map of asset symbol → mid
  price string (e.g. `{"BTC": "70939.5", "ETH": "2500.0"}`).
- **`GET /agent/trading/market/metas`** (`?dex=`) — Market metadata and
  asset contexts: funding rates, open interest, mark/mid/oracle prices,
  impact prices, 24h base and notional volume, premium, previous day
  price. Pass `dex` for DEX-specific data.
- **`GET /agent/trading/market/perp-metas`** — Perpetual contract metadata
  across **all perp DEXs** on Hyperliquid. Returns multiple `universe`
  arrays — one per DEX — each with assets' `name`, `szDecimals` (size
  precision), `maxLeverage`, `marginTableId`, and `isDelisted` flag. The
  default DEX lists crypto perps (BTC, ETH, …); HIP-3 builder-deployed
  DEXs add other markets including **tokenized equity perps** (e.g. NVDA,
  TSLA, AAPL on the `xyz` dex — coin symbol prefixed like `xyz:NVDA`).
  Use this to look up **asset indices** (`a`) and `szDecimals` before
  placing orders — place-order body requires these, and the index is
  scoped to its DEX.
- **`GET /agent/trading/market/spot-metas`** (`?dex=`) — Spot market
  metadata and asset contexts. Returns `universe` (token pairs, names,
  indices, isCanonical) and context per pair (`prevDayPx`, `dayNtlVlm`,
  `dayBaseVlm`, `markPx`, `midPx`, `circulatingSupply`, `totalSupply`,
  `coin`).
- **`GET /agent/trading/market/l2-book/:coin`** — L2 orderbook for a coin
  (e.g. `BTC`). Returns coin name, timestamp, and a two-level array of
  bids and asks, each with `px` (price), `sz` (size), and `n` (number of
  orders at that level).
- **`GET /agent/trading/market/token/:tokenId`** — Detailed spot token info
  by token ID. Returns name, maxSupply, totalSupply, circulatingSupply,
  szDecimals, weiDecimals, midPx, markPx, prevDayPx, deployer, deployTime,
  seededUsdc, futureEmissions. `:tokenId` must be the full hex hash from
  `spot-metas` (e.g. `0xc1fb593aeffbeb02f85e0308e9956a90`), NOT a simple
  number.
- **`GET /agent/trading/market/all-dexs-asset-ctxs`** — Asset contexts
  across all DEXs on Hyperliquid: funding rate, open interest, mark/mid/
  oracle prices, 24h volume, impact prices, premium, prev day price.
  Snapshot equivalent of the `allDexsAssetCtxs` WS channel.

## Historical candles (OHLCV)

Not a backend route — hit Hyperliquid's info endpoint directly:

```http
POST https://api.hyperliquid.xyz/info
Content-Type: application/json

{
  "type": "candleSnapshot",
  "req": {
    "coin": "BTC",
    "interval": "1h",              // 1m,3m,5m,15m,30m,1h,2h,4h,8h,12h,1d,3d,1w,1M
    "startTime": 1706659200000,    // ms
    "endTime": 1706745600000       // ms, optional (defaults to now)
  }
}
```

Returns up to 5000 most recent candles. For HIP-3 spot tokens, prefix the coin
with the dex name, e.g. `"xyz:XYZ100"`.

## Market data (WebSocket)

Hyperliquid exposes a real-time feed at `wss://api.hyperliquid.xyz/ws`.

**Subscribe message shape:**
```json
{ "method": "subscribe", "subscription": { "type": "<channel>" } }
```

**Common channels:**
- `allDexsAssetCtxs` — funding rate, mark price, OI, 24h volume per asset
- `allMids` — real-time mid prices for every coin
- `l2Book` (`{type, coin: "BTC"}`) — orderbook updates
- `trades` (`{type, coin}`) — trade tape
- `candle` (`{type, coin, interval: "1m"}`) — streaming candles
- `orderUpdates` / `userFills` / `userFundings` — user-scoped; requires signing

### Backend-managed WS

The OpenFinance backend keeps one shared connection to
`wss://api.hyperliquid.xyz/ws` and caches the latest snapshot per channel.
Use this when multiple agents share the backend and you want a single
connection + consistent state. MCP tools:

- `subscribe_all_dexs_asset_ctxs` — start the shared backend subscription
- `unsubscribe_all_dexs_asset_ctxs` — stop it
- `get_all_dexs_asset_ctxs` — read the latest cached snapshot
- `get_ws_status` — is the backend's connection alive

⚠ The `allDexsAssetCtxs` array has **no asset names** — each entry maps by
index to the `universe` from `GET /agent/trading/market/metas`. Call
`/market/metas` at least once to build the index→name map.

### Direct WS from the client

For reactive UIs or per-client streams, open your own WS to
`wss://api.hyperliquid.xyz/ws` and subscribe. Don't expect the backend's
cache to reflect connections that weren't opened through it.

## Orders

### Pre-flight: always check balance before placing

Before any order, check the user has funds in the right account:

- **Perp orders** → `GET /agent/trading/account` →
  `marginSummary.withdrawable` (free margin) and `accountValue`. The
  notional you're about to open (`sz * px`) divided by chosen `leverage`
  must be ≤ withdrawable. If 0 or insufficient, transfer from spot first
  (`POST /agent/trading/transfer {amount, toPerp: true}`).
- **Spot orders** → `GET /agent/trading/account/spot` → balance for the
  quote token (USDC for buys, the base token for sells). If insufficient,
  transfer from perp (`toPerp: false`) or prompt the user to deposit.
- **HIP-3 perps** → same as perp orders; HIP-3 markets settle in USDC on
  the perp account.

Skipping this check leaks ugly "insufficient margin" rejections back to
the user instead of a clean "you need to deposit / transfer X first"
message. Always do the read, then decide whether to place, transfer, or
ask.

### Placing orders

- **`POST /agent/trading/orders`** — Place one or more orders. Each order
  needs `a` (asset index from `perp-metas`), `b` (true=buy), `p` (price as
  string), `s` (size as string), `r` (reduce only), `t` (order type object
  with `limit` or `trigger`). Body:
  ```json
  {
    "orders": [{
      "coin": "BTC",
      "is_buy": true,
      "sz": 0.01,
      "limit_px": 65000,
      "order_type": { "limit": { "tif": "Gtc" } },
      "reduce_only": false
    }],
    "grouping": "na"           // "na" | "normalTpsl" | "positionTpsl"
  }
  ```
  `tif` (time-in-force):
    - `"Gtc"` — good-till-cancelled (resting limit)
    - `"Ioc"` — immediate-or-cancel (market-ish; cross the book for a fill)
    - `"Alo"` — add-liquidity-only (post-only; rejects if would be taker)
    - `"FrontendMarket"` — market order with frontend-style slippage
      protection; used for HIP-3 stock perps and "buy now" flows

  Grouping: `"normalTpsl"` groups take-profit/stop-loss child orders with
  a primary; `"positionTpsl"` attaches them to an existing position.
  Fetch market metas first to get correct asset indices and szDecimals.

### HIP-3 perps (tokenized equities, etc.)

HIP-3 builder-deployed DEXs (e.g. `xyz` for stock perps like NVDA/TSLA)
have two extra requirements on top of the standard order shape:

- **Asset index `a` is computed, not looked up directly.** Hyperliquid's
  formula:
    - Main DEX perps: `a = index_in_meta` (BTC=0, ETH=1, …)
    - HIP-3 perps: `a = 100000 + perp_dex_index * 10000 + index_in_meta`
    - Spot: `a = 10000 + spotInfo.index`

  Example: `xyz:NVDA` on `perp_dex_index = 1` at `index_in_meta = 12`
  gives `a = 100000 + 1*10000 + 12 = 110012` (matches the sample
  payload). Pull `index_in_meta` from `/market/perp-metas` per-DEX and
  `perp_dex_index` from the `perpDexs` info call. Docs:
  https://hyperliquid.gitbook.io/hyperliquid-docs/for-developers/api/asset-ids
- **`builder` field is required** in the signed action: `{"b":
  "<builder_address>", "f": <fee_tenths_of_bps>}`. HIP-3 venues route
  through a builder that takes a fee. Example raw action snippet:
  ```json
  {
    "type": "order",
    "orders": [{"a":110012,"b":true,"p":"423.83","s":"0.026","r":false,
                "t":{"limit":{"tif":"FrontendMarket"}}}],
    "grouping": "na",
    "builder": {"b": "0x5ef4deeb76f87d979d0ddc8c51f5b4f65d1c972a", "f": 50}
  }
  ```
  `f` is the builder fee in tenths of a basis point (Hyperliquid
  convention), so `f: 50` ≈ 5 bps. **The OpenFinance backend injects the
  `builder` field automatically** when the coin resolves to an HIP-3
  DEX — callers just pass the coin (e.g. `"xyz:NVDA"`) on
  `POST /agent/trading/orders` and the route handles signing with the
  builder attached. The payload above is what the backend produces, not
  something the caller assembles.

### Reading orders

- **`GET /agent/trading/orders`** — All currently open orders (compact).
  Returns array with `coin`, `side` (B/A), `limitPx`, `sz`, `oid`
  (order ID), `timestamp`, `orderType` per order.
- **`GET /agent/trading/orders/details`** — Same but with full details:
  `origSz` (original size), `triggerPx`, `triggerCondition`, `cloid`
  (client order ID), `reduceOnly` flag.
- **`GET /agent/trading/orders/history`** — Historical orders (filled,
  cancelled, rejected). Adds `statusMsg` (e.g. `"filled"`, `"cancelled"`),
  `filledSz`, `avgFillPx`, `cloid`.
- **`GET /agent/trading/orders/:oid/status`** — Single order's current
  status (`open`, `filled`, `cancelled`), `filledSz`, `avgFillPx`,
  remaining size.

### Cancel / modify

- **`DELETE /agent/trading/orders`** body `{cancels: [{a, o}]}` — Cancel
  one or more open orders. `a` = asset index (from market metas), `o` =
  order ID. Batch-cancellable.
- **`PUT /agent/trading/orders/:oid`** body `{order: {...}}` — Modify an
  existing open order by ID. Same order shape as place.

### TWAP (Time-Weighted Average Price)

- **`POST /agent/trading/twap`** — Place a TWAP order that splits a large
  trade into smaller market-order slices over a specified duration to
  minimize price impact. Returns `twapId` to track or terminate.
- **`GET /agent/trading/twap/fills`** — Get individual slice executions for
  all TWAPs. Returns fills with `coin`, `side`, `fillPx`, `fillSz`,
  `feeUsdc`, `timestamp`, and the parent `twapId`.
- **`DELETE /agent/trading/twap/:twapId`** — Terminate an active TWAP.
  Stops further slices; already-filled slices remain settled.

## Leverage & margin

- **`POST /agent/trading/leverage`** body `{asset, isCross, leverage}` —
  Set leverage + margin mode for an asset. Must be set BEFORE placing
  leveraged orders. `asset` = coin index, `isCross: true` = cross margin
  (shared pool), `false` = isolated (per-position), `leverage` = max
  multiplier.
- **`POST /agent/trading/margin`** body `{asset, isBuy, ntli}` — Add or
  remove margin from an isolated-margin position. Positive `ntli` adds
  (lowers liquidation risk), negative removes (raises leverage). Only
  works on positions using isolated margin mode.

## Fills & funding

- **`GET /agent/trading/fills`** (`?aggregateByTime=false`) — Trade fill
  history. Returns fills with `coin`, `side` (B/A), `px` (fill price),
  `sz`, `feeUsdc`, `timestamp`, `oid`, `cloid`, `crossed` (taker/maker),
  `liquidation` flag.
- **`GET /agent/trading/fills/by-time`** (`?startTime=<ms>&endTime=<ms>`) —
  Same fill data, filtered by time window (Unix ms). `endTime` optional
  (defaults to now).
- **`GET /agent/trading/funding`** — Funding payment history for perp
  positions. Returns payments with `coin`, `fundingRate`, `usdc` amount
  (positive = received, negative = paid), `timestamp`, and position size
  at the time of payment.

## Order-sizing gotchas

- `sz` is in **base asset** (e.g. BTC, ETH), not USD. For BTC at $65k, 0.01 = $650 notional.
- `limit_px` ticks differ per asset — check `perp-metas` for `szDecimals` and
  use `formatHyperliquidPrice` / `formatHyperliquidSize` conventions.
- Hyperliquid rejects prices too far from mid (price bands, ~5-10%). For
  aggressive fills cross the book but stay in-band.

## Margin modes

- **Cross margin**: all positions share one margin pool. Default.
- **Isolated margin**: margin pinned per position via `POST /margin`.

Set `isCross: true/false` on `POST /leverage` to pick the mode for a coin.

## Don't

- Don't use `Gtc` for "buy now" — use `Ioc` or `Alo` with cross-book price.
- Don't expect the WS cache to be populated instantly on server boot — the
  backend auto-subscribes on startup but first message can take a few seconds.
- Don't put raw USD amounts in `sz`. It's base-asset.
- Don't forget to `transfer` USDC from spot to perp before placing perp
  orders — they're separate balances.
- Don't place an order without first reading the relevant account
  balance (`/account` for perp/HIP-3, `/account/spot` for spot). Surface
  shortfalls to the user before signing.

## MCP note

Tool names mirror the routes: `hyperliquid_place_order`,
`hyperliquid_cancel_order`, `hyperliquid_get_account_summary`,
`hyperliquid_get_all_mids`, `hyperliquid_usd_class_transfer`, etc.
