---
name: endpoints
description: "Endpoints API skill. Use when working with Endpoints for tokens, trader-grades, investor-grades. Covers 14 endpoints."
version: 1.0.0
generator: lapsh
---

# Endpoints

## Auth
ApiKey key in header

## Base URL
https://api.tokenmetrics.com

## Setup
1. Set your API key in the appropriate header
2. GET /v1/tokens -- verify access

## Endpoints

14 endpoints across 14 groups. See references/api-spec.lap for full details.

### tokens
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/tokens | Tokens |

### trader-grades
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/trader-grades | Trader Grades |

### investor-grades
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/investor-grades | Investor Grades |

### market-indicator
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/market-indicator | Market Indicator |

### trading-indicator
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/trading-indicator | Trading Indicator |

### resistance-support
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/resistance-support | Resistance & Support |

### price
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/price | Price |

### price-prediction
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/price-prediction | Price Prediction |

### sentiments
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/sentiments | Sentiments |

### quantmetrics-tier-1
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/quantmetrics-tier-1 | Quantmetrics Tier 1 |

### quantmetrics-tier-2
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/quantmetrics-tier-2 | Quantmetrics Tier 2 |

### scenario-analysis
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/scenario-analysis | Scenario Analysis |

### correlation
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/correlation | Correlation |

### indices
| Method | Path | Description |
|--------|------|-------------|
| GET | /v1/indices | Indices |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all tokens?" -> GET /v1/tokens
- "List all trader-grades?" -> GET /v1/trader-grades
- "List all investor-grades?" -> GET /v1/investor-grades
- "List all market-indicator?" -> GET /v1/market-indicator
- "List all trading-indicator?" -> GET /v1/trading-indicator
- "List all resistance-support?" -> GET /v1/resistance-support
- "List all price?" -> GET /v1/price
- "List all price-prediction?" -> GET /v1/price-prediction
- "List all sentiments?" -> GET /v1/sentiments
- "List all quantmetrics-tier-1?" -> GET /v1/quantmetrics-tier-1
- "List all quantmetrics-tier-2?" -> GET /v1/quantmetrics-tier-2
- "List all scenario-analysis?" -> GET /v1/scenario-analysis
- "List all correlation?" -> GET /v1/correlation
- "List all indices?" -> GET /v1/indices
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
