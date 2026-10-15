---
name: perpetual-trading
description: Trade perpetual futures on GRVT exchange using the grvt-pysdk. Use when the user wants to place, cancel, or manage perpetual orders.
---

# Perpetual Trading on GRVT

## When to Use

Use this skill when the user wants to:
- Place buy/sell orders on GRVT perpetual markets
- Cancel orders (single or all)
- Set take-profit / stop-loss orders
- Check order status or open orders
- View order history or fill history

## Prerequisites

```bash
pip install grvt-pysdk
```

GRVT has two types of API keys. Set the environment variables for the ones you need:

```bash
# Required for this skill — Trading API Key credentials
export GRVT_TRADING_API_KEY="<Trading API Key from GRVT exchange UI>"
export GRVT_TRADING_PRIVATE_KEY="<private key associated with Trading API Key>"

# Optional — Funding API Key credentials (for funding account transfers)
export GRVT_FUNDING_API_KEY="<Funding API Key from GRVT exchange UI>"
export GRVT_FUNDING_PRIVATE_KEY="<private key associated with Funding API Key>"

export GRVT_ENV="testnet"  # or "prod"
```

Both key types can be created at:
- Production: https://exchange.grvt.io/exchange/account/api-keys
- Testnet: https://exchange.testnet.grvt.io/exchange/account/api-keys

**This skill uses `GRVT_TRADING_API_KEY` and `GRVT_TRADING_PRIVATE_KEY`.**

## SDK Setup

Login to auto-detect `trading_account_id` and `funding_account_address`:

```python
import os
import requests
from pathlib import Path
from pysdk.grvt_ccxt import GrvtCcxt
from pysdk.grvt_ccxt_env import GrvtEnv

# Load .env file if present
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

env = os.getenv("GRVT_ENV", "testnet")
base = "edge.testnet.grvt.io" if env == "testnet" else "edge.grvt.io"

# Login returns: sub_account_id, funding_account_address
login_resp = requests.post(
    f"https://{base}/auth/api_key/login",
    json={"api_key": os.getenv("GRVT_TRADING_API_KEY")},
).json()
trading_account_id = login_resp["sub_account_id"]
funding_account_address = login_resp["funding_account_address"]

api = GrvtCcxt(
    env=GrvtEnv.TESTNET if env == "testnet" else GrvtEnv.PRODUCTION,
    parameters={
        "api_key": os.getenv("GRVT_TRADING_API_KEY"),
        "trading_account_id": trading_account_id,
        "private_key": os.getenv("GRVT_TRADING_PRIVATE_KEY"),
    },
)
```

## Symbol Format

Perpetual symbols follow the pattern: `{BASE}_{QUOTE}_Perp`

Examples: `BTC_USDT_Perp`, `ETH_USDT_Perp`, `SOL_USDT_Perp`

To discover available perpetuals:
```python
markets = api.fetch_all_markets()
perps = [m for m in markets if m["kind"] == "PERPETUAL"]
for p in perps:
    print(p["instrument"])  # e.g. "BTC_USDT_Perp"
```

## Placing Orders

### Limit Order

```python
order = api.create_order(
    symbol="BTC_USDT_Perp",
    order_type="limit",
    side="buy",        # "buy" for long, "sell" for short
    amount=0.01,       # Size in base currency (BTC)
    price=90000,       # Limit price in quote currency (USDT)
)
```

### Market Order

```python
order = api.create_order(
    symbol="BTC_USDT_Perp",
    order_type="market",
    side="buy",
    amount=0.01,
    price=0,  # Price is ignored for market orders
)
```

### Order Parameters

Additional parameters can be passed via `params`:

```python
order = api.create_order(
    symbol="BTC_USDT_Perp",
    order_type="limit",
    side="buy",
    amount=0.01,
    price=90000,
    params={
        "client_order_id": 12345,          # Optional custom ID
        "time_in_force": "GTC",            # GTC (default), IOC, FOK, AON
        "post_only": True,                 # Maker-only order
        "reduce_only": True,               # Only reduce existing position
    },
)
```

**Time-in-force options:**
- `GTC` — Good Till Cancel (default)
- `IOC` — Immediate or Cancel (fill what you can, cancel rest)
- `FOK` — Fill or Kill (all or nothing)
- `AON` — All or None

### Take-Profit / Stop-Loss (Trigger Orders)

The SDK's `create_order` does not support trigger orders natively. Use this helper
to place real TP/SL trigger orders that only activate when the trigger price is reached:

```python
from pysdk.grvt_ccxt_utils import get_grvt_order, get_order_payload
from pysdk.grvt_ccxt_env import get_grvt_endpoint

def create_trigger_order(api, symbol, side, amount, limit_price, trigger_type, trigger_price, trigger_by="MARK", reduce_only=True, private_key=None):
    """Place a trigger order (TP/SL).

    Args:
        api: GrvtCcxt instance
        symbol: e.g. "BTC_USDT_Perp"
        side: "buy" or "sell"
        amount: order size
        limit_price: execution price after trigger
        trigger_type: "TAKE_PROFIT" or "STOP_LOSS"
        trigger_price: price that activates the order
        trigger_by: "MARK" (default), "INDEX", "LAST", or "MID"
        reduce_only: True to only reduce position (default)
        private_key: hex private key string
    """
    order = get_grvt_order(
        sub_account_id=api.get_trading_account_id(),
        symbol=symbol,
        order_type="limit",
        side=side,
        amount=amount,
        limit_price=limit_price,
        order_duration_secs=24 * 60 * 60,
        params={"reduce_only": reduce_only},
    )
    payload = get_order_payload(order, private_key=private_key, env=api.env, instruments=api.markets)

    # Inject trigger metadata (unsigned — not part of EIP-712 signature)
    payload["order"]["metadata"]["trigger"] = {
        "trigger_type": trigger_type,
        "tpsl": {
            "trigger_by": trigger_by,
            "trigger_price": str(trigger_price),
            "close_position": False,
        },
    }

    path = get_grvt_endpoint(api.env, "CREATE_ORDER")
    return api._auth_and_post(path, payload)


# Example: Long BTC position, set SL at 68000 (trigger) / 67900 (limit)
result = create_trigger_order(
    api, "BTC_USDT_Perp", side="sell", amount=0.01,
    limit_price=67900, trigger_type="STOP_LOSS", trigger_price=68000,
    private_key=os.getenv("GRVT_TRADING_PRIVATE_KEY"),
)

# Example: Long BTC position, set TP at 75000 (trigger) / 74900 (limit)
result = create_trigger_order(
    api, "BTC_USDT_Perp", side="sell", amount=0.01,
    limit_price=74900, trigger_type="TAKE_PROFIT", trigger_price=75000,
    private_key=os.getenv("GRVT_TRADING_PRIVATE_KEY"),
)
```

**Trigger types:** `TAKE_PROFIT`, `STOP_LOSS`
**Trigger by:** `MARK` (default), `INDEX`, `LAST`, `MID`

The order stays dormant until the trigger price is reached, then becomes a limit order at `limit_price`.

## Cancelling Orders

```python
# Cancel by client_order_id (preferred — works immediately after create_order)
api.cancel_order(id=None, params={"client_order_id": "4224496967"})

# Cancel by order_id (get from fetch_open_orders first)
api.cancel_order(id="0x01010105033f70be000000000515217b")

# Cancel all open orders
api.cancel_all_orders()

# Cancel all perpetual orders only
api.cancel_all_orders(params={"kind": "PERPETUAL"})
```

## Querying Orders

```python
# Get a specific order
order = api.fetch_order(id="<order_id>")

# Get all open orders
open_orders = api.fetch_open_orders(symbol="BTC_USDT_Perp")

# Get order history
history = api.fetch_order_history()

# Get fill/trade history
fills = api.fetch_my_trades(symbol="BTC_USDT_Perp", limit=50)
```

## Order Response

`create_order` returns the order payload. Note: `order_id` in the create response is a placeholder (`0x00`).
To get the real order ID, use `fetch_open_orders` or track by `client_order_id`.

Key fields in the response:
- `order_id` — Exchange-assigned order ID (use from `fetch_open_orders`, not `create_order`)
- `metadata.client_order_id` — Your custom ID (auto-generated if not provided)
- `sub_account_id` — Trading account
- `is_market` — Whether it's a market order
- `time_in_force` — `GOOD_TILL_TIME`, `IMMEDIATE_OR_CANCEL`, `FILL_OR_KILL`, `ALL_OR_NONE`
- `legs[0].instrument` — Symbol (e.g. `BTC_USDT_Perp`)
- `legs[0].size` — Order size
- `legs[0].limit_price` — Limit price
- `legs[0].is_buying_asset` — `true` for buy, `false` for sell

## Position Config (Margin Type & Leverage)

The SDK does not natively support `set_position_config`. Use this helper to switch
between CROSS and ISOLATED margin, and to set leverage per instrument.

```python
import time, random
from pysdk.grvt_ccxt_utils import get_EIP712_domain_data
from eth_account import Account
from eth_account.messages import encode_typed_data

def set_position_config(api, instrument, margin_type, leverage, private_key):
    """Set margin type and leverage for a perpetual instrument.

    Args:
        api: GrvtCcxt instance (authenticated)
        instrument: e.g. "BTC_USDT_Perp"
        margin_type: "ISOLATED" or "CROSS"
        leverage: integer 1-50
        private_key: hex private key string
    """
    MARGIN_TYPE_MAP = {"ISOLATED": 1, "CROSS": 2}
    LEVERAGE_MULTIPLIER = 1_000_000

    market = api.fetch_market(instrument)
    instrument_hash = market["instrument_hash"]
    sub_account_id = int(api._trading_account_id)
    expiration_ns = int((time.time() + 86400) * 1_000_000_000)
    nonce = random.randint(1, 2**32 - 1)

    domain_data = get_EIP712_domain_data(api.env)
    types = {
        "SetSubAccountPositionMarginConfig": [
            {"name": "subAccountID", "type": "uint64"},
            {"name": "asset", "type": "uint256"},
            {"name": "marginType", "type": "uint8"},
            {"name": "leverage", "type": "int32"},
            {"name": "nonce", "type": "uint32"},
            {"name": "expiration", "type": "int64"},
        ]
    }
    message_data = {
        "subAccountID": sub_account_id,
        "asset": instrument_hash,
        "marginType": MARGIN_TYPE_MAP[margin_type],
        "leverage": leverage * LEVERAGE_MULTIPLIER,
        "nonce": nonce,
        "expiration": expiration_ns,
    }

    message = encode_typed_data(domain_data, types, message_data)
    signed = Account.sign_message(message, private_key)
    signer = Account.from_key(private_key)

    payload = {
        "sub_account_id": str(sub_account_id),
        "instrument": instrument,
        "margin_type": margin_type,
        "leverage": str(leverage),
        "signature": {
            "signer": signer.address,
            "r": hex(signed.r),
            "s": hex(signed.s),
            "v": signed.v,
            "expiration": str(expiration_ns),
            "nonce": nonce,
        },
    }

    env_name = api.env.value  # "testnet" or "prod"
    base = "trades.testnet.grvt.io" if "testnet" in env_name else "trades.grvt.io"
    url = f"https://{base}/full/v1/set_position_config"
    return api._auth_and_post(url, payload)


# Usage:
# set_position_config(api, "BTC_USDT_Perp", "ISOLATED", 20, os.getenv("GRVT_PRIVATE_KEY"))
# set_position_config(api, "BTC_USDT_Perp", "CROSS", 10, os.getenv("GRVT_PRIVATE_KEY"))
```

**Constraints:**
- Leverage must be a whole number between 1 and 50
- Cannot change margin type while you have an open position for that instrument
- Close the position first, then switch margin type

## Important Notes

- All orders on perpetuals require EIP-712 signing — the SDK handles this automatically using `GRVT_PRIVATE_KEY`
- The SDK auto-manages authentication sessions and refreshes cookies before expiry
- Use `GrvtEnv.TESTNET` for testing before moving to `GrvtEnv.PRODUCTION`
- Prices use 9 decimal precision internally; the SDK handles conversion
- Minimum notional is 100 USDT — ensure price * amount >= 100
- `create_order` returns `order_id: "0x00"` — use `metadata.client_order_id` to track/cancel
- Always confirm the user wants to proceed before placing real orders on production
