---
name: xquik-twitter-api
description: Search X/Twitter users, tweets, and trends with Xquik REST API endpoints.
tags: [api, social-media, twitter, x]
---

# Xquik Twitter API

Use this skill when a task needs X/Twitter search, user lookup, trend checks,
or lightweight social data collection through Xquik.

## Prerequisites

- Store the API key in `XQUIK_API_KEY`.
- Use `https://xquik.com/api/v1` as the REST API base URL.
- Use the `X-API-Key` header for authenticated REST requests.
- Check `https://docs.xquik.com` or `https://xquik.com/openapi.yaml` when the
  task needs a route not shown here.

## What Works

| Task | Route | Notes |
| --- | --- | --- |
| Confirm account access | `GET /account` | Fastest key smoke test |
| Search users | `GET /x/users/search` | Use a username or keyword query |
| Search tweets | `GET /x/tweets/search` | Use X search syntax in `q` |
| Get trends | `GET /x/trends` | Optional `woeid` and `count` query params |
| Use remote MCP | `https://xquik.com/mcp` | Add your API key in the client |

## Workflow

### 1. Confirm the API key

```bash
curl -sS -H "X-API-Key: ${XQUIK_API_KEY}" \
  "https://xquik.com/api/v1/account"
```

If this returns `401`, stop and ask for a valid Xquik API key. Do not continue
with unauthenticated probes.

### 2. Search for users

```bash
curl -sS -H "X-API-Key: ${XQUIK_API_KEY}" \
  "https://xquik.com/api/v1/x/users/search?q=xquik"
```

Use this before user-specific routes when you have a handle, display name, or
ambiguous account reference.

### 3. Search for tweets

```bash
curl -sS -H "X-API-Key: ${XQUIK_API_KEY}" \
  "https://xquik.com/api/v1/x/tweets/search?q=from:xquik&limit=5"
```

Use native X search syntax in `q`. Keep the first query narrow, inspect results,
then widen with keywords, dates, or account filters.

### 4. Check trends

```bash
curl -sS -H "X-API-Key: ${XQUIK_API_KEY}" \
  "https://xquik.com/api/v1/x/trends?woeid=1&count=10"
```

Use trends when the task asks for timely topics or a search seed list.

### 5. Persist findings

For follow-up work, store normalized records in memory:

```json
{
  "xquik": {
    "queries": [
      {
        "query": "from:xquik",
        "route": "/api/v1/x/tweets/search",
        "checked_at": "2026-06-13T00:00:00Z",
        "result_ids": ["1234567890123456789"]
      }
    ]
  }
}
```

Deduplicate by tweet ID, user ID, and query before taking follow-up actions.

## Pitfalls

- Do not guess unsupported routes. Check the OpenAPI document first.
- Do not paste API keys into prompts, issues, logs, or saved memory.
- Do not treat trend data as stable. Recheck before citing current topics.
- Do not create monitors unless the user asked for persistent tracking.
