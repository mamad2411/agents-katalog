---
name: marketer-sync
description: >
  Sync all live data locally for fast reads — strategies, links, pages, metrics,
  schedules, analytics. Triggers: sync, refresh, pull data, check metrics, what is live.
---

# Marketer Sync Skill

## Overview

Pulls all live data from the server MCP into a local reference file at `.10x/sync-data.json`. After syncing, any question about strategies, links, pages, metrics, or schedules can be answered by reading the local file — **zero API calls needed**.

This is the **first command a user should run** in every session. It minimizes API calls to the server by caching everything locally.

## When To Use

- User asks "what strategies are live?"
- User asks "show me my metrics"
- User asks "sync my data" or runs `/sync`
- User asks "what is the status of my campaigns?"
- Before showing the dashboard
- Any time the user wants fresh data locally
- **At the start of every session** — run sync first

## Prerequisites

- `.env` file configured (run `/setup` if not done)
- Required env vars: `LINK_PLATFORM_HANDLE`, `USER_PAT`
- MCP connection to server must be active

## How It Works

### Step 1: Hit All MCP Endpoints

Call these Link Platform MCP tools to gather all data:

```
Data Sources (via Link Platform MCP tools):
----------------------------------------------
1. system_health            → server status
2. agent_list_proposals     → all strategies (draft, live, discarded, archived)
3. analytics_get            → performance analytics and insights
4. links_list               → all links for the handle
5. links_list               → all pages (draft + published)
6. webhooks_list            → scheduled tasks
```

### Step 2: Combine Into Reference File

Write everything to `.10x/sync-data.json`:

```json
{
  "synced_at": "2026-02-17T10:30:00.000Z",
  "handle": "myhandle",
  "mcp_url": "https://myhandle.mcp.10x.in",

  "server_health": {
    "status": "ok"
  },

  "strategies": {
    "total": 12,
    "live": 5,
    "drafts": 3,
    "discarded": 2,
    "archived": 2,
    "items": [
      {
        "strategyId": "str_1708...",
        "name": "Summer Flash Sale",
        "status": "live",
        "slug": "summer-sale",
        "liveUrl": "https://myhandle.10x.in/summer-sale",
        "createdAt": "2026-01-15T...",
        "publishedAt": "2026-01-20T...",
        "performance": {
          "clicks": 1240,
          "conversions": 89,
          "conversionRate": 0.072
        }
      }
    ],
    "topPerformers": [],
    "insights": {}
  },

  "links": {
    "total": 24,
    "note": "links_upsert creates REDIRECT links only (302 redirects for campaign tracking). Page hosting uses site-deployments API.",
    "items": []
  },

  "pages": {
    "total": 8,
    "published": 5,
    "draft": 3,
    "note": "Pages are deployed via POST /v2/handles/{handle}/site-deployments (JWT auth), NOT via links_upsert.",
    "items": []
  },

  "analytics": {
    "summary": {}
  },

  "schedules": {
    "total": 0,
    "items": []
  }
}
```

### Step 3: Print Summary

```
Sync Complete

  Handle:      myhandle.10x.in
  Server:      https://myhandle.mcp.10x.in (healthy)
  Last sync:   2026-02-17 10:30:00 UTC

  Strategies:  5 live / 3 drafts / 2 discarded / 2 archived
  Links:       24 total
  Pages:       8 total (5 published, 3 draft)
  Schedules:   0 active

  Top Performer: "Summer Flash Sale" — 7.2% conversion rate

  Data saved to .10x/sync-data.json
  All future queries will read from local cache.
  Run /sync again to refresh.
```

## After Sync — How the Local Assistant Uses It

**CRITICAL**: After sync, the local assistant MUST read `.10x/sync-data.json` before making any API calls. This file is the **source of truth** for:

- Strategy statuses, names, performance
- Link inventory
- Page inventory (published vs draft)
- Analytics and campaign data
- Scheduled tasks

### Reading Patterns

| User Question | Read From |
|---|---|
| "What strategies are live?" | `data.strategies.items.filter(s => s.status === 'live')` |
| "Show me my metrics" | `data.strategies.items[].performance` + `data.analytics` |
| "What's my best strategy?" | `data.strategies.topPerformers[0]` |
| "Show my drafts" | `data.strategies.items.filter(s => s.status === 'draft')` |
| "What pages are published?" | `data.pages.items.filter(p => p.status === 'PUBLISHED')` |
| "How many conversions this week?" | `data.analytics.summary` |
| "Any scheduled tasks?" | `data.schedules.items` |

### When To Re-Sync vs Use Cache

- **Use cache**: Answering questions, showing status, referencing past data
- **Re-sync**: After deploying via site-deployments API, after discarding, after creating new redirect links, or if user says "refresh"
- **Always sync**: At start of session, before dashboard, before any analysis
