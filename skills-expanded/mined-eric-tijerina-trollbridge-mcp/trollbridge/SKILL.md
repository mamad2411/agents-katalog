---
name: trollbridge
description: Pay-per-call intel for AI agents — live bounty boards, DeFi data, contract safety screens, prediction markets, token rug scans, gas prices, web search. $0.02-$0.05 USDC per call on Base or Solana via x402.
version: 1.0.0
tags:
  - bounties
  - defi
  - crypto
  - x402
  - web3
  - research
  - payments
metadata:
  openclaw:
    requires:
      bins:
        - curl
    homepage: https://github.com/eric-tijerina/trollbridge-mcp
    emoji: "🌉"
---

# TrollBridge

TrollBridge is a pay-per-call intel bridge for AI agents: 17 live data lanes
(bounty boards, DeFi, contract safety, prediction markets, token scans, gas,
search) at **$0.02-$0.05 USDC per call**, settled on Base or Solana through the
x402 protocol. Run by an agent operation; every toll goes to the keeper's
Coinbase. No account, no API key — you pay per call or you get nothing.

## When to use this skill

- Hunting bounties or paid work: which boards have fresh, open, paying tasks
- Due diligence: is this token/contract safe (rug scan, holder concentration,
  proxy and selfdestruct heuristics)
- Market intel: Polymarket odds, DeFi yields, new token listings, gas prices
- Fast facts: crypto spot prices, web search snippets, claim deadlines,
  sweepstakes, recently-paid bounties (verdicts)

## Fastest path: hosted MCP endpoint

Point any MCP client at the hosted Streamable HTTP server — 18 tools, no
install:

```
https://trollbridge-mcp-http.onrender.com
```

Or install the MCP server locally:

```bash
npx -y github:eric-tijerina/trollbridge-mcp
```

```json
{ "mcpServers": { "trollbridge": { "command": "npx", "args": ["-y", "github:eric-tijerina/trollbridge-mcp"] } } }
```

Tool names are `bridge_<lane>` (e.g. `bridge_bounties`, `bridge_token_check`,
`bridge_contract_check`, `bridge_markets`, `bridge_gas`). The server never pays
on your behalf: on HTTP 402 it returns the payment challenge (price, asset,
pay-to addresses for both rails) plus x402 v2 retry instructions.

## Direct HTTP (no MCP client needed)

Every lane is a plain GET:

```
GET https://mini-tollbooth.onrender.com/<lane>?<params>
```

Unpaid you get HTTP 402 with a payment challenge. Pay **$0.02 USDC** (most
lanes; `/enrich`, `/token-check`, `/markets`, `/search`, `/yields`,
`/new-pairs` are $0.05) on Base (eip155:8453) or Solana via x402 v2 — put the
signed payment in the `PAYMENT-SIGNATURE` header — then retry the same request.

| Lane | Params | What you get |
|---|---|---|
| `/bounties` | `limit` 1-200 | Every open bounty across all boards, one schema |
| `/fresh` | `limit` | Bounties posted in the last 24h |
| `/deadlines` | `limit` | Class-action / claim deadlines |
| `/sweepstakes` | `limit` | Free-to-enter sweepstakes, curated |
| `/verdicts` | `limit` | Recently-paid bounties (who actually paid) |
| `/opportunities` | `limit` | Every paying opportunity, normalized |
| `/models` | `limit` | 107-model AI catalog, per-token pricing, free flagged |
| `/prices` | — | Live BTC/ETH/SOL + USDC spot prices |
| `/enrich` | `address`, `network` | Wallet intel: type, balances, risk flags |
| `/token-check` | `mint`, `network` | Rug scan: liquidity, holders, 0-100 safety score |
| `/contract-check` | `address`, `chain` | Contract safety screen: verification, proxy wiring, selfdestruct/tx.origin/owner-mint heuristics, holder concentration |
| `/markets` | `q`, `limit` 1-25 | Live Polymarket odds, prices, volume |
| `/search` | `q` | Web search: title/URL/snippet JSON |
| `/yields` | `limit`, `stablecoinOnly` | Best DeFi yields right now |
| `/new-pairs` | `limit`, `chain` | Newest token listings with rug scores |
| `/gas` | — | Live gas prices per chain |
| `/defi` | `section`, `limit` 1-25 | DeFi movers, fees, revenue, stablecoins |

Free (no toll): `GET /tools` (third-party tool directory), `GET /traffic`
(honest bridge stats), `GET /health` (status, lane count).

## Honest notes

- The bridge runs on a free hosting tier and sleeps after ~15 minutes idle;
  the first call after sleep takes ~30 seconds to wake it. Retry once.
- Traffic is small and growing. `GET /traffic` reports exactly what the bridge
  has seen — lookers vs paid crossings, nothing inflated.
- Tolled lanes are pay-or-nothing: there is no free tier and no API key path.
- Contract/token screens are heuristic, not audits. Bounty data is aggregated
  from public boards; verify terms at the source before acting.
