---
name: xt-assets
description: XT asset management. Use when the user wants to check XT account balances / total assets, transfer between accounts, withdraw, or look up deposit/withdrawal chains and fees. Write operations require an API Key and must follow the confirmation flow; withdrawals require a second confirmation.
---

# XT Asset Management

Executed via the `xt-tradekit` MCP tools. Requires an API Key: before authenticated operations, call `xt_credentials_status` to check status. If not configured, follow the flow in the `xt-spot-trade` skill to guide the user to run `setup-credentials.sh` in their own terminal (**Forbidden**: reading the credentials file contents or asking the user for keys).

Permissions: transfers require the Transfer permission, withdrawals require the Withdraw permission. **For AI trading scenarios, enabling Withdraw is not recommended by default**; if the user genuinely needs withdrawal functionality, remind them to understand the risks and bind an IP allowlist.

## Tool Mapping

| Operation | Tool | Notes |
|------|------|------|
| Spot balances / total assets | `xt_spot_balances` | Returns non-zero assets + USDT valuation |
| Futures account equity | `xt_futures_account` | |
| Transfer between accounts | `xt_asset_transfer` | Account types: SPOT / LEVER / FUTURES_U / FUTURES_C / FINANCE |
| Deposit/withdrawal chains | `xt_currency_chains` | Chain name, fee, minimum withdrawal amount, contract address |
| Withdraw | `xt_withdraw` | **Irreversible, requires second confirmation** |

## Checking Total Assets

Call both `xt_spot_balances` and `xt_futures_account`, then present a summary: spot assets table + futures equity + combined valuation.

## Transfer Confirmation

Before executing, display: direction (e.g. Spot → USDT-M Futures), currency, amount, and wait for the user's confirmation.

## ⚠️ Withdrawal Rules (irreversible operation, mandatory second confirmation)

1. When the user provides only an address without specifying a chain, first call `xt_currency_chains` to display the supported chains, fees, and minimum withdrawal amounts, and let the user choose.
2. Before executing, display in full:
   - Currency, chain name, amount
   - Fee, estimated amount received
   - **Full destination address** (do not truncate the middle characters)
3. Explicitly warn: "⚠️ Withdrawals are irreversible; please verify the address and chain."
4. Only call `xt_withdraw` after the user explicitly confirms.
5. When the address format clearly does not match the selected chain (e.g. withdrawing to a 0x-prefixed address on the Tron chain), block the operation and warn.

## Output Guidelines

- The balance table should list only non-zero assets; bold the total valuation.
- After a successful transfer/withdrawal, display the returned transferId / withdrawId.

> If the `xt-tradekit` MCP tools are unavailable, first install the MCP server via the `xt-tradekit-setup` skill.
