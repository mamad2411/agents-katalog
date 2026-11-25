---
name: alphapipeline-signals
description: Pay-per-call x402 market data for crypto trading agents on Base mainnet - pre-trade honeypot/dump-risk screening, Hyperliquid HIP-4 prediction-market odds, oracle-manipulation-risk checks, funding rates, and CEX/DEX arbitrage signals. No signup, no API key, no OAuth - pay in USDC per call.
version: 1.0.0
author: parkyucheol-del
license: MIT
metadata:
  hermes:
    tags: [crypto, trading, x402, hyperliquid, defi, market-data, base]
    related_skills: []
---

# AlphaPipeline Signals

## When to Use

Reach for this skill whenever the task needs **live crypto/DeFi market data** that a
general web search or the model's own knowledge cannot give you a current, numeric
answer for - and the user (or your own trading logic) is willing to pay a few cents in
USDC per call to get it. Concretely:

- Before buying or swapping an unfamiliar token on an EVM chain: honeypot/tax/mint
  checks, LP lock/burn status, and a cheap pre-screen filter for scanning many
  candidates at once.
- Checking Hyperliquid's HIP-4 prediction markets (crypto price binaries, sports,
  Fed-rate-decision markets, etc.) for a live implied probability.
- Checking whether a Hyperliquid perpetual's mid price has detached from its
  oracle/mark price right now - the exact exposure that let an attacker net ~$1.28M
  from the Papertrade DEX on HyperEVM on 2026-10-10 by moving Hyperliquid's own mid
  price. Useful before trusting any HyperEVM protocol that prices off Hyperliquid mid.
- Perpetual futures funding rate / carry-trade APR, CEX-DEX or Korea-vs-global
  ("kimchi premium") spread checks, Polymarket neg-risk basket arbitrage, or token
  unlock/vesting dump-risk.
- Converting an arbitrary webpage into clean Markdown before feeding it to another
  step of your own reasoning.

Do **not** use this for general knowledge questions, for assets outside the
crypto/DeFi space, or when the user has not agreed to real USDC being spent per call -
every non-free endpoint below moves real money on Base mainnet.

## Quick Reference

Base URL: `https://alphapipeline-eu.onrender.com`. No account, API key, or OAuth -
every call either returns data directly (free endpoints) or a `402 Payment Required`
response whose headers describe exactly how to pay (see Procedure below).

**Free (no payment, use these first to verify connectivity):**

| Tool | Endpoint | What it returns |
|---|---|---|
| `market.kimchi_alert` | `GET /v1/market/kimchi-alert` | Upbit vs. global price premium, with reverse-premium/surge alerts |
| `unlocks.dump_risk` | `GET /v1/unlocks/dump-risk` | On-chain token unlock/vesting dump-risk proxy |
| `events.hip4_alerts` event-types | `GET /v1/prediction/hip4-alerts/event-types` | Webhook event catalog (disabled by default server-side) |

**Paid (USDC on Base, $0.005-$0.03 per call):**

| Tool | Endpoint | Price | What it returns |
|---|---|---|---|
| `tools.ai_markdown` | `GET /v1/tools/ai-markdown` | $0.005 | Ad-free Markdown from any URL |
| `security.token_prescreen` | `GET /v1/security/token-prescreen` | $0.01 | Cheap first-pass LP-lock + liquidity filter |
| `security.token_authenticity` | `GET /v1/security/token-authenticity` | $0.01 | Flags contracts impersonating a known asset (fake "USDC", etc.) |
| `derivatives.funding_rate` | `GET /v1/derivatives/funding-rate` | $0.01 | Bybit/Binance perpetual funding rate |
| `derivatives.funding_apr_matrix` | `GET /v1/derivatives/funding-apr-matrix` | $0.01 | Funding rate annualized into APR + carry-trade breakeven |
| `prediction.hip4_snapshot` | `GET /v1/prediction/hip4-snapshot` | $0.01 | Live Hyperliquid HIP-4 prediction-market odds |
| `prediction.hip4_price_ladder` | `GET /v1/prediction/hip4-price-ladder` | $0.01 | HIP-4 "above $X" strike ladder for one underlying |
| `market.cycle_compare` | `GET /v1/market/cycle-compare` | $0.01 | BTC/ETH price vs. the 2016/2020 halving cycles |
| `market.oracle_gap` | `GET /v1/market/oracle-gap` | $0.01 | Hyperliquid mid vs. oracle/mark gap (bp) for one perp - the Papertrade-exposure check |
| `calendar.macro_dday` | `GET /v1/calendar/macro-dday` | $0.01 | Countdown to the next FOMC/CPI/NFP |
| `security.token_risk` | `GET /v1/security/token-risk` | $0.02 | Honeypot/tax/mint contract audit |
| `security.contract_health_audit` | `GET /v1/security/contract-health-audit` | $0.02 | LP lock/burn audit |
| `dex.liquidity_slippage` | `GET /v1/dex/liquidity-slippage` | $0.02 | DEX pool liquidity + estimated slippage |
| `derivatives.whale_position_audit` | `GET /v1/derivatives/whale-position-audit` | $0.02 | Hyperliquid wallet position audit |
| `arb.spread_matrix` | `GET /v1/arb/spread-matrix` | $0.02 | CEX vs. DEX spread calculator |
| `prediction.exit_capacity_audit` | `GET /v1/prediction/exit-capacity-audit` | $0.02 | Polymarket order-book exit-capacity check |
| `security.token_diagnostic` | `GET /v1/security/token-diagnostic` | $0.03 | token_risk + contract_health_audit bundled |
| `prediction.neg_risk_arbitrage` | `GET /v1/prediction/neg-risk-arbitrage` | $0.03 | Polymarket neg-risk basket arbitrage detector |

Every priced response field is a raw number or a fixed-threshold boolean - there is no
qualitative "safe to buy" or composite risk-score field anywhere in this API. Decide
what to do with the numbers yourself.

## Procedure

**1. Connect.** AlphaPipeline is also a remote MCP server, so if your runtime
supports remote MCP tool discovery directly, add the connection config shipped
alongside this file (`mcp-config.json`) and skip to step 3 - `tools/list` works with
no payment. Otherwise call the plain REST endpoints below directly.

**2. Discover for free first.** Call `GET /v1/market/kimchi-alert` or
`GET /v1/unlocks/dump-risk` with no payment header to confirm the service is reachable
before spending anything.

**3. Call a priced endpoint and read the 402.** A request with no payment header gets
back `402 Payment Required`. This server speaks x402 v2: the response **body is an
empty `{}`** - the actual payment terms (accepted asset, exact USDC amount, Base
chain id `8453`, pay-to address) are base64-encoded JSON inside the `payment-required`
response *header*, not the body. Decode that header to get the terms.

```bash
curl -s "https://alphapipeline-eu.onrender.com/v1/derivatives/funding-rate?symbol=BTC"
# -> 402, empty {} body, payment terms in the payment-required response header
```

**4. Sign and retry with an x402 client.** You need an EVM-compatible wallet (a raw
private key via `EVM_PRIVATE_KEY`, or a seed phrase via `EVM_MNEMONIC`, standard HD
path `m/44'/60'/0'/0/0`) holding a small amount of USDC on Base mainnet. Using the
official `x402` Python SDK:

```python
import asyncio, os
from eth_account import Account
from x402 import x402Client
from x402.http.clients import x402HttpxClient
from x402.mechanisms.evm import EthAccountSigner
from x402.mechanisms.evm.exact.register import register_exact_evm_client

account = Account.from_key(os.environ["EVM_PRIVATE_KEY"])
client = x402Client()
register_exact_evm_client(client, EthAccountSigner(account))

async def call(path: str) -> str:
    async with x402HttpxClient(client, base_url="https://alphapipeline-eu.onrender.com") as http:
        resp = await http.get(path)
        await resp.aread()
        return resp.text  # 200 + JSON data; the SDK handled sign -> retry -> settle

print(asyncio.run(call("/v1/derivatives/funding-rate?symbol=BTC")))
```

The SDK signs an EIP-3009 `transferWithAuthorization` payment, retries the request
with it attached, and the server settles it through Coinbase's CDP Facilitator on
Base mainnet in the same round trip - no separate on-chain transaction to wait on.
Settlement is real USDC; there is no testnet/sandbox mode on the live server.

Any other x402-aware HTTP client works the same way; the Python SDK above is just the
one this project's own examples use.

## Pitfalls

- **The 402 body is empty.** Don't parse the response body for payment terms -
  decode the `payment-required` *header* instead. A client written for the older
  body-shaped x402 convention will silently get `{}` with no error.
- **Every call is real money.** There is no free trial beyond the two permanently-free
  onboarding endpoints (`market.kimchi_alert`, `unlocks.dump_risk`) and
  `tools/list`/`initialize` on the MCP path. Confirm the user actually wants to spend
  USDC before looping this skill over many candidates.
- **`elevated`/`flagged_as_counterfeit`/risk flags are fixed-threshold booleans, not
  verdicts.** Nothing in this API tells you whether it is safe to trade - it gives you
  the numbers (gap in basis points, tax %, LP-lock %, etc.) and leaves the decision to
  your own logic.
- **Hyperliquid-sourced endpoints never expose trade volume.** `market.oracle_gap`,
  `prediction.hip4_snapshot`, and `prediction.hip4_price_ladder` all note this - don't
  expect a volume field that isn't there.
- `security.token_prescreen` returns `liquidity_usd: null` for chains GeckoTerminal
  doesn't cover (currently Base, Ethereum, BSC, Polygon, Arbitrum, Optimism, Avalanche)
  - that's a coverage gap, not a liquidity signal.

## Verification

After connecting, confirm the skill actually works end to end:

1. `GET /v1/market/kimchi-alert` returns `200` with a `kimchi_premium_pct` field, with
   no payment required.
2. A priced endpoint called with no payment returns `402` with an empty `{}` body and
   a non-empty `payment-required` response header.
3. If you have a funded wallet configured, the same call retried through an x402
   client returns `200` with real data and a settlement confirmation from the SDK.
