---
name: scrapeio
description: Pull public social media data with the ScrapeIO API - profiles, posts, videos, comments, transcripts, search, trending content and ad libraries from TikTok, Instagram, YouTube, X (Twitter), Facebook, Reddit, LinkedIn and 25 more platforms. Use when the user asks for creator or account stats, post metrics, comments, transcripts, hashtag or keyword research, trends, influencer discovery, or competitor ads.
---

# ScrapeIO

ScrapeIO returns public social media data as the same JSON shape on every platform. Every call spends credits; cached and failed calls are free.

## Setup

The key is in the `SCRAPEIO_API_KEY` environment variable. If it is missing, ask the user to create a free key at https://scrapeio.com/login and set it. Never print the key.

## Two ways to call

1. **MCP tools** (preferred when the `scrapeio` MCP server is connected): call the platform tool directly, for example `tiktok_profile` with `{ "handle": "nike" }`. For anything without its own tool, use `list_endpoints` to find a path, then `call_endpoint`.
2. **HTTP**: fetch https://scrapeio.com/llms.txt for the endpoint list (or https://scrapeio.com/llms-full.txt for every parameter), then:

```bash
curl -s "https://scrapeio.com/v1/tiktok/profile?handle=nike" -H "x-api-key: $SCRAPEIO_API_KEY"
```

## Rules

- Choose the narrowest endpoint for the question. Prefer `handle` when the user gives a username.
- The answer is in `data`. Lists have `data.items`, `data.cursor` and `data.has_more`.
- Fetch more pages only when the user needs them; each page is a separate paid call.
- `credits_used` and `credits_remaining` come back on every response. Tell the user when credits run low.
- 403 means private and 404 means not found: report it, do not retry. 502 means every source is down: retry once after a few seconds. 402 means the account needs credits (https://scrapeio.com/pricing).

## Report

Lead with the numbers the user asked for. Name posts by caption or title and date, and link to them with the `url` field. Field names match across platforms, so one table can compare TikTok, Instagram and YouTube side by side.
