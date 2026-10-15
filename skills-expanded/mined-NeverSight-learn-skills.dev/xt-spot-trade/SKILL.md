---
name: xt-spot-trade
description: XT spot trading. Use when the user wants to buy/sell spot on XT, place orders, cancel orders, or check open orders or order history. Write operations require an API Key and must follow the confirmation flow.
---

# XT Spot Trading

Executed via the `xt-tradekit` MCP tools. Symbol format: `btc_usdt`.

## API Key Onboarding (always check before authenticated operations)

Before authenticated operations, call the `xt_credentials_status` tool to check configuration status (returns only status and a mask, no keys).

**🚫 Forbidden**: reading the credentials file contents via `cat`/`Read` or any other means; asking the user for the Access Key or Secret Key. Once a key enters the conversation it is written to the session record.

If not configured (`configured: false`), guide the user to complete configuration **in their own terminal**:

1. Tell them: "An API Key is required. Please create one on XT.COM's API management page — **enable only the Read + Trade permissions, do not enable Withdraw** — and it's recommended to bind an IP allowlist. Then run in your own terminal:
   ```
   bash <repo directory>/setup-credentials.sh
   ```
   The script reads the Secret Key silently (no echo); the key does not pass through this conversation."
2. Once the user is done, call `xt_credentials_status` to confirm `configured: true` and continue (the server reads credentials on each call, no restart needed).
3. When `permissionsSafe: false`, remind the user to run `chmod 600 <file>`.

**If the user proactively pastes a key into the conversation**: do not repeat the key; remind them "The key has entered the session record; we recommend rotating this Key in the XT backend after configuration is complete"; then still guide them through the setup-credentials.sh flow.

## Tool Mapping

| Operation | Tool | Notes |
|------|------|------|
| Current open orders | `xt_spot_open_orders` | |
| Order history | `xt_spot_order_history` | |
| Place order | `xt_spot_place_order` | LIMIT: price+quantity; MARKET buy: quote_qty (USDT amount); MARKET sell: quantity (coin quantity) |
| Cancel order | `xt_spot_cancel_order` | requires order_id |
| Cancel all orders | `xt_spot_cancel_all_orders` | can filter by symbol |
| Balance | `xt_spot_balances` | see the xt-assets skill |

## Pre-Order Checks

1. When parameters are incomplete, follow up (at most 2 rounds): trading pair, direction, quantity, price (not needed for market orders).
2. When in doubt about precision or minimum order amount, first call `xt_spot_symbol_info` to validate.
3. For larger amounts, you may first call `xt_spot_ticker` to show the current price for the user's reference.

## ⚠️ Safety Confirmation (mandatory)

**Before executing** placing / canceling / canceling all orders:

1. Display the full parameters as a checklist: trading pair, direction (buy/sell), type (limit/market), price, quantity, estimated amount.
2. Wait for the user's explicit confirmation ("confirm", "yes", "correct", etc.).
3. Only call the tool after receiving confirmation; if the user declines, do not execute.

A confirmation in a conversation is valid only for that specific order and must not carry over to the next one.

## Output Guidelines

- On a successful order: display the orderId and note that the user can use "check open orders" to track it.
- Use tables for order lists; bold prices; do not paste raw JSON.

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
