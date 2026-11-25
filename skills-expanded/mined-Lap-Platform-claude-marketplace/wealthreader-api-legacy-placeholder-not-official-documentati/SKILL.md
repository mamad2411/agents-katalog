---
name: wealthreader-api-legacy-placeholder-not-official-documentation
description: "Wealthreader API — Legacy Placeholder (Not Official Documentation) API skill. Use when working with Wealthreader API — Legacy Placeholder (Not Official Documentation) for root, docs. Covers 3 endpoints."
version: 1.0.0
generator: lapsh
---

# Wealthreader API — Legacy Placeholder (Not Official Documentation)
API version: 1.0.0

## Auth
No authentication required.

## Base URL
https://virtserver.swaggerhub.com/Wealth-Reader/api/1.0.0

## Setup
1. No auth setup needed
2. GET / -- verify access

## Endpoints

3 endpoints across 2 groups. See references/api-spec.lap for full details.

### root
| Method | Path | Description |
|--------|------|-------------|
| GET | / | Landing (not official docs) |

### docs
| Method | Path | Description |
|--------|------|-------------|
| GET | /docs | List supported language branches |
| GET | /docs/{lang} | Documentation notice by language (legacy placeholder) |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all docs?" -> GET /docs
- "Get doc details?" -> GET /docs/{lang}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
