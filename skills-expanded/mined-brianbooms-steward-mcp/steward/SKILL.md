---
name: steward
description: "Pay-per-call data and commerce tools for AI agents, settled in USDC on Base via raw x402 v1. No accounts, no API keys."
metadata:
  maintainer: brianbooms
  npm: "@brianbooms/steward-mcp"
  license: MIT
  version: 0.3.1
---

# Steward

Steward is a pay-per-call toolkit for AI agents: 92 paid HTTP endpoints plus an
MCP server, all settled in **USDC on Base (eip155:8453)** with the raw
**x402 v1** protocol. There are no accounts, no API keys, and no subscriptions —
you pay per call with crypto.

- Paid HTTP APIs: `https://pay.brianbooms.com`
- Machine-readable route list: `https://pay.brianbooms.com/.well-known/x402`
- A2A agent card: `https://pay.brianbooms.com/.well-known/agent-card.json`
- MCP server: `@brianbooms/steward-mcp` on npm (MIT), this repo
- Built by AI-assisted artist and content creator Brian Booms (brianbooms.com)

## How an agent pays (x402 v1 flow)

1. **Discover** routes and prices from the machine-readable list at
   `https://pay.brianbooms.com/.well-known/x402` (92 routes, $0.005–$0.99 per
   call; penny routes like jokes and fortunes are $0.01).
2. **Request** the endpoint (GET/POST). If payment is required the server
   answers **HTTP 402** with the exact payment terms (amount in USDC atomic
   units, destination, facilitator).
3. **Sign** an EIP-3009 `transferWithAuthorization` paying that amount of USDC
   on Base. The facilitator is `https://facilitator.xpay.sh` (zero-fee);
   settlement pays `0xa98e8c6cbc64b7bb30fd0d2015ab24814c661839`.
4. **Retry** the same request with the signed payload in the `X-PAYMENT`
   header. The server verifies via the facilitator and returns the response.

Any buyer library that speaks raw x402 v1 (official x402 client, Coinbase CDP
buyer, ag402, Circle CLI) can pay Steward today — no integration work needed.

## Endpoint families (92 routes)

- **Data** (`/api/v1/data/...`): weather, joke, fortune, fx, time,
  timezone-convert, wiki, iss-pass, astronomy, holidays, country, dns, crypto,
  stock, gas-price, geocode, ip, unit-convert, date-calc, text-stats,
  readability, summarize, feed, sleep-tip, sleep-plan, lyric-quote,
  daily-briefing, catalog-search, id-generate, preflight, cert, httpcheck
- **Commerce** (`/api/v1/catalog/...`, `/api/v1/buy/...`, `/api/v1/license/...`,
  `/api/v1/rewards/...`): catalog query, product SKUs, license quotes, rewards
  lookup, merch kit, press kit
- **Sleep** (`/api/v1/sleep/...`): recommendations, queue
- **Playlist/audio** (`/api/v1/playlist/build`, `/api/v1/audio/...`):
  playlist builder, audio match, audio rest, audio focus
- **Ascendency** (`/api/v1/ascendency/...`): status, leaders

## MCP tools (24, this repo)

`steward_weather`, `steward_joke`, `steward_fortune`, `steward_fx`,
`steward_time`, `steward_wiki`, `steward_iss_pass`, `steward_audio_match`,
`steward_audio_rest`, `steward_audio_focus`, `steward_sleep_tip`,
`steward_receipts`, `steward_catalog`, `steward_product`,
`steward_purchase_instructions`, `steward_rewards`, `steward_payment_format`,
`steward_cheapest_route`, `steward_route_fees`, `trust_verify_status`,
`trust_agent_attestation`, `trust_screen`, `steward_verifier_pubkey`,
`steward_directory`

Install: `npm install @brianbooms/steward-mcp`, or add to your MCP client config
pointing at this package. See README.md for setup and TEST-REPORT-2026-10-05.md
for the latest test evidence.
