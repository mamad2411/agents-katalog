---
name: xt-futures-trade
description: XT USDT perpetual futures trading. Use when the user wants to open long/short positions, close positions, check positions, place or cancel futures orders, or check futures account equity on XT. Write operations require an API Key and must follow the confirmation flow.
---

# XT Futures Trading (USDT-M Perpetual)

Executed via the `xt-tradekit` MCP tools. Symbol format: `btc_usdt`.

## API Key Onboarding

Before authenticated operations, call the `xt_credentials_status` tool to check (no keys included). If not configured, follow the flow in the `xt-spot-trade` skill to guide the user to run `setup-credentials.sh` in **their own terminal**. **Forbidden**: reading the credentials file contents or asking the user for keys. Futures trading shares the same Key as spot.

## Contract Quantity Conversion (critical!)

The order quantity unit for XT futures is **contracts** (integers), not coin quantity:

1. Before placing an order, first call `xt_futures_contract_info` to get `contractSize` (face value per contract, e.g. BTC=0.001 BTC/contract, ETH=0.01 ETH/contract).
2. User says "buy 0.1 ETH" → 0.1 / 0.01 = **10 contracts**; user says "open a 500 USDT position" → first look up the current price to convert to coin quantity, then divide by the face value.
3. Show the user the conversion result (contract count + equivalent coin quantity + approximate USDT) before confirming.

## Tool Mapping

| Operation | Tool | Key parameters |
|------|------|---------|
| Account equity | `xt_futures_account` | |
| Current positions | `xt_futures_positions` | Only returns non-zero positions |
| Current orders | `xt_futures_open_orders` | |
| Open long | `xt_futures_place_order` | order_side=BUY, position_side=LONG |
| Open short | `xt_futures_place_order` | order_side=SELL, position_side=SHORT |
| Close long | `xt_futures_place_order` | order_side=SELL, position_side=LONG |
| Close short | `xt_futures_place_order` | order_side=BUY, position_side=SHORT |
| Cancel order | `xt_futures_cancel_order` | requires order_id |
| Order history | `xt_futures_order_history` | |
| Contract specs | `xt_futures_contract_info` | contractSize/precision/max leverage |

For limit orders pass `order_type=LIMIT` + price; for market orders pass `order_type=MARKET` (no price).

## Position-Closing Flow

1. First call `xt_futures_positions` to display current positions (direction, contract count, closeable contract count, average entry price).
2. When the user does not specify a quantity, close the entire position by default (using availableCloseSize), and note this in the confirmation.

## ⚠️ Safety Confirmation (mandatory)

**Before executing** opening / closing / canceling:

1. Display: contract, direction (open long/open short/close long/close short), type, price (mark as market if market order), contract count and equivalent coin quantity, approximate USDT.
2. Futures trading involves leverage; on the first position opening, add a one-line risk reminder (do not repeat it verbosely).
3. Only execute after the user explicitly confirms.

## Output Guidelines

- Use tables for positions/orders; bold prices and PnL.
- Display small decimal fields such as funding rate and change percentage as percentages.

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
