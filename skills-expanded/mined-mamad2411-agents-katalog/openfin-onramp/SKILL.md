---
name: openfin-onramp
description: Fiat-to-crypto onramp via Moonpay, prefilled with the caller's wallet, chain, currency, and fiat amount. Use whenever the user says they want to buy crypto with a card / bank / Apple Pay / Google Pay, top up a wallet from fiat, fund a Hyperliquid / Polymarket / Solana wallet "with my card", or "I'm out of USDC, how do I get some". Triggers&#58; "buy USDC with my card", "credit card onramp", "Apple Pay USDC", "deposit fiat", "I have no crypto, how do I start", "fund my wallet with fiat", "buy ETH on Base with USD". Covers POST /agent/onramp/moonpay — returns a Moonpay simple-URL with chain / currencyCode / walletAddress / fiat amount baked in. The user opens the URL to complete KYC + payment in Moonpay's UI; once the buy clears, funds arrive in the user's OpenFinance-provisioned wallet on the chosen chain. No on-chain signing from the agent. Wallet defaults to the caller's OpenFinance-managed EVM address (or Solana address when chain=solana / currencyCode ends `_sol`). Pair with openfin-relay (bridge after onramp lands on a different chain than where you want to trade) and openfin-setup (API key check).
---

# Fiat Onramp (Moonpay)

The user can buy crypto with a card / bank / Apple Pay / Google Pay
through Moonpay. The OpenFinance backend builds a prefilled Moonpay buy
URL — the user opens it to complete KYC and payment. Funds land in the
user's OpenFinance-managed wallet for the chosen chain.

The agent never signs an on-chain tx for this. Onramp lives entirely in
Moonpay's flow.

## Prerequisite

1. User completed `openfin-setup` (API key in place — `open_…`).
2. User's wallet is provisioned for the destination chain (EVM is
   default; Solana wallet must be enabled if `chain=solana` /
   `currencyCode=*_sol`).

## Endpoint

### `POST /agent/onramp/moonpay`

Builds a (HMAC-signed if backend has the secret) Moonpay simple URL
with chain, currency, wallet address, and fiat amount baked in.

**Body**

| Field | Type | Notes |
|---|---|---|
| `chain` | string | One of `ethereum` / `polygon` / `base` / `arbitrum` / `optimism` / `bsc` / `solana`. Combined with `currency` to derive `currencyCode`. |
| `currency` | string | Crypto symbol (`usdc`, `eth`, `sol`, `btc`, …). Combined with `chain`. |
| `currencyCode` | string | Direct Moonpay code (e.g. `usdc_polygon`). **Overrides** `chain` + `currency` derivation. |
| `amount` | number | Fiat amount the user will spend |
| `baseCurrency` | string | ISO-4217 fiat code, lowercased. Defaults to `usd`. |
| `walletAddress` | string | Optional — defaults to the caller's wallet for the chain (EVM by default; Solana when `chain=solana` / `currencyCode` ends `_sol`) |
| `redirectURL`, `email`, `externalCustomerId`, `theme`, `colorCode` | string | Optional pass-through |

**Response**

```json
{ "url": "https://buy.moonpay.com/?...&signature=..." }
```

The agent should hand the URL back to the user (or open it in the
client). Once Moonpay clears the buy, funds arrive at `walletAddress`
on the chosen chain. There's nothing else for the agent to do — no
status polling.

## Wallet defaults

If `walletAddress` is omitted:

- `chain` is EVM (`ethereum`, `polygon`, `base`, `arbitrum`,
  `optimism`, `bsc`) → uses the caller's EVM address
- `chain=solana` or `currencyCode` ends in `_sol` → uses the caller's
  Solana address
- If the required wallet isn't provisioned, the request fails fast —
  surface the error and send the user back to openfinance.tech to
  enable that chain.

Use `GET /agent/wallets` (see `openfin-setup`) if the agent wants to
display the receiving address before opening the URL.

## Currency code rules of thumb

If the agent passes `chain` + `currency`, the backend derives
`currencyCode`. Common pairs Moonpay supports:

| chain | currency | derived `currencyCode` |
|---|---|---|
| `ethereum` | `eth` | `eth` |
| `ethereum` | `usdc` | `usdc` |
| `polygon` | `usdc` | `usdc_polygon` |
| `base` | `usdc` | `usdc_base` |
| `arbitrum` | `usdc` | `usdc_arbitrum` |
| `optimism` | `usdc` | `usdc_optimism` |
| `solana` | `sol` | `sol` |
| `solana` | `usdc` | `usdc_sol` |

If unsure, pass `currencyCode` directly with the exact Moonpay code.

## Pair with other skills

- After onramp lands on chain X but the user wants to trade on chain
  Y — use `openfin-relay` to bridge.
- After onramp lands as USDC on Arbitrum and user wants to trade on
  Hyperliquid — `GET /agent/trading/deposit-address`, send USDC there
  (no bridge needed).
- After onramp lands as USDC on Polygon and user wants to trade on
  Polymarket — confirm the token is **USDC.e** (not native USDC) before
  trading; otherwise use `openfin-relay` to swap on-Polygon.

## Example

User: "Buy $100 of USDC on Base with my card."

```http
POST /agent/onramp/moonpay
x-api-key: open_…
Content-Type: application/json

{
  "chain": "base",
  "currency": "usdc",
  "amount": 100,
  "baseCurrency": "usd"
}
```

Response:

```json
{ "url": "https://buy.moonpay.com/?currencyCode=usdc_base&walletAddress=0x…&baseCurrencyAmount=100&baseCurrencyCode=usd&signature=…" }
```

Agent surfaces the URL: "Open this Moonpay link to complete the
purchase: <url>. USDC will land at your Base wallet (0x…) once cleared."

## Don't

- Don't ask the user for credit-card details. Moonpay collects them in
  their own KYC-compliant UI; the OpenFinance backend never sees them.
- Don't treat the returned URL as authenticated to the user. It's
  prefilled but the actual KYC + payment happen on Moonpay.
- Don't poll the backend for onramp status. Moonpay handles the buy
  and emits funds to the wallet directly. To verify funds arrived,
  read on-chain via `openfin-onchain` (`/balances`) or the chain's
  block explorer.

## MCP note

`get_moonpay_onramp_url` — same body, returns `{ url }`.
