---
name: random-lovecraft
description: "Random Lovecraft API skill. Use when working with Random Lovecraft for sentences, books. Covers 4 endpoints."
version: 1.0.0
generator: lapsh
---

# Random Lovecraft
API version: 1.0

## Auth
No authentication required.

## Base URL
https://randomlovecraft.com/api

## Setup
1. No auth setup needed
2. GET /sentences -- verify access

## Endpoints

4 endpoints across 2 groups. See references/api-spec.lap for full details.

### sentences
| Method | Path | Description |
|--------|------|-------------|
| GET | /sentences | A random sentence |
| GET | /sentences/{id} | A specific sentence |

### books
| Method | Path | Description |
|--------|------|-------------|
| GET | /books/{id}/sentences | Random sentences from a specific book |
| GET | /books | List all books |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all sentences?" -> GET /sentences
- "Get sentence details?" -> GET /sentences/{id}
- "List all sentences?" -> GET /books/{id}/sentences
- "List all books?" -> GET /books

## Response Tips
- Check response schemas in references/api-spec.lap for field details

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
