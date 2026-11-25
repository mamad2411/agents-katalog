---
name: sedra-iv-api
description: "SEDRA IV API skill. Use when working with SEDRA IV for word, lexeme. Covers 2 endpoints."
version: 1.0.0
generator: lapsh
---

# SEDRA IV API
API version: 1.0.0

## Auth
No authentication required.

## Base URL
http://sedra.bethmardutho.org/api

## Setup
1. No auth setup needed
2. GET /word/{id} -- verify access

## Endpoints

2 endpoints across 2 groups. See references/api-spec.lap for full details.

### word
| Method | Path | Description |
|--------|------|-------------|
| GET | /word/{id} | Get Syriac word. |

### lexeme
| Method | Path | Description |
|--------|------|-------------|
| GET | /lexeme/{id} | Get Syriac lexeme. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "Get word details?" -> GET /word/{id}
- "Get lexeme details?" -> GET /lexeme/{id}

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
