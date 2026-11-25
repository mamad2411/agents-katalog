---
name: automata-market-intelligence-api
description: "Automata Market Intelligence API skill. Use when working with Automata Market Intelligence for similar, search, contentpro-similar-text. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Automata Market Intelligence API
API version: 1.0.1

## Auth
ApiKey x-api-key in header

## Base URL
https://api.byautomata.io/

## Setup
1. Set your API key in the appropriate header
2. GET /similar -- verify access
3. POST /contentpro-similar-text -- create first contentpro-similar-text

## Endpoints

4 endpoints across 4 groups. See references/api-spec.lap for full details.

### similar
| Method | Path | Description |
|--------|------|-------------|
| GET | /similar | Send a company website to receive a list of companies related to them. |

### search
| Method | Path | Description |
|--------|------|-------------|
| GET | /search | Send search terms to receive the most relevant companies along with text snippets. |

### contentpro-similar-text
| Method | Path | Description |
|--------|------|-------------|
| POST | /contentpro-similar-text | The /contentpro-similar-text endpoint accepts and arbitrary piece of text and returns similar articles and blogs written by companies. |

### contentpro-search
| Method | Path | Description |
|--------|------|-------------|
| GET | /contentpro-search | Send search terms to receive the most relevant articles and companies. |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all similar?" -> GET /similar
- "List all search?" -> GET /search
- "Create a contentpro-similar-text?" -> POST /contentpro-similar-text
- "List all contentpro-search?" -> GET /contentpro-search
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params
- Create/update endpoints typically return the created/updated object

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
