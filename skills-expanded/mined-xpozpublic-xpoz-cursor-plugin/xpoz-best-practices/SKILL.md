---
name: xpoz-best-practices
version: 2026-06-14
description: Reference guide for using Xpoz effectively. Load this skill whenever working with Xpoz MCP tools — it ensures correct query syntax, optimal field selection, proper pagination, and best practices for every Xpoz interaction. Covers authentication, query syntax (boolean operators, date filtering), response modes (fast/paging/CSV), field selection, tracking setup, and all platform tool references (Twitter, Instagram, Reddit, TikTok). Use for ANY Xpoz-related work, not just explicit best-practices questions.
allowed-tools: mcp(xpoz:*)
---

# Xpoz Best Practices

## Overview

Xpoz is a social media intelligence platform providing access to **Twitter/X**, **Instagram**, **Reddit**, and **TikTok** data through 48 MCP tools — no social media API keys required.

## When to Use

Load this skill for **any Xpoz interaction** — not just when the user explicitly asks about best practices. It provides the context needed to use Xpoz tools correctly:

- Calling any Xpoz MCP tool (query syntax, field selection, response modes)
- Setting up authentication or tracking
- Troubleshooting errors or empty results
- Choosing which tool to use for a specific task

## Quick Start

The Xpoz MCP server should already be configured by the plugin. If not, run `/xpoz-setup`.

See **[references/authentication.md](references/authentication.md)** for detailed auth flows and troubleshooting.

## Query Syntax

All keyword search tools support boolean query syntax:

| Operator | Example | Effect |
|----------|---------|--------|
| Exact phrase | `"machine learning"` | Matches exact phrase |
| OR | `"AI" OR "artificial intelligence"` | Matches either term |
| AND | `"Tesla" AND "earnings"` | Matches both terms |
| Grouping | `("deep learning" OR "neural network") AND python` | Combines operators |

**Date filtering:** Use `startDate` / `endDate` in YYYY-MM-DD format. Omit to use defaults (varies by tool).

**Content filtering** (Twitter only): Set `filterOutRetweets: true` to exclude retweets.

**Forbidden in query string:** `from:`, `to:`, `lang:`, `since:`, `until:`, `filter:` — use dedicated parameters instead.

## Platform Quick Reference

### Twitter/X (13 tools)
| Tool | Purpose |
|------|---------|
| `getTwitterUser` / `getTwitterUsers` | Look up 1-100 users by ID or username |
| `searchTwitterUsers` | Fuzzy search users by name |
| `getTwitterUserConnections` | Get followers or following |
| `getTwitterUsersByKeywords` | Find users who posted about a topic |
| `getTwitterPostsByIds` | Get 1-100 posts by ID |
| `getTwitterPostsByAuthor` | Get all posts from a username |
| `getTwitterPostsByKeywords` | Search posts by keywords |
| `getTwitterPostRetweets` | Get retweets of a post |
| `getTwitterPostQuotes` | Get quote tweets of a post |
| `getTwitterPostComments` | Get replies to a post |
| `getTwitterPostInteractingUsers` | Get commenters, quoters, or retweeters |
| `countTweets` | Count tweets matching a phrase |

See **[references/twitter.md](references/twitter.md)** for all parameters, fields, and examples.

### Instagram (9 tools)
| Tool | Purpose |
|------|---------|
| `getInstagramUser` | Look up user by ID or username |
| `searchInstagramUsers` | Fuzzy search users by name |
| `getInstagramUserConnections` | Get followers or following |
| `getInstagramUsersByKeywords` | Find users who posted about a topic |
| `getInstagramPostInteractingUsers` | Get commenters or likers of a post |
| `getInstagramPostsByIds` | Get posts by strong_id |
| `getInstagramPostsByUser` | Get posts from a user |
| `getInstagramPostsByKeywords` | Search posts by keywords in captions/subtitles |
| `getInstagramCommentsByPostId` | Get comments on a post |

See **[references/instagram.md](references/instagram.md)** for all parameters, fields, and examples.

### Reddit (9 tools)
| Tool | Purpose |
|------|---------|
| `getRedditUser` | Look up user by username |
| `searchRedditUsers` | Fuzzy search users by name |
| `getRedditUsersByKeywords` | Find users who posted about a topic |
| `getRedditPostsByKeywords` | Search posts by keywords |
| `getRedditPostWithCommentsById` | Get a post with all its comments |
| `getRedditCommentsByKeywords` | Search comments by keywords |
| `searchRedditSubreddits` | Search subreddits by name |
| `getRedditSubredditWithPostsByName` | Get subreddit details with posts |
| `getRedditSubredditsByKeywords` | Search subreddits by keyword in description |

See **[references/reddit.md](references/reddit.md)** for all parameters, fields, and examples.

### TikTok (9 tools)
| Tool | Purpose |
|------|---------|
| `getTiktokUser` | Look up user by ID or username |
| `searchTiktokUsers` | Fuzzy search users by name |
| `getTiktokUsersByKeywords` | Find users who posted about a topic |
| `getTiktokUsersByHashtags` | Find users who used specific hashtags |
| `getTiktokPostsByIds` | Get posts by ID |
| `getTiktokPostsByUser` | Get posts from a user |
| `getTiktokPostsByKeywords` | Search posts by keywords |
| `getTiktokPostsByHashtags` | Search posts by hashtags |
| `getTiktokCommentsByPostId` | Get comments on a post |

See **[references/tiktok.md](references/tiktok.md)** for all parameters, fields, and examples.

## Tracking

Setting up tracking is a best practice for getting more complete data from Xpoz. Tracked items are crawled regularly in the background, which means:

- **Better coverage** — continuous collection captures posts and activity that a single point-in-time query might miss
- **More complete data** — tracked items accumulate data over time, giving you a fuller picture than one-off queries

Track keywords, users, subreddits, and hashtags across all 4 platforms.

**Supported types per platform:**

| Platform | keyword | user | subreddit | hashtag |
|----------|---------|------|-----------|---------|
| Twitter | Yes | Yes | — | — |
| Instagram | Yes | Yes | — | — |
| Reddit | Yes | Yes | Yes | — |
| TikTok | Yes | Yes | — | Yes |

**View current tracking:**
```
Call getTrackedItems
```

**Add tracked items:**
```
Call addTrackedItems with items:
  [{ phrase: "AI agents", type: "keyword", platform: "twitter" }]
```

**Remove tracked items:**
```
Call removeTrackedItems with items:
  [{ phrase: "AI agents", type: "keyword", platform: "twitter" }]
```

See **[xpoz-social-tracking](../xpoz-social-tracking/SKILL.md)** for full tracking workflows and advanced patterns.

## Response Modes

All paginated tools support three response modes via `responseType`:

| Mode | Behavior | Best For |
|------|----------|----------|
| `"fast"` (default) | Returns up to 300 results immediately | Quick lookups, exploration |
| `"paging"` | Async — returns `operationId`, poll with `checkOperationStatus` | Large datasets, page-by-page |
| `"csv"` | Async CSV export to S3 — returns download URL | Bulk export, offline analysis |

See **[references/pagination-and-export.md](references/pagination-and-export.md)** for async polling patterns, pagination, and CSV export details.

## Field Selection

Pass `fields` to request only the data you need. This reduces response size and improves performance.

```
Call getTwitterPostsByKeywords with:
  query: "AI agents"
  fields: ["id", "text", "authorUsername", "likeCount"]
```

Each platform has different available fields — see the platform-specific references for complete field lists.

## Common Patterns

**Search → Analyze → Export:**
1. Search posts by keywords (fast mode) to preview results
2. Analyze engagement, sentiment, or themes
3. Export full dataset to CSV for deeper analysis

**Find Users → Get Their Posts → Analyze:**
1. Search users by keywords to find relevant accounts
2. Get posts by author for top accounts
3. Analyze content patterns, posting frequency, engagement

**Data Freshness:**
- Data is cached in Xpoz's database with automatic API fallback when stale — results are kept fresh automatically
- Use `forceLatest: true` to bypass cache and force a live fetch (increases latency and cost)

## Troubleshooting

| Problem | Solution |
|---------|----------|
| "Unauthorized" | Verify token — run `/xpoz-setup` |
| Empty results | Check query syntax, widen date range, try different keywords |
| Stale data | Use `forceLatest: true` to bypass cache |
| Operation timeout | Keep polling `checkOperationStatus` every ~5s until status is no longer `running` |

## Detailed Guides

For complete parameters, response fields, patterns, and examples:

- **[references/authentication.md](references/authentication.md)** — Auth flows for MCP and SDK
- **[references/pagination-and-export.md](references/pagination-and-export.md)** — Response modes, operationId polling, CSV export, field selection
- **[references/twitter.md](references/twitter.md)** — All 13 Twitter tools with parameters, fields, and examples
- **[references/instagram.md](references/instagram.md)** — All 9 Instagram tools with parameters, fields, and examples
- **[references/reddit.md](references/reddit.md)** — All 9 Reddit tools with parameters, fields, and examples
- **[references/tiktok.md](references/tiktok.md)** — All 9 TikTok tools with parameters, fields, and examples
- **[references/sdk.md](references/sdk.md)** — Python & TypeScript SDK reference

## Example Prompts

- "How do I search for tweets about AI?"
- "What fields are available for Instagram posts?"
- "How do I export Reddit data to CSV?"
- "Set up tracking for my brand across all platforms"
- "How do I paginate through large result sets?"
- "What's the difference between fast mode and paging mode?"
- "Show me all available TikTok tools"
