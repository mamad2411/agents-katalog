---
name: axesso-api
description: "Axesso API skill. Use when working with Axesso for amz. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Axesso Api
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://api.axesso.de

## Setup
1. No auth setup needed
2. GET /amz/amazon-lookup-product -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### amz
| Method | Path | Description |
|--------|------|-------------|
| GET | /amz/amazon-lookup-product | lookup product information |
| GET | /amz/amazon-lookup-buy-recommendations | request buy recommendations to a given product |
| GET | /amz/amazon-search-by-keyword | fetch results auf a keyword search on Amazon |
| GET | /amz/sort-options | request available sort options to use in keyword search |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all amazon-lookup-product?" -> GET /amz/amazon-lookup-product
- "List all amazon-lookup-buy-recommendations?" -> GET /amz/amazon-lookup-buy-recommendations
- "List all amazon-search-by-keyword?" -> GET /amz/amazon-search-by-keyword
- "List all sort-options?" -> GET /amz/sort-options

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
