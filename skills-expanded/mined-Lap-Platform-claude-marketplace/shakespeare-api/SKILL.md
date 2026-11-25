---
name: shakespeare-api
description: "Shakespeare API skill. Use when working with Shakespeare for shakespeare. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Shakespeare API
API version: 1.5

## Auth
ApiKey X-Fungenerators-Api-Secret in header

## Base URL
http://api.fungenerators.com

## Setup
1. Set your API key in the appropriate header
2. GET /shakespeare/generate/name -- verify access

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### shakespeare
| Method | Path | Description |
|--------|------|-------------|
| GET | /shakespeare/generate/name | Generate random Shakespearen names. |
| GET | /shakespeare/generate/insult | Generate random Shakespeare style insults. |
| GET | /shakespeare/generate/lorem-ipsum | Generate Shakespeare lorem ipsum. |
| GET | /shakespeare/translate | Translate from English to Shakespeare English. |
| GET | /shakespeare/quote | Get a random Shakespeare quote. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all name?" -> GET /shakespeare/generate/name
- "List all insult?" -> GET /shakespeare/generate/insult
- "List all lorem-ipsum?" -> GET /shakespeare/generate/lorem-ipsum
- "List all translate?" -> GET /shakespeare/translate
- "List all quote?" -> GET /shakespeare/quote
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
