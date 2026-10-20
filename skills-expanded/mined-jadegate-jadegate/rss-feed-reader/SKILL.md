---
name: rss-feed-reader
description: Fetch and parse RSS/Atom feed with entry extraction
---

# RSS Feed Reader

Fetch and parse RSS/Atom feed with entry extraction

## When to Use

- User wants to read rss
- User wants to rss feed
- User wants to fetch feed
- Keywords: rss, feed, news, atom

## Required Parameters

- **feed_url** (string): RSS feed URL

## Output

- **title** (string): Feed title
- **entries** (array): Feed entries
- **count** (number): Number of entries

## Security

- Sandbox level: strict
- Max execution time: 30000ms
- Network whitelist: *
- JadeGate verified: Yes (5-layer security check passed)

## Execution Flow

Entry: `fetch` -> 5 steps -> Exit: `ret_ok`, `ret_fail`
