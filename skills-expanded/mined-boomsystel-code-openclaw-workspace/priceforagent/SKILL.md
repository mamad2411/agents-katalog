---
name: priceforagent
description: Get real-time prices for crypto, stocks, and commodities. Use when the user asks about asset prices, market data, or needs to check the value of Bitcoin, Ethereum, stocks like NVDA/AAPL, or commodities like gold/silver. Supports natural language queries ("What's the price of Bitcoin?") and direct lookups.
---

# Price for Agent

LLM-friendly price service for crypto, stocks, and commodities.

**Base URL:** `http://43.128.84.212:8080`

## Quick Start

### 1. Register for API Key

```bash
curl -X POST http://43.128.84.212:8080/v1/register \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "my-agent"}'
```

Response:
```json
{"api_key": "pfa_xxx...", "message": "API key generated successfully"}
```

### 2. Query Prices

**Natural language:**
```bash
curl -X POST http://43.128.84.212:8080/v1/query \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the price of Bitcoin and Ethereum?"}'
```

**Direct lookup:**
```bash
curl -H "X-API-Key: YOUR_KEY" http://43.128.84.212:8080/v1/price/bitcoin
```

**Batch:**
```bash
curl -X POST http://43.128.84.212:8080/v1/batch \
  -H "X-API-Key: YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pairs": ["BTC", "ETH", "NVDA"]}'
```

## Supported Assets

| Type | Examples |
|------|----------|
| Crypto | BTC, ETH, SOL, DOGE, XRP |
| Stocks | NVDA, AAPL, TSLA, GOOGL |
| Commodities | GOLD, SILVER, OIL |

## Rate Limits

- 2 requests per second per API key
- Usage tracked via `/v1/usage`

## Function Calling

```bash
curl http://43.128.84.212:8080/v1/function-schema
```

## OpenAPI Spec

```bash
curl http://43.128.84.212:8080/v1/openapi.yaml
```

## Response Format

```json
{
  "pair": "BTC",
  "price": 64770.50,
  "ask": 64835.27,
  "bid": 64705.73,
  "currency": "USDT",
  "market": "open",
  "timestamp": 1770353307
}
```
