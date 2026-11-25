---
name: article-rewriter-and-article-extractor-api
description: "Article Rewriter and Article Extractor API skill. Use when working with Article Rewriter and Article Extractor for api. Covers 5 endpoints."
version: 1.0.0
generator: lapsh
---

# Article Rewriter and Article Extractor API
API version: 1.0

## Auth
ApiKey key in query

## Base URL
https://api.spinbot.net/

## Setup
1. Set your API key in the appropriate header
2. GET /api/acc -- verify access
3. POST /api/pretty-spinner -- create first pretty-spinner

## Endpoints

5 endpoints across 1 groups. See references/api-spec.lap for full details.

### api
| Method | Path | Description |
|--------|------|-------------|
| GET | /api/acc | Return the user credit information. |
| POST | /api/pretty-spinner | Human readable auto rewrite your article. |
| POST | /api/spinner | Rewriting (spinning) your input article. |
| POST | /api/spintax | Generate Spintax format for the input article |
| POST | /api/article | Extracting the main article of the given URL. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all acc?" -> GET /api/acc
- "Create a pretty-spinner?" -> POST /api/pretty-spinner
- "Create a spinner?" -> POST /api/spinner
- "Create a spintax?" -> POST /api/spintax
- "Create a article?" -> POST /api/article
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
