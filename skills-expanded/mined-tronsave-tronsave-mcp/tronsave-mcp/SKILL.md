---
name: tronsave-mcp
description: |
  Operate TronSave through its MCP server: quote and buy TRON ENERGY/BANDWIDTH, manage orders,
  auto-sell settings, API keys and the TronSave internal balance. Use when the user wants to rent
  energy/bandwidth, check TronSave prices, balances or orders, or manage a TronSave account.
metadata:
  author: TronSave
  version: "2.0"
  mcp-server: https://mcp.tronsave.io/mcp
  mcp-server-testnet: https://mcp.tronsave.io/testnet/mcp
---

# TronSave MCP skill

The server also sends these rules in `initialize.instructions`; this file is for frameworks that load skills or system prompts. Tool contracts: `docs/TOOLS.md`.

## Ground rules

1. **Read vs write.** Tools annotated `readOnlyHint: true` may be called freely. Every other tool changes state or spends funds: show a plan and get explicit user confirmation first. One confirmed write per confirmation.
2. **Secrets.** Never ask for or accept private keys or seed phrases. Signatures and signed transactions are produced by the user's wallet, never by you; never edit them. Do not repeat API keys in messages.
3. **Units.** Prices are SUN per resource unit; payment amounts are SUN; 1 TRX = 1,000,000 SUN. `durationSec` is seconds; `extendTo` (internal extend tools) is epoch SECONDS. Show users TRX.
4. **Network.** `/mcp` = mainnet (real funds), `/testnet/mcp` = Nile.
5. **Errors.** Results with `isError: true` carry `{"error":{code,message,retryable,hint}}`. Follow `hint`. Never repeat a write when `retryable` is false. After `UPSTREAM_TIMEOUT`/`UPSTREAM_UNREACHABLE` on a write, the outcome is unknown: verify with a read tool before doing anything else.

## Auth

Call `tronsave_get_session_status` when unsure. It returns `authMode` (`none` | `api-key` | `signature`) and what is available.

| Need | Do |
|---|---|
| Market data, quotes, order list, onchain buy | nothing |
| Internal balance, deposit address, extend request, internal-balance buy | `tronsave_login {apiKey}` (ask the user for their TronSave API key) — skip if the client already sends an `Authorization: ApiKey` header |
| Profile, order update/cancel/manual sell, auto-sell, API-key management | wallet login: `tronsave_get_sign_message` → user signs `message` in their wallet → `tronsave_login {signature: "<signature>_<timestamp>"}` |

On `SESSION_REQUIRED`, `API_KEY_SESSION_REQUIRED` or `INVALID_SESSION_TYPE`: perform the login named in `hint`, then resume. On `SIGNATURE_EXPIRED`: get a new sign message. Never pass session ids as tool arguments.

## Workflows

### W1 Price check (read)
`tronsave_get_min_price` or `tronsave_list_order_books` for market levels; `tronsave_estimate_buy_resource {receiver, buyResourceAmount, durationSec}` for a concrete quote. Report unit price (SUN), total (`estimateTrx / 1e6` TRX) and `availableResource`.

### W2 Buy ENERGY / BANDWIDTH (write)
1. Estimate (W1) for the exact receiver, amount and duration.
2. Choose payment: `internal` if an API key is available and the internal balance (`tronsave_get_internal_account`, SUN) covers `estimateTrx`; otherwise `onchain`, which needs the user's wallet to sign a TRX transfer of `estimateTrx` SUN to `systemDepositAddress` and give you the signed transaction object.
3. Plan + confirmation: receiver, amount, duration, unit price, total TRX, payment method.
4. `tronsave_create_order` with `orderUnitPrice = unitPrice`, `orderDurationSec = durationSec`, `paymentPaymentAmount = estimateTrx`.
5. Check `success`; report `data.orderId`; verify with `tronsave_get_order` (wallet login) or `tronsave_list_orders`.

### W3 Change or cancel an order (write, wallet login)
`tronsave_get_order {id}` → confirm → one of `tronsave_update_order {orderId, newPrice?, receiver?}`, `tronsave_cancel_order {orderId}`, `tronsave_sell_order_manual {orderId, signedTx}` → re-read with `tronsave_get_order`.

### W4 Account overview (read)
`tronsave_get_session_status`, then whichever is unlocked: `tronsave_get_internal_account`, `tronsave_get_user_info`, `tronsave_get_user_auto_setting`, `tronsave_list_orders {isOnlyMyOrder: true}`.

### W5 Top up internal balance (read)
`tronsave_get_deposit_address {amountTrx ≥ 10}` → tell the user to send TRX from their wallet to `depositAddress`.

### W6 Auto-sell (write, wallet login)
Read `tronsave_get_user_auto_setting` first. First time: `tronsave_register_auto_sell`; afterwards `tronsave_update_auto_sell_setting` with only the sections to change. Re-read to verify.

### W7 API keys (write, wallet login)
`tronsave_generate_api_key` returns a secret once: give it to the user, tell them to store it, never repeat it. `tronsave_revoke_api_key` disables the current key. `tronsave_delete_auto_buy_setting {id}` removes an auto-buy rule permanently.

### W8 Extend delegations (write, API key)
`tronsave_list_extendable_delegates` is discovery only. Call `tronsave_internal_extend_delegates {receiver, extendTo (Unix SECONDS)}` to get the `extendData` rows and the cost, show them to the user, then pass the rows unchanged to `tronsave_internal_create_extend_request {receiver, extendData[]}`.

## Output to the user

State what you did, the result (`success`, order id, amounts in TRX), and anything that still needs their action (signing, top-up, confirmation). If an outcome is unknown, say so and show how you verified it.
