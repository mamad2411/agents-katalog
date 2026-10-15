---
name: toobit-cex-trade
description: "This skill should be used when the user asks to 'buy BTC', 'sell ETH', 'place a limit order', 'place a market order', 'cancel my order', 'amend my order', 'long BTC futures', 'short ETH futures', 'open a position', 'close a position', 'flash close', 'reverse position', 'set take profit', 'set stop loss', 'set leverage', 'change margin type', 'adjust margin', 'auto add margin', 'check my orders', 'order status', 'fill history', 'trade history', 'futures balance', 'today PnL', 'commission rate', or any request to place/cancel/amend spot or USDT-M perpetual futures orders on Toobit CEX. Covers spot trading and USDT-M perpetual futures (leverage, margin, TP/SL, flash close, reverse position). Requires API credentials. Do NOT use for market data (use toobit-cex-market), or account balance/deposits/withdrawals (use toobit-cex-portfolio)."
license: MIT
metadata:
  author: toobit
  version: "1.0.0"
  homepage: "https://www.toobit.com"
  agent:
    requires:
      bins: ["toobit"]
    install:
      - id: npm
        kind: node
        package: "toobit-trade-cli"
        bins: ["toobit"]
        label: "Install toobit CLI (npm)"
---

# Toobit CEX Trading CLI

Spot and USDT-M perpetual futures order management on Toobit exchange. Place, cancel, amend, and monitor orders; set leverage and margin type; adjust margin; flash close and reverse positions; set take-profit/stop-loss. **Requires API credentials.**

## Prerequisites

1. Install `toobit` CLI:
   ```bash
   npm install -g toobit-trade-cli
   ```
2. Configure credentials in `~/.toobit/config.toml`:
   ```toml
   default_profile = "live"

   [profiles.live]
   api_key    = "your-api-key"
   secret_key = "your-secret-key"
   ```
   Or set environment variables:
   ```bash
   export TOOBIT_API_KEY=your_key
   export TOOBIT_SECRET_KEY=your_secret
   ```
3. Verify credentials:
   ```bash
   toobit account check-api-key
   ```

## Credential Check

**Run this check before any authenticated command.**

```bash
toobit account check-api-key    # verify API key status and permissions
```

- If the command returns an error or authentication failure: **stop all operations**, guide the user to edit `~/.toobit/config.toml`, and wait for setup to complete before retrying.
- If credentials are valid: proceed with the requested operation.

### Handling Authentication Errors

If any command returns a 401 / -2015 authentication error:
1. **Stop immediately** — do not retry the same command
2. Inform the user: "Authentication failed. Your API credentials may be invalid, expired, or IP not whitelisted."
3. Guide the user to update credentials:
   ```
   ~/.toobit/config.toml
   ```
4. After the user confirms the file is updated, run `toobit account check-api-key` to verify
5. Only then retry the original operation

## Skill Routing

- For market data (prices, charts, depth, funding rates) → use `toobit-cex-market`
- For account balance, sub-accounts, deposits, withdrawals → use `toobit-cex-portfolio`
- For spot/futures orders, leverage, margin, flash close → use `toobit-cex-trade` (this skill)

## Quickstart

```bash
# Market buy 0.01 BTC (spot)
toobit spot place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.01

# Limit sell 0.01 BTC at $100,000 (spot)
toobit spot place --symbol BTCUSDT --side SELL --type LIMIT --quantity 0.01 --price 100000

# View open spot orders
toobit spot orders --symbol BTCUSDT

# Cancel a spot order
toobit spot cancel --orderId <orderId>

# Long BTC futures at market
toobit futures place --symbol BTC-SWAP-USDT --side BUY_OPEN --orderType MARKET --quantity 0.01

# Set BTC futures leverage to 10x
toobit futures leverage --symbol BTC-SWAP-USDT --leverage 10

# Flash close BTC futures position
toobit futures flash-close --symbol BTC-SWAP-USDT --side LONG

# View futures positions
toobit futures positions --symbol BTC-SWAP-USDT

# Futures account balance
toobit futures balance
```

## Command Index

### Spot Orders

| # | Command | Type | Description |
|---|---|---|---|
| 1 | `toobit spot place` | WRITE | Place spot order (MARKET/LIMIT) |
| 2 | `toobit spot cancel` | WRITE | Cancel spot order by orderId |
| 3 | `toobit spot cancel-all` | WRITE | Cancel all open spot orders for a symbol |
| 4 | `toobit spot get` | READ | Single spot order details |
| 5 | `toobit spot orders` | READ | List open spot orders |
| 6 | `toobit spot history` | READ | Historical (filled/cancelled) spot orders |
| 7 | `toobit spot fills` | READ | Spot trade fill history |

### Futures Orders

| # | Command | Type | Description |
|---|---|---|---|
| 8 | `toobit futures place` | WRITE | Place futures order |
| 9 | `toobit futures cancel` | WRITE | Cancel futures order |
| 10 | `toobit futures cancel-all` | WRITE | Cancel all futures orders for a symbol |
| 11 | `toobit futures amend` | WRITE | Amend futures order (price/quantity) |
| 12 | `toobit futures flash-close` | WRITE | Flash close entire position at market |
| 13 | `toobit futures leverage` | READ/WRITE | Get or set leverage |
| 14 | `toobit futures margin-type` | WRITE | Set margin type (cross/isolated) |
| 15 | `toobit futures get` | READ | Single futures order details |
| 16 | `toobit futures orders` | READ | List open futures orders |
| 17 | `toobit futures history` | READ | Historical futures orders |
| 18 | `toobit futures positions` | READ | Open futures positions |
| 19 | `toobit futures history-positions` | READ | Closed position history |
| 20 | `toobit futures fills` | READ | Futures trade fill history |
| 21 | `toobit futures balance` | READ | Futures account balance (equity, margin, PnL) |
| 22 | `toobit futures pnl` | READ | Today's realized PnL |
| 23 | `toobit futures commission` | READ | Commission rate for a symbol |

### MCP-Only Tools (no CLI shortcut)

| # | Tool | Type | Description |
|---|---|---|---|
| 24 | `futures_set_trading_stop` | WRITE | Set TP/SL on an existing position |
| 25 | `futures_reverse_position` | WRITE | Reverse (flip) position direction |
| 26 | `futures_adjust_margin` | WRITE | Adjust isolated margin |
| 27 | `futures_auto_add_margin` | WRITE | Enable/disable auto-add margin |
| 28 | `futures_get_balance_flow` | READ | Futures balance flow (ledger) |
| 29 | `spot_batch_orders` | WRITE | Batch place spot orders |
| 30 | `spot_cancel_order_by_ids` | WRITE | Cancel spot orders by multiple IDs |
| 31 | `spot_place_order_test` | WRITE | Test spot order (validates params, no execution) |
| 32 | `futures_batch_orders` | WRITE | Batch place futures orders |
| 33 | `futures_cancel_order_by_ids` | WRITE | Cancel futures orders by multiple IDs |

## Cross-Skill Workflows

### Spot market buy
> User: "Buy $500 worth of ETH at market"

```
1. toobit-cex-market    toobit market ticker --symbol ETHUSDT          → get current price to estimate qty
2. toobit-cex-portfolio toobit account info                            → confirm available USDT ≥ $500
        ↓ user approves
3. toobit-cex-trade     toobit spot place --symbol ETHUSDT --side BUY --type MARKET --quantity <qty>
4. toobit-cex-trade     toobit spot fills --symbol ETHUSDT             → confirm fill price and size
```

### Open long BTC futures with TP/SL
> User: "Long 0.1 BTC futures at market, TP at $105k, SL at $88k"

```
1. toobit-cex-portfolio toobit account info                            → confirm margin available
2. toobit-cex-trade     toobit futures leverage --symbol BTC-SWAP-USDT → check current leverage
        ↓ user approves
3. toobit-cex-trade     toobit futures place --symbol BTC-SWAP-USDT --side BUY_OPEN \
                          --orderType MARKET --quantity 0.1
4. toobit-cex-trade     (MCP) futures_set_trading_stop → set tpPrice=105000, slPrice=88000
5. toobit-cex-trade     toobit futures positions --symbol BTC-SWAP-USDT → confirm position opened
```

### Adjust leverage then place order
> User: "Set BTC futures to 5x leverage then go long"

```
1. toobit-cex-trade     toobit futures leverage --symbol BTC-SWAP-USDT          → check current
        ↓ user approves change
2. toobit-cex-trade     toobit futures leverage --symbol BTC-SWAP-USDT --leverage 5
3. toobit-cex-trade     toobit futures place --symbol BTC-SWAP-USDT --side BUY_OPEN \
                          --orderType MARKET --quantity 0.1
4. toobit-cex-trade     toobit futures positions --symbol BTC-SWAP-USDT → confirm position + leverage
```

### Flash close and reverse
> User: "Close my BTC long and flip to short"

```
1. toobit-cex-trade     toobit futures positions --symbol BTC-SWAP-USDT → confirm open long
2. toobit-cex-trade     toobit futures flash-close --symbol BTC-SWAP-USDT --side LONG
        OR
2. toobit-cex-trade     (MCP) futures_reverse_position → reverse in one step
3. toobit-cex-trade     toobit futures positions --symbol BTC-SWAP-USDT → confirm new short
```

### Cancel all open spot orders
> User: "Cancel all my open BTC spot orders"

```
1. toobit-cex-trade     toobit spot orders --symbol BTCUSDT            → list open orders
2. toobit-cex-trade     toobit spot cancel-all --symbol BTCUSDT
3. toobit-cex-trade     toobit spot orders --symbol BTCUSDT            → confirm all cancelled
```

## Operation Flow

### Step 0 — Credential Check

Before any authenticated command:

1. Run `toobit account check-api-key` to verify API key validity
2. If error → stop, guide user to configure `~/.toobit/config.toml`
3. If valid → proceed

### Step 1: Identify instrument type and action

**Spot** (symbol format: `BTCUSDT`):
- Place/cancel order → `toobit spot place/cancel/cancel-all`
- Query → `toobit spot get/orders/history/fills`

**Futures / Perpetual** (symbol format: `BTC-SWAP-USDT`):
- Place/cancel/amend order → `toobit futures place/cancel/cancel-all/amend`
- Close position → `toobit futures flash-close`
- Reverse position → MCP `futures_reverse_position`
- Leverage → `toobit futures leverage [--leverage <n>]`
- Margin type → `toobit futures margin-type --symbol <sym> --marginType <type>`
- Adjust margin → MCP `futures_adjust_margin`
- TP/SL → MCP `futures_set_trading_stop`
- Auto-margin → MCP `futures_auto_add_margin`
- Query → `toobit futures get/orders/history/positions/history-positions/fills/balance/pnl/commission`

### Step 2: Confirm write parameters

**Read commands** (orders, positions, fills, get, balance, pnl, commission): run immediately.

**Write commands** (place, cancel, amend, flash-close, leverage set, margin-type): confirm key details once:

- Spot place: confirm `--symbol`, `--side` (BUY/SELL), `--type` (MARKET/LIMIT), `--quantity`; `--price` required for LIMIT
- Futures place: confirm `--symbol`, `--side` (BUY_OPEN/SELL_OPEN/BUY_CLOSE/SELL_CLOSE), `--orderType`, `--quantity`
- Flash close: confirm `--symbol` and `--side` (LONG/SHORT); closes the **entire** position at market
- Reverse position: confirm this will close current and open opposite; double the risk
- Leverage set: confirm new value and impact on existing positions
- TP/SL: confirm trigger prices via MCP `futures_set_trading_stop`

### Step 3: Verify after writes

- After `spot place`: run `toobit spot orders` or `toobit spot fills` to confirm
- After `futures place`: run `toobit futures orders` or `toobit futures positions` to confirm
- After `flash-close`: run `toobit futures positions` to confirm position size is 0
- After cancel: run `toobit spot orders` / `toobit futures orders` to confirm order removed

## CLI Command Reference

### Spot — Place Order

```bash
toobit spot place --symbol <sym> --side <BUY|SELL> --type <MARKET|LIMIT> \
  --quantity <n> [--price <p>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Spot symbol (e.g., `BTCUSDT`) |
| `--side` | Yes | - | `BUY` or `SELL` |
| `--type` | Yes | `MARKET` | `MARKET` or `LIMIT` |
| `--quantity` | Yes | - | Order size in base currency |
| `--price` | Cond. | - | Required for `LIMIT` orders |

---

### Spot — Cancel Order

```bash
toobit spot cancel --orderId <id> [--clientOrderId <id>] [--json]
```

---

### Spot — Cancel All Orders

```bash
toobit spot cancel-all --symbol <sym> [--json]
```

Cancels all open orders for the specified symbol.

---

### Spot — Get Order

```bash
toobit spot get --orderId <id> [--clientOrderId <id>] [--json]
```

Returns: `orderId`, `symbol`, `side`, `type`, `price`, `origQty`, `executedQty`, `avgPrice`, `status`, `time`.

---

### Spot — Open Orders

```bash
toobit spot orders [--symbol <sym>] [--limit <n>] [--json]
```

Returns all pending/open spot orders. Filter by `--symbol` optionally.

---

### Spot — Trade History

```bash
toobit spot history --symbol <sym> [--limit <n>] [--startTime <ms>] [--endTime <ms>] [--json]
```

Returns filled/cancelled orders.

---

### Spot — Fills

```bash
toobit spot fills [--symbol <sym>] [--limit <n>] [--json]
```

Returns: `symbol`, `orderId`, `price`, `qty`, `commission`, `commissionAsset`, `time`.

---

### Futures — Place Order

```bash
toobit futures place --symbol <sym> --side <side> --orderType <type> \
  --quantity <n> [--price <p>] [--leverage <n>] [--json]
```

| Param | Required | Default | Description |
|---|---|---|---|
| `--symbol` | Yes | - | Futures symbol (e.g., `BTC-SWAP-USDT`) |
| `--side` | Yes | - | `BUY_OPEN`, `SELL_OPEN`, `BUY_CLOSE`, `SELL_CLOSE` |
| `--orderType` | Yes | `MARKET` | `MARKET`, `LIMIT`, `LIMIT_MAKER` |
| `--quantity` | Yes | - | Order quantity |
| `--price` | Cond. | - | Required for LIMIT orders |
| `--leverage` | No | - | Set leverage with order |

**Side values:**
- `BUY_OPEN` — open long position
- `SELL_OPEN` — open short position
- `BUY_CLOSE` — close short position
- `SELL_CLOSE` — close long position

---

### Futures — Cancel Order

```bash
toobit futures cancel --orderId <id> [--clientOrderId <id>] [--json]
```

---

### Futures — Cancel All Orders

```bash
toobit futures cancel-all --symbol <sym> [--json]
```

---

### Futures — Amend Order

```bash
toobit futures amend --orderId <id> [--quantity <n>] [--price <p>] [--json]
```

Must provide at least one of `--quantity` or `--price`.

---

### Futures — Flash Close Position

```bash
toobit futures flash-close --symbol <sym> --side <LONG|SHORT> [--json]
```

Closes the **entire** position at market price. Equivalent to placing a market close order for the full position size.

---

### Futures — Get or Set Leverage

```bash
# Get current leverage
toobit futures leverage --symbol <sym> [--json]

# Set leverage
toobit futures leverage --symbol <sym> --leverage <n> [--json]
```

| Param | Required | Description |
|---|---|---|
| `--symbol` | Yes | Futures symbol |
| `--leverage` | No | New leverage value; omit to query current |

---

### Futures — Set Margin Type

```bash
toobit futures margin-type --symbol <sym> --marginType <CROSS|ISOLATED> [--json]
```

| Value | Behavior |
|---|---|
| `CROSS` | Cross margin — shared across positions |
| `ISOLATED` | Isolated margin — independent per position |

---

### Futures — Get Order

```bash
toobit futures get --orderId <id> [--clientOrderId <id>] [--json]
```

Returns: `orderId`, `symbol`, `side`, `type`, `price`, `origQty`, `executedQty`, `avgPrice`, `status`, `time`.

---

### Futures — Open Orders

```bash
toobit futures orders [--symbol <sym>] [--json]
```

---

### Futures — Order History

```bash
toobit futures history --symbol <sym> [--limit <n>] [--json]
```

---

### Futures — Positions

```bash
toobit futures positions [--symbol <sym>] [--json]
```

Returns: `symbol`, `side`, `positionAmt`, `avgPrice`, `unrealisedPnl`, `leverage`, `marginType`, `liquidationPrice`.

---

### Futures — History Positions

```bash
toobit futures history-positions [--symbol <sym>] [--json]
```

Returns closed position records with realized PnL.

---

### Futures — Fills

```bash
toobit futures fills [--symbol <sym>] [--limit <n>] [--json]
```

---

### Futures — Balance

```bash
toobit futures balance [--json]
```

Returns: futures account equity, available margin, total margin, unrealized PnL across all positions.

---

### Futures — Today PnL

```bash
toobit futures pnl [--json]
```

Returns: today's realized PnL summary.

---

### Futures — Commission Rate

```bash
toobit futures commission --symbol <sym> [--json]
```

Returns: `makerCommissionRate`, `takerCommissionRate` for the specified symbol.

---

## MCP Tool Reference

### Spot Tools

| Tool | Description |
|---|---|
| `spot_place_order` | Place spot order |
| `spot_place_order_test` | Test spot order (validates params, no execution) |
| `spot_batch_orders` | Batch place multiple spot orders |
| `spot_cancel_order` | Cancel spot order |
| `spot_cancel_open_orders` | Cancel all open spot orders for a symbol |
| `spot_cancel_order_by_ids` | Cancel spot orders by multiple IDs |
| `spot_get_order` | Get single spot order details |
| `spot_get_open_orders` | List open spot orders |
| `spot_get_trade_orders` | Spot order history |
| `spot_get_fills` | Spot fill history |

### Futures Tools

| Tool | Description |
|---|---|
| `futures_place_order` | Place futures order |
| `futures_batch_orders` | Batch place multiple futures orders |
| `futures_cancel_order` | Cancel futures order |
| `futures_cancel_all_orders` | Cancel all futures orders for a symbol |
| `futures_cancel_order_by_ids` | Cancel futures orders by multiple IDs |
| `futures_amend_order` | Amend futures order |
| `futures_get_order` | Get single futures order details |
| `futures_get_open_orders` | List open futures orders |
| `futures_get_history_orders` | Futures order history |
| `futures_get_positions` | Open futures positions |
| `futures_get_history_positions` | Closed position history |
| `futures_set_leverage` | Set futures leverage |
| `futures_get_leverage` | Get current leverage |
| `futures_set_margin_type` | Set margin type (CROSS/ISOLATED) |
| `futures_set_trading_stop` | Set TP/SL on position |
| `futures_flash_close` | Flash close position at market |
| `futures_reverse_position` | Reverse (flip) position direction |
| `futures_adjust_margin` | Adjust isolated margin amount |
| `futures_auto_add_margin` | Enable/disable auto-add margin |
| `futures_get_balance` | Futures account balance |
| `futures_get_fills` | Futures fill history |
| `futures_get_commission_rate` | Commission rate |
| `futures_get_today_pnl` | Today's realized PnL |
| `futures_get_balance_flow` | Futures balance flow (ledger) |

---

## Input / Output Examples

**"Buy 0.05 BTC at market"**
```bash
toobit spot place --symbol BTCUSDT --side BUY --type MARKET --quantity 0.05
# → Order placed: orderId 7890123456 (FILLED)
```

**"Set a limit sell for 0.1 ETH at $3500"**
```bash
toobit spot place --symbol ETHUSDT --side SELL --type LIMIT --quantity 0.1 --price 3500
# → Order placed: orderId 7890123457 (NEW)
```

**"Show my open spot orders"**
```bash
toobit spot orders --symbol BTCUSDT
# → table: orderId, symbol, side, type, price, origQty, executedQty, status
```

**"Long 0.1 BTC futures at market"**
```bash
toobit futures place --symbol BTC-SWAP-USDT --side BUY_OPEN --orderType MARKET --quantity 0.1
# → Order placed: orderId 7890123458 (FILLED)
```

**"Close my BTC long position immediately"**
```bash
toobit futures flash-close --symbol BTC-SWAP-USDT --side LONG
# → Position closed: BTC-SWAP-USDT LONG
```

**"Set BTC futures leverage to 5x"**
```bash
toobit futures leverage --symbol BTC-SWAP-USDT --leverage 5
# → Leverage set: BTC-SWAP-USDT 5x
```

**"Switch BTC futures to isolated margin"**
```bash
toobit futures margin-type --symbol BTC-SWAP-USDT --marginType ISOLATED
# → Margin type set: BTC-SWAP-USDT ISOLATED
```

**"Show my futures positions"**
```bash
toobit futures positions --symbol BTC-SWAP-USDT
# → symbol: BTC-SWAP-USDT | side: LONG | positionAmt: 0.1 | avgPrice: 95000 | upl: +120.5 | leverage: 10x
```

**"What's my futures balance?"**
```bash
toobit futures balance
# → equity: 5000.00 | availableMargin: 4200.00 | totalMargin: 800.00 | unrealisedPnl: +120.5
```

**"What's my commission rate for BTC futures?"**
```bash
toobit futures commission --symbol BTC-SWAP-USDT
# → maker: 0.02% | taker: 0.06%
```

## Edge Cases

### Spot
- **Symbol format**: always uppercase, no separator — `BTCUSDT`, `ETHUSDT`
- **Side values**: `BUY` or `SELL` (uppercase)
- **Market order**: `--type MARKET` does not require `--price`; `LIMIT` does
- **Quantity**: in base currency (e.g., BTC amount for BTCUSDT)
- **Minimum order**: check `toobit market info` for `minQty` and `minNotional` per symbol
- **Test order**: use MCP `spot_place_order_test` to validate parameters without execution

### Futures
- **Symbol format**: dash-separated with SWAP — `BTC-SWAP-USDT`, `ETH-SWAP-USDT`
- **Side values**: `BUY_OPEN` (open long), `SELL_OPEN` (open short), `BUY_CLOSE` (close short), `SELL_CLOSE` (close long)
- **Flash close**: closes the entire position; to partial close, use `futures place` with `BUY_CLOSE`/`SELL_CLOSE` and specific quantity
- **Reverse position**: automatically closes current and opens opposite; use with caution
- **Leverage**: max varies by symbol and tier; exchange rejects if exceeded. Check `market_get_risk_limits` for max leverage per tier
- **Margin type**: switching from ISOLATED to CROSS when positions are open may fail; close positions first
- **TP/SL**: use MCP `futures_set_trading_stop` after opening a position — requires `symbol`, `side`, `tpPrice`, `slPrice`
- **Auto-add margin**: when enabled for isolated margin mode, system auto-adds margin when approaching liquidation
- **Adjust margin**: only for isolated margin mode; add or reduce margin for a specific position

## Global Notes

- All write commands require valid API credentials in `~/.toobit/config.toml` or env vars
- API key must have "Spot Trading" permission for spot orders and "Futures Trading" permission for futures orders
- IP whitelist must include your machine's public IP
- `--json` returns raw Toobit API response
- Rate limit: varies per endpoint; typically 10–20 requests per second
- All timestamps are in milliseconds (Unix epoch)
- Signature method: HMAC-SHA256; handled automatically by the CLI
