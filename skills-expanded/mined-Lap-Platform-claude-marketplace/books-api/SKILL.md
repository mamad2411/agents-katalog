---
name: books-api
description: "Books API skill. Use when working with Books for lists, lists.{format}, reviews.{format}. Covers 6 endpoints."
version: 1.0.0
generator: lapsh
---

# Books API
API version: 3.0.0

## Auth
ApiKey api-key in query

## Base URL
https://api.nytimes.com/svc/books/v3

## Setup
1. Set your API key in the appropriate header
2. GET /lists/best-sellers/history.json -- verify access

## Endpoints

6 endpoints across 3 groups. See references/api-spec.lap for full details.

### lists
| Method | Path | Description |
|--------|------|-------------|
| GET | /lists/best-sellers/history.json | Best Seller History List |
| GET | /lists/{date}/{list}.json | Best Seller List by Date |
| GET | /lists/overview.{format} | Best Seller List Overview |
| GET | /lists/names.{format} | Best Seller List Names |

### lists.{format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /lists.{format} | Best Seller List |

### reviews.{format}
| Method | Path | Description |
|--------|------|-------------|
| GET | /reviews.{format} | Reviews |

## Common Questions

Match user requests to endpoints in references/api-spec.lap. Key patterns:
- "List all history.json?" -> GET /lists/best-sellers/history.json
- "Get lists.{format} details?" -> GET /lists.{format}
- "Get list details?" -> GET /lists/{date}/{list}.json
- "Get overview.{format} details?" -> GET /lists/overview.{format}
- "Get names.{format} details?" -> GET /lists/names.{format}
- "Get reviews.{format} details?" -> GET /reviews.{format}
- "How to authenticate?" -> See Auth section

## Response Tips
- Check response schemas in references/api-spec.lap for field details
- List endpoints may support pagination; check for limit, offset, or cursor params

## References
- Full spec: See references/api-spec.lap for complete endpoint details, parameter tables, and response schemas

> Generated from the official API spec by [LAP](https://lap.sh)
