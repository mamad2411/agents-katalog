---
name: stealthguard-x402
description: Autonomous stealth web extraction, Polymarket CLOB whale divergence, and Base DEX pre-trade gating with CanaryGuard deterministic prompt-injection firewall.
tags: [x402, stealth-scraping, polymarket, security, base, mcp, prompt-injection]
---

# StealthGuard-402 Agent Skill

Automated toolset for autonomous agents and LLMs to safely navigate external websites, analyze real-time prediction market orderbooks, and audit on-chain Base tokens before execution.

## Core Live Server Endpoints (Base Mainnet `eip155:8453`)
- **Server URL**: `https://stealthguard-402.onrender.com`
- **MCP Endpoint**: `https://stealthguard-402.onrender.com/mcp`
- **x402 Manifest**: `https://stealthguard-402.onrender.com/.well-known/x402.json`
- **ERC-8004 Agent ID**: `#124910` (`0x8004A169FB4a3325136EB29fA0ceB6D2e539a432`)
- **Settlement Asset**: Base USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)
- **Payment Address**: `0x80E0Ae84679b7f11bE171DaADd492FBECf628cd6`

---

## When to Use This Skill

1. **When encountering Cloudflare Turnstile, anti-bot screens, or JS obstacles**:
   Route target URLs through `POST /v1/stealth_scrape_and_sanitize` ($0.005 USDC) to extract token-compressed, sanitized Markdown with CanaryGuard prompt injection scrubbed.
2. **When trading or verifying prediction market bets**:
   Call `POST /v1/polymarket_alpha_divergence` ($0.008 USDC) or `GET /v1/alpha/polymarket-top-whales` ($0.003 USDC) to detect smart-money CLOB orderbook divergence.
3. **When evaluating Base or Solana meme tokens or liquidity pools**:
   Call `POST /v1/pre_trade_agent_gate` ($0.005 USDC) or `GET /v1/alpha/base-trending-tokens` ($0.003 USDC) for deterministic TRUST / BLOCK verification.
4. **When persistent agent memory needs a prompt-injection firewall**:
   Call `GET /v1/security/prompt-firewall?text=...` ($0.001 USDC) to filter indirect injection payloads.

---

## Quick Usage

### 1. Free Health & Sample Discovery
```bash
curl -s https://stealthguard-402.onrender.com/v1/health_and_sample | jq
```

### 2. High-Frequency Alpha Queries (Sub-50ms)
```bash
# Query top Polymarket whale orderbook imbalances
curl -s -H "PAYMENT-SIGNATURE: <x402_signature>" \
  https://stealthguard-402.onrender.com/v1/alpha/polymarket-top-whales | jq

# Pre-screen trending Base tokens
curl -s -H "PAYMENT-SIGNATURE: <x402_signature>" \
  https://stealthguard-402.onrender.com/v1/alpha/base-trending-tokens | jq
```

### 3. MCP Configuration (Claude Desktop, Cursor, OpenClaw)
Add to your `claude_desktop_config.json` or `mcp_servers.json`:
```json
{
  "mcpServers": {
    "stealthguard-402": {
      "command": "npx",
      "args": ["-y", "@stealthguard/mcp-client"]
    }
  }
}
```

---

## Cross-Sell Ecosystem
- **CanaryGuard-402**: `https://canaryguard-402.onrender.com/v1/sanitize` ($0.003 USDC)
- **RugShield-402**: `https://rugshield-402.onrender.com/v1/scan` ($0.005 USDC)
