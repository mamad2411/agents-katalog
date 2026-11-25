---
name: visibleai-audit
description: GEO audit API for AI agents. Check brand visibility across ChatGPT, Perplexity, Gemini. Pay $0.99 USDC via x402. No API keys needed.
version: 1.1.0
---

# VisibleAI Audit

Check how visible any brand is across AI search engines. Returns a GEO (Generative Engine Optimization) score with full optimization report.

## Quick Start

```bash
# Agent request → returns 402 with payment instructions
curl -X POST https://visibleai.space/api/v1/audit \
  -H "Content-Type: application/json" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'

# Pay 0.99 USDC on Base, then retry with tx hash
curl -X POST https://visibleai.space/api/v1/audit \
  -H "Content-Type: application/json" \
  -H "X-Payment-Tx: 0xYOUR_TX_HASH" \
  -d '{"brand": "BRAND_NAME", "industry": "INDUSTRY"}'
```

## Parameters

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| brand | string | Yes | Brand or company name |
| website | string | No | Website URL to analyze |
| industry | string | No | Industry or vertical (default: "general") |
| competitors | string[] | No | Up to 5 competitor names |

## Response

Full optimization report (JSON):
- `overall_score` (0-100) and letter `grade`
- Per-engine scores (Gemini, Perplexity, and more)
- Category breakdown (discovery, branded, comparison)
- Site analysis (schema markup, meta tags)
- Actionable `recommendations` — specific fixes to improve visibility

## Payment

- **Price:** $0.99 USDC per audit
- **Network:** Base (chain ID 8453)
- **Protocol:** x402
- **Wallet:** `0xB33FF8b810670dFe8117E5936a1d5581A05f350D`
- **No API keys required** — pay per query, no accounts

## Payment Flow

1. POST to `/api/v1/audit` → receive 402 with payment details
2. Send 0.99 USDC to wallet on Base
3. Retry same request with `X-Payment-Tx: <tx_hash>` header
4. Receive full audit response

## MCP Server

Also available as an MCP tool:

```json
{
  "visibleai": {
    "url": "https://visibleai.space/api/mcp"
  }
}
```

Tool: `visibleai_audit(brand, website?, industry?)`

## Links

- Website: https://visibleai.space
- API Docs: https://visibleai.space/api-docs
- MCP: https://visibleai.space/api/mcp
- ClawHub: visibleai-audit
