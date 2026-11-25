# Tight Market Crypto (TMC) Strategy — v2 Reversal-Based

## What This Strategy Does

TMC trades **short-duration crypto prediction markets** on Polymarket (5 or 15-minute windows like "Will BTC be above $X at 2:15PM?"). It detects markets where the crypto price has created a **clear underdog** (one side priced cheaply), then bets on that underdog — gambling that a **last-second reversal** will flip the outcome and pay a large multiple.

**Core thesis**: When the cheap side (underdog) has a high payout ratio (3x-20x) and there are signs of contrarian momentum, a last-second price reversal can deliver outsized returns that more than compensate for the losses on the trades that don't reverse.

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     COORDINATOR (main loop, 0.5s tick)       │
│                                                               │
│  ┌──────────────┐   ┌──────────────┐   ┌──────────────────┐ │
│  │ Discovery     │──>│ Signal Engine │──>│ Executor         │ │
│  │ (every 30s)   │   │ (every tick)  │   │ (on signal fire) │ │
│  └──────┬───────┘   └──────┬───────┘   └──────────────────┘ │
│         │                   │                                  │
└─────────┼───────────────────┼──────────────────────────────────┘
          │                   │
    ┌─────▼──────┐    ┌──────▼──────────┐
    │ Market     │    │ Chainlink Feed  │  (WebSocket thread)
    │ Finder     │    │ (live prices +  │
    │ (Gamma API)│    │  volatility)    │
    └────────────┘    └─────────────────┘
                      ┌─────────────────┐
                      │ Tightness       │  (WebSocket thread)
                      │ Tracker         │
                      │ (Polymarket     │
                      │  odds feed)     │
                      └─────────────────┘
```

### Files

| File                   | Role                                                                                                                                       |
| ---------------------- | ------------------------------------------------------------------------------------------------------------------------------------------ |
| `coordinator.py`       | Main orchestrator — runs the event loop, discovers markets, triggers signals, executes trades, handles market expiry and outcome recording |
| `signal_engine.py`     | Core decision logic — evaluates reversal potential using underdog price, tight_ratio, and momentum signals                                 |
| `executor.py`          | Trade execution — places FOK orders via CLOB API, tracks daily loss, records trades to JSON, updates outcomes post-resolution              |
| `market_finder.py`     | Market discovery — queries Gamma API for active 15-min crypto markets, parses token IDs and time windows                                   |
| `chainlink_feed.py`    | Real-time price data — Chainlink WebSocket feed for BTC/ETH/SOL/XRP, calculates rolling volatility and expected moves                      |
| `tightness_tracker.py` | Odds monitoring — Polymarket WebSocket feed, records YES/NO price snapshots, tracks how "tight" (close to 50/50) a market is               |
| `models.py`            | Dataclasses for all domain objects (CryptoMarket, OddsSnapshot, TightnessProfile, TightMarketOpportunity, TightMarketTradeResult)          |

---

## The Signal: How Entry Decisions Work (v2 — Reversal-Based)

### Entry Criteria

A signal fires when ALL of these gates pass:

1. **Cheap Side in Range**: `tmc_min_cheap_ask ≤ cheap_side_ask ≤ tmc_max_entry_ask` (default: 0.05–0.30). This ensures the underdog has a meaningful payout (3.3x–20x) but isn't so cheap it has no realistic chance.

2. **Market is Decisive** (`tight_ratio`): `tight_ratio < tmc_max_tight_ratio` (default: 0.40). A low tight_ratio means the market has had a clear favorite — exactly the setup needed for a reversal to pay off.

3. **Contrarian Price Momentum**: Price must NOT be confirming the majority. If the price is moving away from strike (reinforcing the favorite), there is no reversal — skip.

4. **Odds Not Confirming Majority**: The underdog's odds must not be dropping (favorite getting stronger). We block when odds strongly confirm the majority.

5. **In Execution Window**: Signal only fires within `tmc_execution_window` seconds of expiry.

### Why This Works (The Edge)

Historical data shows:

- **10-20% implied probability bucket**: actual WR = 20% vs. implied 14.4% → **EV = +39%**
- `tight_ratio < 0.40` alone turns PnL from **-$13.94 to +$14.15** (ROI +67.4%)
- The strategy removes 33 of 49 historical losses while keeping 5 of 8 wins

### Timeline and Windows

```
Market lifetime (15 minutes):
|=====================================================|
0min                                               15min

                    Entry Window (last 30s):
                                         |===========|
                                         30s       0s (expiry)

                         Execution Window (last 11s):
                                              |======|
                                              11s   0s
```

### Skip Conditions (Signal Does NOT Fire)

- Already fired for this market (one-shot per market)
- Strike price not captured yet
- Outside entry window (>30s or already expired)
- Below min seconds remaining (<5s)
- No Chainlink price available
- CLOB asks not available or invalid (<=0)
- **Cheap side too cheap**: `cheap_side_ask < tmc_min_cheap_ask` (no realistic chance)
- **Cheap side too expensive**: `cheap_side_ask > tmc_max_entry_ask` (low payout, ~50/50 market)
- **Tight ratio too high**: `tight_ratio >= tmc_max_tight_ratio` (market is indecisive)
- **Confirming momentum**: price moving away from strike (favorite getting stronger)
- **Odds confirming majority**: underdog odds are dropping

---

## Discovery and Market Lifecycle

### How Markets Are Found (`market_finder.py`)

1. Polls Gamma API (`GET /markets?active=true&closed=false`)
2. Filters for crypto markets with 15-minute time windows (regex: `HH:MM[AP]M-HH:MM[AP]M`)
3. Validates the asset is in `tmc_crypto_assets` (BTC, ETH, SOL, XRP)
4. Filters by expiry: between 60s and 1200s from now
5. Parses `clobTokenIds` (JSON-encoded string!) to get YES/NO token IDs
6. Returns `CryptoMarket` objects

### Market Lifecycle (managed by `coordinator.py`)

```
DISCOVERED ──> TRACKED ──> STRIKE CAPTURED ──> SIGNAL EVALUATION ──> EXPIRED
    │              │              │                    │                  │
    │              │              │                    │                  ├─ Get final Binance price
    │              │              │                    │                  ├─ Determine outcome (YES/NO)
    │              │              │                    │                  ├─ Update trade logs with P&L
    │              │              │                    │                  └─ Save shadow log entry
    │              │              │                    │
    │              │              │                    └─ Signal fires → executor.execute()
    │              │              │
    │              │              └─ Binance price at start_date = strike
    │              │
    │              └─ TightnessTracker starts WebSocket subscription
    │
    └─ Gamma API returns market, added to tracked dict
```

---

## Trade Execution

### Order Flow (`executor.py`)

1. **Kill switch check**: If `daily_loss >= tmc_max_daily_loss` ($50 default), reject all trades
2. **Dry run mode** (`config.dry_run=True`): Log simulated trade, save to JSON, return success
3. **Live mode**:
   - Place YES market buy order (FOK) for `amount_per_side` ($5 default)
   - Place NO market buy order (FOK) for `amount_per_side`
   - Record order IDs
   - Add `total_cost` to daily loss tracker
4. Save trade record to `data/tight_market_crypto_trades.json`

### What Gets Bought

The strategy buys **both sides** (YES and NO) at their current ask prices. Since one side will always pay out $1.00 per share at resolution, the profit/loss depends on the total cost:

- **Cost** = `yes_ask + no_ask` per share (both bought at market)
- **Payout** = $1.00 per share (winning side)
- **P&L** = payout - total_cost

Wait — this is NOT pure arbitrage (yes_ask + no_ask is almost always >= $1.00). The strategy actually bets on **one side winning**, buying both sides as a form of position entry. The `amount_per_side` is the same for each, so the net return depends on which side wins and its ask price at entry.

**Correction**: Looking more carefully, the payout calculation is `amount_per_side / winning_ask`, meaning the strategy gets more shares on the cheaper side. The net return is: `(amount_per_side / winning_ask) - total_cost`.

---

## Risk Management

| Mechanism                 | Detail                                                                                           |
| ------------------------- | ------------------------------------------------------------------------------------------------ |
| **Daily loss limit**      | Tracks cumulative cost of trades. Kill switch at $50/day (configurable). Resets at midnight UTC. |
| **One-shot signals**      | Each market can only fire once — prevents repeated entries on the same market.                   |
| **One-sided market skip** | Skips markets where the minority side ask is below threshold (too imbalanced = no edge).         |
| **Execution window**      | Only trades in the final 60s — maximizes information before committing.                          |
| **Volatility boost**      | Increases expected_move threshold near expiry to avoid false signals from noise.                 |
| **FOK orders**            | Fill-or-Kill ensures full fill or no fill — no partial positions.                                |
| **Dry run default**       | `dry_run=True` by default — must explicitly enable live trading.                                 |

---

## Data Logging

### Trade Log (`data/tight_market_crypto_trades.json`)

Every trade (dry run or live) is recorded with:

- Market info (condition_id, question, asset)
- Entry prices (yes_ask, no_ask)
- Signal metrics (distance, expected_move, tight_ratio)
- Execution result (success, order_ids, cost, error)
- **Post-resolution fields** (filled when market expires):
  - `outcome`: "YES" or "NO"
  - `final_crypto_price`: Binance price at expiry
  - `payout`: amount_per_side / winning_ask
  - `net_return`: payout - total_cost
  - `return_pct`: percentage return

### Shadow Log (`data/tight_market_crypto_shadow.json`)

Records **every expiring market** (traded or not) with comprehensive analysis:

- Full price and odds trails during entry/execution windows (1/sec for execution, 1/5sec for entry)
- Skipped signal analysis with reasons
- Reversal detection (did the majority side flip?)
- Price momentum in final seconds
- Min/max distance to strike during execution window

This shadow data is critical for backtesting and tuning parameters.

---

## Configuration Reference

All parameters are set via environment variables (`.env`) and loaded into `Config`:

| Env Variable                    | Default           | Description                                                      |
| ------------------------------- | ----------------- | ---------------------------------------------------------------- |
| `TMC_CRYPTO_ASSETS`             | "BTC,ETH,SOL,XRP" | Comma-separated list of assets to track                          |
| `TMC_ENTRY_WINDOW`              | 180.0             | Seconds before expiry to begin signal evaluation                 |
| `TMC_EXECUTION_WINDOW`          | 60.0              | Seconds before expiry where trades can actually execute          |
| `TMC_VOLATILITY_MULTIPLIER`     | 1.0               | K threshold: lower = stricter signal filter                      |
| `TMC_VOLATILITY_WINDOW`         | 300.0             | Seconds of Binance data for volatility calc                      |
| `TMC_VOLATILITY_BOOST_FACTOR`   | 2.0               | Multiplier for expected_move inside execution window             |
| `TMC_MAX_DISTANCE_RATIO`        | 8.0               | Max raw distance/expected_move ratio to enter trade              |
| `TMC_ODDS_BYPASS_MAX_ASK`       | 0.15              | Max cheap side ask to allow distance ratio bypass (6.7:1 payout) |
| `TMC_BLOCK_CONFIRMING_MOMENTUM` | true              | Block when price momentum confirms majority (0% WR)              |
| `TMC_MOMENTUM_THRESHOLD`        | 0.0               | Min momentum ($/s) to count as directional                       |
| `TMC_MAX_INVESTMENT`            | 10.0              | Total USD per trade (split equally: $5 YES + $5 NO)              |
| `TMC_MAX_DAILY_LOSS`            | 50.0              | Kill switch: stop trading if daily loss exceeds this             |
| `TMC_DISCOVERY_INTERVAL`        | 30.0              | Seconds between Gamma API market scans                           |
| `DRY_RUN`                       | true              | Simulate trades without placing real orders                      |

---

## Threading Model

```
Main Thread (coordinator._main_loop):
  - Discovery every 30s
  - Signal evaluation every 0.5s
  - Trade execution (serial)
  - Outcome recording on market expiry

Thread 2 (TightnessTracker):
  - Polymarket WebSocket connection
  - Receives YES/NO ask updates
  - Stores OddsSnapshots in thread-safe dict

Thread 3 (BinancePriceFeed):
  - Binance WebSocket connection
  - Receives price ticks for all tracked assets
  - Maintains price history deques (900 points per asset)
  - Computes volatility on-demand from stored data
```

Data flows from WebSocket threads to main thread via shared dicts. No explicit locks are used on the data structures — the deques and dicts are treated as effectively thread-safe for the read/append patterns used.

---

## Key Gotchas for Future Development

1. **`clobTokenIds` from Gamma API** is a JSON-encoded string, not a list. Must `json.loads()` before indexing.
2. **Signals are one-shot**: Once fired for a market, that market is permanently marked. There's no retry mechanism.
3. **Volatility can be zero**: If Binance has insufficient data, `expected_move=0` and the signal formula divides by zero — this is guarded by checking `expected_move > 0`.
4. **No LLM validation**: Unlike the arbitrage strategy, TMC does NOT use an LLM to validate trades. Decisions are purely mathematical.
5. **Both sides are bought**: The strategy buys YES and NO for the same dollar amount, but payout depends on which side wins and its ask price.
6. **Shadow log grows unbounded**: `tight_market_crypto_shadow.json` accumulates entries forever — may need rotation for long-running deployments.
7. **WebSocket reconnection**: Both Binance and Polymarket WebSocket connections have basic reconnection logic but can silently fail — check for stale data.
8. **Outcome resolution uses Binance price**: The "truth" for whether YES or NO wins comes from Binance (not Polymarket), so there could be edge cases where Polymarket resolves differently than what the bot calculates.
