---
name: openfin-onramp
author: OpenFinance
homepage: https://openfinance.tech
license: Proprietary
version: 1.0.1
description: Fiat → crypto onramp through OpenFinance. Smart-routed across **Moonpay** (cards / Apple Pay / Google Pay / SEPA / bank — global, non-INR) and **Onramp.money** (UPI / IMPS — INR only). Default to POST /agent/onramp (smart router; `baseCurrency:"inr"` → Onramp.money, anything else → Moonpay). Use POST /agent/onramp/moonpay or /onrampmoney to force a provider. Triggers — "buy USDC with my card", "Apple Pay", "deposit fiat", "fund my wallet", "I have no crypto, how do I start", "buy ETH on Base with USD"; INR triggers — "buy USDC with INR", "deposit ₹1000", "top up with UPI / IMPS", "India onramp". The agent never signs an on-chain tx — user opens the returned URL to complete KYC + payment in the provider's UI; funds land in the user's OpenFinance-managed wallet for the chosen chain. Onramp.money has a **fixed (coin × network) matrix** (usdt:bep20|matic20|erc20|trc20, usdc:bep20|matic20 ONLY, busd:bep20, matic:matic20, bnb:bep20, eth:erc20|matic20, sol:spl); calls outside it throw — propose a supported pair instead. Pair with openfin-relay (bridge after onramp) and openfin-setup (API key).
---

# Fiat Onramp (Moonpay + Onramp.money)

> **Publisher.** Part of the OpenFinance skill bundle (openfin-setup, openfin-troubleshooting, openfin-hyperliquid, openfin-relay, openfin-onramp, openfin-polymarket, openfin-onchain) — all maintained by OpenFinance (https://openfinance.tech). Install as a set, not individually.

Two providers, one smart-router endpoint:

| Provider | Rails | Best for | `baseCurrency` |
|---|---|---|---|
| **Moonpay** | Cards, Apple Pay, Google Pay, SEPA, bank | Global / non-INR | `usd`, `eur`, `gbp`, … |
| **Onramp.money** | UPI, IMPS, bank | India / INR | `inr` (only) |

The agent never signs on-chain — the user opens the returned URL to
finish KYC + payment.

## Prerequisite

1. `openfin-setup` complete.
2. The destination chain's wallet is provisioned for the user (EVM
   default; Solana must be enabled if `chain=solana` /
   `currencyCode=*_sol`).

## Endpoints

### `POST /agent/onramp` — smart router (default)

`baseCurrency: "inr"` → Onramp.money. Anything else (or omitted →
defaults `usd`) → Moonpay. Body is the union of fields; the router
forwards only the relevant ones.

| Field | Notes |
|---|---|
| `baseCurrency` | **Routing key**, lowercased. Default `"usd"`. |
| `chain` | `ethereum` / `polygon` / `base` / `arbitrum` / `optimism` / `bsc` / `tron` / `solana`. (Onramp.money supports a subset — see matrix.) |
| `currency` | Crypto symbol (`usdc`, `usdt`, `eth`, `sol`, `btc`, …). |
| `amount` | Fiat amount the user will spend. |
| `walletAddress` | Optional; defaults to caller's wallet for the chain. |
| `redirectURL` | Provider redirects here on success. |

Response: `{ provider: "moonpay" | "onrampmoney", url: "https://…" }`.

Common Moonpay `currencyCode` derivations (when the smart router picks
Moonpay from `chain` + `currency`): `eth`/`usdc` on Ethereum →
`eth`/`usdc`; `usdc` on Polygon/Base/Arbitrum/Optimism → `usdc_polygon`
/ `usdc_base` / `usdc_arbitrum` / `usdc_optimism`; Solana `sol` →
`sol`, Solana `usdc` → `usdc_sol`. If unsure, the smart router accepts
`currencyCode` directly and forwards it.

The Moonpay-only / Onramp.money-only REST routes
(`POST /agent/onramp/moonpay`, `POST /agent/onramp/onrampmoney`) still
exist for dashboards and direct API consumers, but they are **not
exposed as MCP actions** — agents should always use the smart router so
`baseCurrency: "inr"` lands on Onramp.money correctly. Force-provider
fields below are documented for completeness (REST callers only).

### `POST /agent/onramp/onrampmoney` — REST-only (dashboards)

| Field | Notes |
|---|---|
| `chain` | `ethereum` / `polygon` / `bsc` / `tron` / `solana`. Mapped to legacy `network` code. |
| `network` | Legacy code (`erc20` / `matic20` / `bep20` / `trc20` / `spl`); overrides `chain` mapping. |
| `currency` / `coinCode` | Coin (`usdc`, `usdt`, `busd`, `matic`, `bnb`, `eth`, `sol`). |
| `amount` | INR (e.g. `1000` = ₹1000). |
| `coinAmount` | Crypto-side target — wins over `amount` if both sent. |
| `paymentMethod` | `1` = UPI/Instant (default in India), `2` = IMPS/Bank. Skip to let user choose. |
| `walletAddress`, `redirectURL`, `addressTag` | Optional. |

Chain → Onramp `network`: `ethereum→erc20`, `polygon→matic20`,
`bsc→bep20`, `tron→trc20`, `solana→spl`.

## Onramp.money supported (coin × network) matrix

Calls outside this matrix throw. Propose a supported pair or switch to
Moonpay.

| Coin | Networks |
|---|---|
| `usdt` | `bep20`, `matic20`, `erc20`, `trc20` |
| `usdc` | `bep20`, `matic20` (NOT `erc20` / `solana`) |
| `busd` | `bep20` |
| `matic` | `matic20` |
| `bnb` | `bep20` |
| `eth` | `erc20`, `matic20` |
| `sol` | `spl` |

Near-misses to remap on the fly:

- "USDC with INR on Ethereum" → propose Polygon (or Moonpay).
- "USDC with INR on Solana" → propose Polygon / BSC (or Moonpay).
- "ETH with INR on Arbitrum / Base / Optimism" → onramp on Eth/Polygon
  and bridge via `openfin-relay`, or use Moonpay.

## Wallet defaults

If `walletAddress` is omitted: EVM `chain` → caller's EVM address;
`chain=solana` or `currencyCode=*_sol` → caller's Solana address.
Missing wallet → request fails; send the user to openfinance.tech.

## Pair with other skills

- Onramp lands on chain X, user wants to trade on chain Y → bridge via
  `openfin-relay`.
- USDC on Arbitrum → Hyperliquid → use `GET /agent/trading/deposit-address`.
  Hyperliquid takes **only USDC** (not USDT, not USDC.e).
- **INR → Hyperliquid**: Onramp.money INR → USDC on Polygon or BSC →
  `openfin-relay` to Arbitrum → Hyperliquid deposit address.
- USDC on Polygon → Polymarket → swap to pUSD and route to the
  deposit wallet (`GET /agent/polymarket/deposit-wallet`).

## Examples

USD → USDC on Base (Moonpay):
```json
POST /agent/onramp
{ "chain": "base", "currency": "usdc", "amount": 100, "baseCurrency": "usd" }
→ { "provider": "moonpay", "url": "https://buy.moonpay.com/?…" }
```

INR → USDC on Polygon via UPI (Onramp.money):
```json
POST /agent/onramp
{ "baseCurrency": "inr", "chain": "polygon", "currency": "usdc",
  "amount": 5000, "paymentMethod": 1 }
→ { "provider": "onrampmoney", "url": "https://onramp.money/app/?…" }
```

## Don't

- Don't use Onramp.money for non-INR fiats — INR-only.
- Don't ignore the (coin × network) matrix — propose a supported pair
  instead of retrying.
- Don't ask for card / UPI details — the provider collects them in
  their own KYC UI.
- Don't poll for onramp status — the provider emits funds directly to
  the wallet. Verify on-chain via `openfin-onchain` (`/balances`).

## MCP

Single tool: `get_onramp_url` (smart router). Same body as
`POST /agent/onramp`; returns `{ provider, url, … }`. The
force-provider routes are REST-only — there is no
`get_moonpay_onramp_url` or `get_onrampmoney_onramp_url` MCP action,
so every onramp call goes through the smart router. INR triggers
("buy USDT with INR", "deposit ₹1000", "get USDC with UPI") route
to Onramp.money automatically.
