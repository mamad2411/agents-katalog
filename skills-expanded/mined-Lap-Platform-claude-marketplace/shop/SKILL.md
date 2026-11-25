---
name: shop
description: "Shop API skill. Use when working with Shop for openai. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# Shop
API version: v1.1

## Auth
No authentication required.

## Base URL
https://server.shop.app

## Setup
1. No auth setup needed
2. GET /openai/search -- verify access

## Endpoints

2 endpoints across 1 groups. See references/api-spec.lap for full details.

### openai
| Method | Path | Description |
|--------|------|-------------|
| GET | /openai/search | Search for products |
| GET | /openai/details | Return more details about a list of products. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Search search?" -> GET /openai/search
- "List all details?" -> GET /openai/details

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
