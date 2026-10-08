---
name: x-search-tool
description: >-
  X (Twitter) search tool. Performs keyword searches and retrieves tweets from specified users.
  Use when: Use when: you need to search topics on X, retrieve posts from specific accounts, or understand trends and public opinion.
tags: [search, x, twitter, external]
---


# X Search Tool

An external tool for searching X (Twitter) and retrieving tweets.

## How to Invoke

**Bash**: Run with `animaworks-tool x_search "検索クエリ" [オプション]` or `animaworks-tool x_search --user @username`

### search — Keyword Search
```bash
animaworks-tool x_search "検索クエリ" [-n 10] [--days 7]
```

### user_tweets — Retrieve User Tweets
```bash
animaworks-tool x_search --user @username [-n 10]
```

## Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| query | string | — | Search query |
| user | string | — | Username (with @) |
| count | integer | 10 | Number of results |
| days | integer | 7 | Number of days to search |

## CLI Usage

```bash
animaworks-tool x_search "検索クエリ" [-n 10] [--days 7]
animaworks-tool x_search --user @username [-n 10]
```

## Notes

- Requires X API (Bearer Token) configuration
- Search results are treated as external sources (untrusted)
