---
name: pirates-api
description: "Pirates API skill. Use when working with Pirates for pirate. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Pirates API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
https://api.fungenerators.com

## Setup
1. Set your API key in the appropriate header
2. GET /pirate/generate/name -- verify access

## Endpoints

4 endpoints across 1 groups. See references/api-spec.lap for full details.

### pirate
| Method | Path | Description |
|--------|------|-------------|
| GET | /pirate/generate/name | Generate random pirate names. |
| GET | /pirate/generate/insult | Generate random pirate insults. |
| GET | /pirate/generate/lorem-ipsum | Generate pirate lorem ipsum. |
| GET | /pirate/translate | Translate from English to pirate. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all name?" -> GET /pirate/generate/name
- "List all insult?" -> GET /pirate/generate/insult
- "List all lorem-ipsum?" -> GET /pirate/generate/lorem-ipsum
- "List all translate?" -> GET /pirate/translate
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
