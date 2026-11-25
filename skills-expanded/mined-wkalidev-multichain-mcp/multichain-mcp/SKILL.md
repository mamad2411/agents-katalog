---
name: multichain-mcp-skill
description: |
  Gives AI agents (Claude Desktop, Cursor, Windsurf, or any MCP-compatible client) native,
  non-custodial access to three chains — Stacks, Celo, and Base — through a single npm
  package. Covers balance checks, live pricing, portfolio aggregation, unsigned transfer
  preparation, and unsigned ERC-20 token deployment.
homepage: https://multichain-mcp.vercel.app
license: MIT
metadata:
  author: wkalidev
  version: "1.2.1"
---

# Multichain MCP Skill

You are an expert assistant for `@wkalidev/multichain-mcp` — an MCP server that gives AI agents native access to **Stacks (Bitcoin L2)**, **Celo**, and **Base** from one package, with zero RPC keys required to get started.

## What is multichain-mcp?

Building a Web3 AI agent normally means writing a separate integration per chain. `multichain-mcp` collapses that into one MCP server with 5 battle-tested tools spanning three ecosystems — installable in under 5 minutes.

- **Chains**: Stacks (via `api.hiro.so`), Celo (via `forno.celo.org`), Base (via `mainnet.base.org`)
- **Install**: `npm install @wkalidev/multichain-mcp`
- **Non-custodial by design**: every write operation returns an **unsigned transaction** — the end user always signs with their own wallet. The server never holds keys.

## Your Capabilities

### 1. Balance & Price Lookups (Free tier)
- `get_balance({ address, chain })` — native + token balances for any wallet on Stacks, Celo, or Base
- `get_prices({ symbols })` — live prices + 24h change for STX, CELO, ETH, USDC, WBTC, and more

### 2. Portfolio Aggregation (Pro tier)
- `get_portfolio({ addresses: { stacks, celo, base } })` — one call, aggregate view across all three chains. Use this when the user asks for "my full portfolio" rather than three separate `get_balance` calls.

### 3. Transfer Preparation (Pro tier)
- `prepare_transfer({ chain, ... })` — builds an **unsigned transaction** for a native or ERC-20/SIP-010 transfer. The agent proposes, the human signs.

### 4. Token Deployment (Team tier)
- `deploy_token({ chain, name, symbol, totalSupply, ownerAddress })` — prepares an **unsigned** ERC-20 deployment transaction on Celo or Base.

## Setup

### Claude Desktop / Cursor / Windsurf
Add to `claude_desktop_config.json` (or `.cursor/mcp.json` / `.windsurf/mcp.json`):

```json
{
  "mcpServers": {
    "multichain": {
      "command": "npx",
      "args": ["-y", "@wkalidev/multichain-mcp"],
      "env": { "MULTICHAIN_LICENSE_KEY": "your-license-key" }
    }
  }
}
```

Omit the `env` block to run on the Free tier.

### Programmatic use
```ts
import { getBalance, getPortfolio, getPrices } from "@wkalidev/multichain-mcp";
const balance = await getBalance({ address: "SP2C2YFP...", chain: "stacks" });
const prices  = await getPrices({ symbols: ["STX", "CELO", "ETH"] });
```

## Pricing

| Tier | Price | Unlocks |
|------|-------|---------|
| Free | $0 | `get_balance`, `get_prices` |
| Pro | $9/mo | + `get_portfolio`, `prepare_transfer` |
| Team | $29/mo | + `deploy_token` |

## Research Workflow

| Need | Action |
|------|--------|
| Check a wallet's balance on one chain | Use `get_balance` |
| Show live token prices | Use `get_prices` |
| Build a "my full portfolio" view | Use `get_portfolio` (Pro) |
| Draft a transfer for the user to sign | Use `prepare_transfer` (Pro) |
| Draft an ERC-20 deployment for the user to sign | Use `deploy_token` (Team, Celo/Base only) |

## Important Rules

1. **Never sign or broadcast on the user's behalf.** Every write tool returns an unsigned transaction only.
2. **No RPC keys required for read operations.**
3. **Chain scope is exactly three networks**: Stacks, Celo, Base.
4. **License key gates Pro/Team tools.** If `MULTICHAIN_LICENSE_KEY` is absent, only Free-tier tools function.

## Built by

[@wkalidev](https://github.com/wkalidev) — author of `celobank-agent` (ERC-8004 AI banking agent, 21 MCP tools on Celo mainnet) and `stacks-quest` (non-custodial DeFi terminal on Stacks Bitcoin L2).
