---
name: market-maker
description: Create a market maker bot for Turbine's BTC 15-minute prediction markets. Use when building trading bots for Turbine.
disable-model-invocation: true
argument-hint: "[algorithm-type]"
---

# Turbine Market Maker Bot Generator

You are helping a programmer create a market maker bot for Turbine's Bitcoin 15-minute prediction markets.

## Step 0: Environment Context Detection

Before writing Python code, check the project's Python version requirements by reading `pyproject.toml` (if it exists) to determine syntax compatibility.

**Environment Rules:**
- If Python version is 3.9+: Use modern syntax (`list[str]`, `dict[str, int]`, `X | None`)
- If Python version is 3.8 or below: Use `from typing import List, Dict, Optional`
- Use `async`/`await` syntax (supported in all Python 3.9+ environments)
- For dataclasses, use `@dataclass` decorator (available in Python 3.7+)

## Step 1: Environment Setup Check

First, check if the user has the required setup:

1. Check if `turbine_client` is importable by looking at the project structure
2. Check if `.env` file exists with the required credentials
3. If `.env` doesn't exist, guide them through creating it

## Step 2: Private Key Setup

Check if .env file exists with TURBINE_PRIVATE_KEY set. If not:

1. Create a `.env` template file with placeholder values (never ask for or handle actual private keys):
```
# Turbine Trading Bot Configuration
# IMPORTANT: Add your private key below, then save this file.
# Use a dedicated trading wallet with limited funds.
# Get it from MetaMask: Settings > Security & Privacy > Export Private Key
TURBINE_PRIVATE_KEY=
TURBINE_API_KEY_ID=
TURBINE_API_PRIVATE_KEY=
```
2. Tell the user to open `.env` in their editor and paste their private key themselves
3. Remind them of security best practices:
   - Use a dedicated trading wallet with limited funds
   - Never share your private key with anyone or any tool
   - The `.env` file is gitignored and stays local

Never ask for, accept, or write a user's private key. The user must edit the `.env` file themselves.

## Step 3: API Key Auto-Registration

The generated bot should auto-register API credentials on first run using the SDK's `TurbineClient.request_api_credentials()` method. This uses EIP-712 signature authentication (the private key signs a challenge locally — it is never transmitted).

If `examples/price_action_bot.py` exists in the project, read it and copy its credential registration pattern. Otherwise, use the template code below in the generated bot:

```python
# --- Generated bot runtime code (not executed by the agent) ---
import os
import re
from pathlib import Path
from turbine_client import TurbineClient

def get_or_create_api_credentials(env_path: Path = None):
    """Get existing API credentials or register new ones via EIP-712 signature.

    The private key is used locally to sign an authentication challenge.
    It is never transmitted — only the signature is sent to the API.
    """
    if env_path is None:
        env_path = Path(__file__).parent / ".env"

    api_key_id = os.environ.get("TURBINE_API_KEY_ID")
    api_private_key = os.environ.get("TURBINE_API_PRIVATE_KEY")

    if api_key_id and api_private_key:
        print("Using existing API credentials")
        return api_key_id, api_private_key

    private_key = os.environ.get("TURBINE_PRIVATE_KEY")
    if not private_key:
        raise ValueError("Set TURBINE_PRIVATE_KEY in your .env file")

    print("Registering new API credentials...")
    credentials = TurbineClient.request_api_credentials(
        host="https://api.turbinefi.com",
        private_key=private_key,
    )

    api_key_id = credentials["api_key_id"]
    api_private_key = credentials["api_private_key"]

    # Save API keys (not the private key) to .env for future runs
    _append_api_keys_to_env(env_path, api_key_id, api_private_key)
    os.environ["TURBINE_API_KEY_ID"] = api_key_id
    os.environ["TURBINE_API_PRIVATE_KEY"] = api_private_key

    print(f"API credentials saved to {env_path}")
    return api_key_id, api_private_key


def _append_api_keys_to_env(env_path: Path, api_key_id: str, api_private_key: str):
    """Append or update only API key values in an existing .env file.

    Never writes TURBINE_PRIVATE_KEY — that is managed by the user.
    """
    env_path = Path(env_path)
    if not env_path.exists():
        return  # User must create .env themselves

    content = env_path.read_text()
    if "TURBINE_API_KEY_ID=" in content:
        content = re.sub(r'^TURBINE_API_KEY_ID=.*$', f'TURBINE_API_KEY_ID={api_key_id}', content, flags=re.MULTILINE)
    else:
        content = content.rstrip() + f"\nTURBINE_API_KEY_ID={api_key_id}"
    if "TURBINE_API_PRIVATE_KEY=" in content:
        content = re.sub(r'^TURBINE_API_PRIVATE_KEY=.*$', f'TURBINE_API_PRIVATE_KEY={api_private_key}', content, flags=re.MULTILINE)
    else:
        content = content.rstrip() + f"\nTURBINE_API_PRIVATE_KEY={api_private_key}"
    env_path.write_text(content + "\n")
```

## Step 4: Algorithm Selection

Present the user with these trading algorithm options for prediction markets:

**Option 1: Price Action Trader (Recommended)**
- Uses real-time BTC price from Pyth Network (same oracle Turbine uses)
- Compares current price to the market's strike price
- If BTC is above strike price → buy YES (bet it stays above)
- If BTC is below strike price → buy NO (bet it stays below)
- Adjusts confidence based on how far price is from strike
- Best for: Beginners, following price momentum
- Risk: Medium - follows current price action

**Option 2: Simple Spread Market Maker**
- Places bid and ask orders around the mid-price with a fixed spread
- Best for: Learning the basics, stable markets
- Risk: Medium - can accumulate inventory in trending markets

**Option 3: Inventory-Aware Market Maker**
- Adjusts quotes based on current position to reduce inventory risk
- Skews prices to encourage trades that reduce position
- Best for: Balanced exposure, risk management
- Risk: Lower - actively manages inventory

**Option 4: Momentum-Following Trader**
- Detects price direction from recent trades
- Buys when momentum is up, sells when momentum is down
- Best for: Trending markets, breakouts
- Risk: Higher - can be wrong on reversals

**Option 5: Mean Reversion Trader**
- Fades large moves expecting price to revert
- Buys after dips, sells after spikes
- Best for: Range-bound markets, overreactions
- Risk: Higher - can fight strong trends

**Option 6: Probability-Weighted Trader**
- Uses distance from 50% as a signal
- Bets on extremes reverting toward uncertainty
- Best for: Markets with overconfident pricing
- Risk: Medium - based on market efficiency assumptions

## Reference Implementation

A complete, production-ready implementation exists for the **Price Action Trader**:

**`examples/price_action_bot.py`**
- Signs a single gasless max USDC permit per settlement contract on first trade
- All subsequent orders use the existing allowance (no per-order permit overhead)
- Order sizing in USDC terms with position tracking

When generating a bot:
1. **Read `examples/price_action_bot.py`** as the primary reference
2. Copy the structure exactly, customizing only configuration parameters as needed
3. **DO NOT** use the simplified code snippets in this skill - they are incomplete

For **other algorithm options**, use the same bot structure but replace the algorithm-specific methods:
- `calculate_signal()` - Replace with the chosen algorithm's signal logic
- `execute_signal()` - Adapt order placement to match the algorithm
- `price_action_loop()` - Rename and adapt the main loop for the algorithm

The reference implementations include critical patterns that **MUST** be preserved in all bots:
- Position syncing from API (`sync_position()`, `verify_position()`)
- Pending order TX tracking (`pending_order_txs` set)
- Trade verification (check failed_trades, pending_trades, recent trades)
- Market transition detection with `market_expiring` flag
- Unclaimed winnings discovery from previous sessions
- Rate-limited claiming (15s delay between claims)
- Async HTTP client for non-blocking external API calls
- Gasless max permit approval when entering new markets (`ensure_settlement_approved()`)
- USDC-based order sizing (`calculate_shares_from_usdc()`)
- Position tracking in USDC terms (`position_usdc` dict)

## Step 5: Generate the Bot Code

Based on the user's algorithm choice, generate a complete bot file. The bot should:

1. Load credentials from environment variables
2. Auto-register API keys if needed
3. Connect to the BTC 15-minute quick market
4. Implement the chosen algorithm
5. Include proper error handling
6. Cancel orders on shutdown
7. **Automatically detect new BTC markets and switch liquidity/trades to them**
8. Handle market expiration gracefully with seamless transitions
9. **Handle gasless USDC approval** via one-time max permit per settlement contract
10. **Track traded markets and automatically claim winnings when they resolve**

Use `examples/price_action_bot.py` as the primary reference

Use `examples/price_action_bot.py` as the structural template for all bots. The generated bot should follow this high-level structure:

```python
"""
Turbine Market Maker Bot - {ALGORITHM_NAME}
Generated for Turbine

Algorithm: {ALGORITHM_DESCRIPTION}
"""

import asyncio
import os
import time
from dotenv import load_dotenv
import httpx  # For Price Action Trader - fetching BTC price from Pyth Network

from turbine_client import TurbineClient, TurbineWSClient, Outcome, Side
from turbine_client.exceptions import TurbineApiError, WebSocketError

# Load environment variables
load_dotenv()

# ============================================================
# CONFIGURATION - Adjust these parameters for your strategy
# ============================================================
ORDER_SIZE = 1_000_000  # 1 share (6 decimals)
MAX_POSITION = 5_000_000  # Maximum position size (5 shares)
QUOTE_REFRESH_SECONDS = 30  # How often to refresh quotes
# Algorithm-specific parameters added here...

# Credential registration — include get_or_create_api_credentials()
# from Step 3 above (or copy from examples/price_action_bot.py if available)


class MarketMakerBot:
    """Market maker bot implementation with automatic market switching and winnings claiming."""

    def __init__(self, client: TurbineClient):
        self.client = client
        self.market_id: str | None = None
        self.settlement_address: str | None = None  # For USDC approval
        self.contract_address: str | None = None  # For claiming winnings
        self.strike_price: int = 0  # BTC price when market created (6 decimals) - used by Price Action Trader
        self.current_position = 0
        self.active_orders: dict[str, str] = {}  # order_hash -> side
        self.running = True
        # Track markets we've traded in for claiming winnings
        self.traded_markets: dict[str, str] = {}  # market_id -> contract_address
        # Algorithm state...

    async def get_active_market(self) -> tuple[str, int, int]:
        """
        Get the currently active BTC quick market.
        Returns (market_id, end_time, start_price) tuple.
        """
        quick_market = self.client.get_quick_market("BTC")
        return quick_market.market_id, quick_market.end_time, quick_market.start_price

    async def cancel_all_orders(self, market_id: str) -> None:
        """Cancel all active orders on a market before switching."""
        if not self.active_orders:
            return

        print(f"Cancelling {len(self.active_orders)} orders on market {market_id[:8]}...")
        for order_id in list(self.active_orders.keys()):
            try:
                self.client.cancel_order(market_id=market_id, order_id=order_id)
                del self.active_orders[order_id]
            except TurbineApiError as e:
                print(f"Failed to cancel order {order_id}: {e}")

    async def switch_to_new_market(self, new_market_id: str, start_price: int = 0) -> None:
        """
        Switch liquidity and trading to a new market.
        Called when a new BTC 15-minute market becomes active.

        Args:
            new_market_id: The new market ID to switch to.
            start_price: The BTC price when market was created (8 decimals).
                         Used by Price Action Trader to compare against current price.
        """
        old_market_id = self.market_id

        # Track old market for claiming winnings later
        if old_market_id and self.contract_address:
            self.traded_markets[old_market_id] = self.contract_address
            print(f"Tracking market {old_market_id[:8]}... for winnings claim")

        if old_market_id:
            print(f"\n{'='*50}")
            print(f"MARKET TRANSITION DETECTED")
            print(f"Old market: {old_market_id[:8]}...")
            print(f"New market: {new_market_id[:8]}...")
            print(f"{'='*50}\n")

            # Cancel all orders on the old market
            await self.cancel_all_orders(old_market_id)

        # Update to new market
        self.market_id = new_market_id
        self.strike_price = start_price  # Store for Price Action Trader
        self.active_orders = {}

        # Fetch settlement and contract addresses from markets list
        try:
            markets = self.client.get_markets()
            for market in markets:
                if market.id == new_market_id:
                    self.settlement_address = market.settlement_address
                    self.contract_address = market.contract_address
                    print(f"Settlement: {self.settlement_address[:16]}...")
                    print(f"Contract: {self.contract_address[:16]}...")
                    break
        except Exception as e:
            print(f"Warning: Could not fetch market addresses: {e}")

        strike_usd = start_price / 1e6 if start_price else 0
        print(f"Now trading on market: {new_market_id[:8]}...")
        if strike_usd > 0:
            print(f"Strike price: ${strike_usd:,.2f}")

    async def monitor_market_transitions(self) -> None:
        """
        Background task that polls for new markets and triggers transitions.
        Runs continuously while the bot is active.
        """
        POLL_INTERVAL = 5  # Check every 5 seconds

        while self.running:
            try:
                new_market_id, end_time, start_price = await self.get_active_market()

                # Check if market has changed
                if new_market_id != self.market_id:
                    await self.switch_to_new_market(new_market_id, start_price)

                # Log time remaining periodically
                time_remaining = end_time - int(time.time())
                if time_remaining <= 60 and time_remaining > 0:
                    print(f"Market expires in {time_remaining}s - preparing for transition...")

            except Exception as e:
                print(f"Market monitor error: {e}")

            await asyncio.sleep(POLL_INTERVAL)

    # ... Algorithm implementation ...


async def main():
    private_key = os.environ.get("TURBINE_PRIVATE_KEY")
    if not private_key:
        print("Error: Set TURBINE_PRIVATE_KEY in your .env file")
        print("Run: claude \"/turbine-setup\" to get started")
        return

    api_key_id, api_private_key = get_or_create_api_credentials()

    client = TurbineClient(
        host="https://api.turbinefi.com",
        chain_id=137,  # Polygon mainnet
        private_key=private_key,
        api_key_id=api_key_id,
        api_private_key=api_private_key,
    )

    print(f"Bot wallet address: {client.address}")

    quick_market = client.get_quick_market("BTC")
    print(f"Initial market: BTC @ ${quick_market.start_price / 1e6:,.2f}")

    bot = MarketMakerBot(client)

    try:
        await bot.switch_to_new_market(quick_market.market_id, quick_market.start_price)
        await bot.run("https://api.turbinefi.com")
    except KeyboardInterrupt:
        print("\nShutting down...")
    finally:
        bot.running = False
        if bot.market_id:
            await bot.cancel_all_orders(bot.market_id)
        client.close()
        print("Bot stopped cleanly.")


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 6: Verify .env File and Install Dependencies

1. Check if `.env` already exists with `TURBINE_PRIVATE_KEY` set (non-empty value). If not, the template was already created in Step 2 — remind the user to open it and add their key manually.

2. Install dependencies by running:
```bash
pip install -e . python-dotenv httpx
```

Note: `httpx` is used by the Price Action Trader to fetch real-time BTC prices from Pyth Network.

## Step 7: Explain How to Run and Deploy

Tell the user:

```
Your bot is ready! To run it:

  python {bot_filename}.py

The bot will:
- Automatically register API credentials on first run (saved to .env)
- Connect to the current BTC 15-minute market
- Gaslessly approve USDC on first trade per settlement (one-time max permit, no gas needed)
- Start trading based on your chosen algorithm
- Automatically switch to new markets when they start
- Track traded markets and claim winnings when they resolve

To stop the bot, press Ctrl+C.


Want to run your bot 24/7 in the cloud? Deploy to Railway (free $5 credit for 30 days):

  claude "/railway-deploy"
```

## Core Bot Run Method

Every generated bot must include this `run()` method that handles WebSocket streaming with automatic market switching and winnings claiming:

```python
async def run(self, host: str) -> None:
    """
    Main trading loop with WebSocket streaming, automatic market switching, and winnings claiming.
    """
    ws = TurbineWSClient(host)

    # Start background tasks
    monitor_task = asyncio.create_task(self.monitor_market_transitions())
    claim_task = asyncio.create_task(self.claim_resolved_markets())

    while self.running:
        try:
            # Ensure we have a current market
            if not self.market_id:
                market_id, _ = await self.get_active_market()
                await self.switch_to_new_market(market_id)

            current_market = self.market_id

            async with ws.connect() as stream:
                # Subscribe to the current market
                await stream.subscribe(current_market)
                print(f"Subscribed to market {current_market[:8]}...")

                # Place initial quotes
                await self.place_quotes()

                async for message in stream:
                    # Check if market has changed (set by monitor task)
                    if self.market_id != current_market:
                        print("Market changed, reconnecting to new market...")
                        break  # Exit inner loop to reconnect

                    if message.type == "orderbook":
                        await self.on_orderbook_update(message.orderbook)
                    elif message.type == "trade":
                        await self.on_trade(message.trade)
                    elif message.type == "order_cancelled":
                        self.on_order_cancelled(message.data)

        except WebSocketError as e:
            print(f"WebSocket error: {e}, reconnecting...")
            await asyncio.sleep(1)
        except Exception as e:
            print(f"Unexpected error: {e}")
            await asyncio.sleep(5)

    # Cleanup background tasks
    monitor_task.cancel()
    claim_task.cancel()
```

## Algorithm Implementation Details

When generating bots, use these implementations:

### Price Action Trader (Recommended)

**⚠️ IMPORTANT: Use the reference implementation at `examples/price_action_bot.py`**

Read that file for the complete, production-ready implementation. The simplified snippet below is **incomplete** and missing critical patterns.

**Key methods in the reference implementation:**

- `get_current_btc_price()` - Fetches BTC price from Pyth Network (async, non-blocking)
- `calculate_signal()` - Returns (action, confidence) based on price vs strike
- `execute_signal()` - Places orders with proper verification flow
- `price_action_loop()` - Main trading loop
- `sync_position()` / `verify_position()` - Position management
- `cleanup_pending_orders()` - Handles settling orders
- `discover_unclaimed_markets()` - Finds winnings from previous sessions

**The reference implementation handles (that the snippet below does NOT):**

- Async HTTP client for non-blocking price fetches
- Position verification after every order attempt
- Pending order tracking to prevent double-ordering
- Failed trade detection immediately after submission
- Market expiration flag to stop trading 60s before expiry
- Processed trade ID tracking to avoid double-counting fills
- Rate-limited claiming with 15s delays

**Algorithm summary:**

- Fetches current BTC price from Pyth Network (same oracle Turbine uses)
- Compares to market's strike price (stored in `quick_market.start_price`, 6 decimals)
- If BTC > strike by threshold → buy YES
- If BTC < strike by threshold → buy NO
- Confidence scales with distance from strike (capped at 90%)

### Simple Spread Market Maker
```python
SPREAD_BPS = 200  # 2% total spread (1% each side)

def calculate_quotes(self, mid_price):
    """Calculate bid/ask around mid price."""
    half_spread = (mid_price * SPREAD_BPS) // 20000
    bid = max(1, mid_price - half_spread)
    ask = min(999999, mid_price + half_spread)
    return bid, ask
```

### Inventory-Aware Market Maker
```python
SPREAD_BPS = 200
SKEW_FACTOR = 50  # BPS skew per share of inventory

def calculate_quotes(self, mid_price):
    """Skew quotes based on inventory."""
    half_spread = (mid_price * SPREAD_BPS) // 20000

    # Skew to reduce inventory
    inventory_shares = self.current_position / 1_000_000
    skew = int(inventory_shares * SKEW_FACTOR)

    bid = max(1, mid_price - half_spread - skew)
    ask = min(999999, mid_price + half_spread - skew)
    return bid, ask
```

### Momentum Following
```python
MOMENTUM_WINDOW = 10  # Number of trades to consider
MOMENTUM_THRESHOLD = 0.6  # 60% same direction = trend

def detect_momentum(self, recent_trades):
    """Detect market momentum from recent trades."""
    if len(recent_trades) < MOMENTUM_WINDOW:
        return None

    buys = sum(1 for t in recent_trades[-MOMENTUM_WINDOW:] if t["side"] == "BUY")
    buy_ratio = buys / MOMENTUM_WINDOW

    if buy_ratio > MOMENTUM_THRESHOLD:
        return "UP"
    elif buy_ratio < (1 - MOMENTUM_THRESHOLD):
        return "DOWN"
    return None
```

### Mean Reversion
```python
REVERSION_THRESHOLD = 50000  # 5% move triggers fade
LOOKBACK_TRADES = 20

def should_fade(self, current_price, recent_trades):
    """Check if price moved enough to fade."""
    if len(recent_trades) < LOOKBACK_TRADES:
        return None

    avg_price = sum(t["price"] for t in recent_trades) / len(recent_trades)
    deviation = current_price - avg_price

    if deviation > REVERSION_THRESHOLD:
        return "SELL"  # Fade the up move
    elif deviation < -REVERSION_THRESHOLD:
        return "BUY"  # Fade the down move
    return None
```

### Probability-Weighted
```python
EDGE_THRESHOLD = 200000  # 20% from 50% = extreme

def find_edge(self, best_bid, best_ask):
    """Look for mispriced extremes."""
    mid = (best_bid + best_ask) // 2
    distance_from_fair = abs(mid - 500000)

    if distance_from_fair > EDGE_THRESHOLD:
        if mid > 500000:
            return "SELL"  # Market too bullish
        else:
            return "BUY"  # Market too bearish
    return None
```

## Automatic Market Transition

**All generated bots automatically handle market transitions.** When a BTC 15-minute market expires:

1. **Detection**: The bot polls every 5 seconds for new markets
2. **Order Cleanup**: All active orders on the expiring market are cancelled
3. **Seamless Switch**: The bot automatically connects to the new market
4. **Continued Trading**: Trading resumes on the new market without manual intervention

**How it works:**
- A background task (`monitor_market_transitions`) runs continuously
- It compares the current market ID with the active market from the API
- When a new market is detected, `switch_to_new_market()` handles the transition
- Positions carry over (they're wallet-based), but orders must be re-placed

**Warning before expiration:**
- When less than 60 seconds remain, the bot logs a warning
- Orders are cancelled proactively to avoid stuck orders on expired markets

## USDC Approval

Bots use a **one-time gasless max permit** for USDC approval. On first trade per settlement contract, the bot signs an EIP-2612 max permit (max value, max deadline) and submits it via the relayer. No native gas is required.

```python
def ensure_settlement_approved(self, settlement_address: str) -> None:
    """Ensure USDC is approved for this settlement contract via gasless max permit."""
    if settlement_address in self.approved_settlements:
        return

    # Check on-chain allowance
    current = self.client.get_usdc_allowance(spender=settlement_address)
    if current >= MAX_APPROVAL_THRESHOLD:  # half of max uint256
        self.approved_settlements[settlement_address] = current
        return

    # Sign and submit gasless max permit via relayer
    result = self.client.approve_usdc_for_settlement(settlement_address)
    # Wait for TX confirmation...
    self.approved_settlements[settlement_address] = 2**256 - 1
```

**Key points:**

- Call `ensure_settlement_approved()` when entering each new market
- Orders submitted without `permit_signature` field — Settlement uses existing allowance
- No native gas token required (relayer pays gas)
- One-time per settlement contract — all future orders reuse the allowance
- Order size specified in USDC terms, converted to shares based on price

## Automatic Winnings Claiming

**Bots must track markets they've traded in and automatically claim winnings when markets resolve.**

### Implementation Pattern

Add these fields to your bot class:

```python
class MarketMakerBot:
    def __init__(self, client: TurbineClient):
        self.client = client
        self.market_id: str | None = None
        self.settlement_address: str | None = None
        self.contract_address: str | None = None  # Current market contract
        self.current_position = 0
        self.active_orders: dict[str, str] = {}
        self.running = True
        # Track markets we've traded in for claiming winnings
        # market_id -> contract_address
        self.traded_markets: dict[str, str] = {}
```

### Track Markets When Switching

When switching to a new market, save the old market for later claiming:

```python
async def switch_to_new_market(self, new_market_id: str, start_price: int = 0) -> None:
    """Switch liquidity to a new market.

    Args:
        new_market_id: The new market ID.
        start_price: BTC strike price (6 decimals) - used by Price Action Trader.
    """
    old_market_id = self.market_id

    # Track old market for claiming winnings later
    if old_market_id and self.contract_address:
        self.traded_markets[old_market_id] = self.contract_address
        print(f"Tracking market {old_market_id[:16]}... for winnings claim")

    if old_market_id:
        await self.cancel_all_orders()

    self.market_id = new_market_id
    self.strike_price = start_price  # Store for Price Action Trader
    self.active_orders = {}

    # Fetch settlement and contract addresses
    markets = self.client.get_markets()
    for market in markets:
        if market.id == new_market_id:
            self.settlement_address = market.settlement_address
            self.contract_address = market.contract_address
            break

    if start_price:
        print(f"Strike price: ${start_price / 1e6:,.2f}")
```

### Background Task for Claiming

Add a background task that checks for resolved markets and claims winnings:

```python
async def claim_resolved_markets(self) -> None:
    """Background task to claim winnings from resolved markets."""
    while self.running:
        try:
            if not self.traded_markets:
                await asyncio.sleep(30)
                continue

            markets_to_remove = []
            for market_id, contract_address in list(self.traded_markets.items()):
                try:
                    # Check if market is resolved
                    markets = self.client.get_markets()
                    market_resolved = False
                    for market in markets:
                        if market.id == market_id and market.resolved:
                            market_resolved = True
                            break

                    if market_resolved:
                        print(f"\nMarket {market_id[:16]}... has resolved!")
                        print(f"Attempting to claim winnings...")
                        try:
                            result = self.client.claim_winnings(contract_address)
                            tx_hash = result.get("txHash", result.get("tx_hash", "unknown"))
                            print(f"Winnings claimed! TX: {tx_hash}")
                            markets_to_remove.append(market_id)
                        except TurbineApiError as e:
                            if "no winnings" in str(e).lower() or "no position" in str(e).lower():
                                print(f"No winnings to claim for {market_id[:16]}...")
                                markets_to_remove.append(market_id)
                            else:
                                print(f"Failed to claim winnings: {e}")
                except Exception as e:
                    print(f"Error checking market {market_id[:16]}...: {e}")

            # Remove claimed markets from tracking
            for market_id in markets_to_remove:
                self.traded_markets.pop(market_id, None)

        except Exception as e:
            print(f"Claim monitor error: {e}")

        await asyncio.sleep(30)  # Check every 30 seconds
```

### Start the Claim Task

In the `run()` method, start the claim task alongside other background tasks:

```python
async def run(self, host: str) -> None:
    """Main trading loop with automatic market switching and winnings claiming."""
    ws = TurbineWSClient(host=host)

    # Start background tasks
    monitor_task = asyncio.create_task(self.monitor_market_transitions())
    claim_task = asyncio.create_task(self.claim_resolved_markets())

    try:
        # ... main trading loop ...
    finally:
        monitor_task.cancel()
        claim_task.cancel()
```

**Key points:**
- `claim_winnings(contract_address)` uses gasless EIP-712 permits
- The API handles all on-chain redemption via a relayer
- Markets are removed from tracking after successful claim or if no position exists
- Check every 30 seconds to catch resolutions promptly

## Critical Patterns (from examples/price_action_bot.py)

These patterns are implemented in the reference example and **MUST** be preserved in all generated bots:

### Position Tracking

- `current_position` tracks net position (YES shares - NO shares)
- `sync_position()` fetches from API on market switch
- `verify_position()` corrects internal tracking after orders

### Pending Order Management

- `pending_order_txs: set[str]` tracks TX hashes of orders being settled
- Don't place new orders while any are pending
- `cleanup_pending_orders()` checks API and clears settled TXs

### Trade Verification Flow

After posting an order:

1. Wait 2 seconds for processing
2. Check `get_failed_trades()` for immediate failures
3. Check `get_pending_trades()` for on-chain settlement
4. Check `get_trades()` for immediate fills
5. Check `get_orders()` for open orders
6. Call `verify_position()` to sync from API

### Market Expiration Handling

- `market_expiring` flag set when <60s remaining
- Don't place new orders when flag is True
- Reset flag when switching to new market
- Clear `processed_trade_ids` and `pending_order_txs` on market switch

### Winnings Discovery

- `discover_unclaimed_markets()` finds positions from previous sessions
- Scans all user positions for winning shares in resolved markets
- Adds discovered markets to claim tracking
- Rate-limited claiming with 15s delays between claims

## Important Notes for Users

- **Risk Warning**: Trading involves risk. Start with small sizes.
- **Testnet First**: Consider testing on Base Sepolia (chain_id=84532) first.
- **Monitor Positions**: Always monitor your bot and have stop-loss logic.
- **Market Expiration**: BTC 15-minute markets expire quickly. Bots handle this automatically!
- **Gas/Fees**: Trading on Polygon has minimal gas costs but watch for fees.
- **Continuous Operation**: Bots are designed to run 24/7, switching between markets automatically.
- **USDC Approval**: Bots use a one-time gasless max permit per settlement contract. No native gas required.

## Quick Reference

**Price Scaling**: Prices are 0-1,000,000 representing 0-100%
- 500000 = 50% probability
- 250000 = 25% probability

**Size Scaling**: Sizes use 6 decimals
- 1_000_000 = 1 share
- 500_000 = 0.5 shares

**Outcome Values**:
- Outcome.YES (0) = BTC ends ABOVE strike price
- Outcome.NO (1) = BTC ends BELOW strike price

**Strike Price (for Price Action Trader)**:
- Available via `quick_market.start_price` (6 decimals)
- Example: 95000000000 = $95,000.00
- Current BTC price fetched from Pyth Network (same oracle Turbine uses):
  - URL: `https://hermes.pyth.network/v2/updates/price/latest?ids[]=0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43`
  - BTC Feed ID: `0xe62df6c8b4a85fe1a67db44dc12de5db330f7ac66b72dc658afedf0f4a415b43`
- If current > strike → buy YES, if current < strike → buy NO
