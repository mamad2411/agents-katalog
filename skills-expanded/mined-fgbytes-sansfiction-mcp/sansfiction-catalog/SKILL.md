---
name: sansfiction-catalog
description: Search the SansFiction book catalog and manage a personal reading library (books, collections, reading progress, ratings, stats) over a token-authenticated REST API. Use when a user wants to find books, look up book/series/collection metadata, or read and update their SansFiction library.
license: proprietary
---

<!--
  Canonical copy of this skill is served at:
    https://sansfiction.com/.well-known/agent-skills/sansfiction-catalog/SKILL.md
  Source of truth: web/fgbook/lib/agents/discovery.ts (SANSFICTION_CATALOG_SKILL).
  Keep this file in sync when editing that constant.
-->

# SansFiction

SansFiction is a digital library for books, collections, reading journals, and
discovery. This skill drives its public REST API (`/api/v1`). An MCP server
exposing the same capabilities is also available at `/api/mcp` for MCP-native
clients — both accept the same bearer token.

Base URL: `https://sansfiction.com`

## Authentication

Public catalog endpoints need no auth. Personal library endpoints require a
bearer token:

```http
Authorization: Bearer sf_mcp_xxxxxxxxxxxxxxxxxxxxxxxx
```

A signed-in user generates a token at `https://sansfiction.com/docs/agents`.
Never ask the user for a password — only a token. On `401`, ask for a fresh one.

## Public catalog (no auth)

- `GET /api/v1/catalog/search?q={query}&limit=20&searchType=all|author|series|mood|isbn`
- `GET /api/v1/catalog/books/{bookId}`
- `GET /api/v1/catalog/series/{seriesId}`
- `GET /api/v1/catalog/collections?limit=20`

```bash
curl "https://sansfiction.com/api/v1/catalog/search?q=dune&limit=5"
```

## Personal library (bearer token required)

- `GET    /api/v1/library/books?status=reading|want|read|dnf|all&limit=20`
- `POST   /api/v1/library/books` — body `{ "book_id", "status?", "edition_id?" }`
- `PATCH  /api/v1/library/books/{bookId}` — body `{ "status?","rating?","review?","started_at?","finished_at?","current_page?" }`
- `DELETE /api/v1/library/books/{bookId}`
- `GET    /api/v1/library/search?q={query}&status=all&limit=10`
- `GET    /api/v1/library/collections?limit=20&query=`
- `GET    /api/v1/library/collections/{collectionId}?limit=&offset=&rank=true`
- `POST   /api/v1/library/collections/{collectionId}/items` — body `{ "book_id","note?","edition_id?" }`
- `GET    /api/v1/library/stats?scope=weekly|monthly|yearly&include_logs=false`

```bash
curl -H "Authorization: Bearer $SF_TOKEN" \
  "https://sansfiction.com/api/v1/library/books?status=reading"
```

## Conventions

- Responses are JSON. Errors look like `{ "error": string, "code"?: string }`.
- `book_id` is the catalog UUID returned by any catalog search/detail response.
- Rate limits: 60 req/min anonymous, 180 req/min with a token. Honor
  `Retry-After` on `429`; check `X-RateLimit-Remaining` / `X-RateLimit-Reset`.

## Typical workflow

1. Find a book: `GET /api/v1/catalog/search` → take `book.id`.
2. Add it: `POST /api/v1/library/books { "book_id": "…", "status": "want" }`.
3. Track progress: `PATCH /api/v1/library/books/{id} { "current_page": 120 }`.
4. Finish: `PATCH /api/v1/library/books/{id} { "status": "read", "rating": 5, "review": "…" }`.

## Alternative transport: MCP

MCP-native clients can connect to `https://sansfiction.com/api/mcp`
(streamable HTTP) with the same bearer token; its tools mirror these endpoints.
