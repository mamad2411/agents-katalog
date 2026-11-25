---
name: last30days-plugin
description: Requires python3, bash, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `last30days`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Research the last 30 days across Reddit, X, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, and grounded web search. Returns a ranked, clustered brief with citations. Use when the task needs recent social evidence, competitor comparisons, launch reactions, trend scans, or person/company profiles.
version: 1.0.4
license: MIT
requires:
  bins:
  - python3
  - bash
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      bins:
      - python3
      - bash
      env:
      - AISA_API_KEY
    optionalEnv:
    - LAST30DAYS_PLANNER_MODEL
    - LAST30DAYS_RERANK_MODEL
    - LAST30DAYS_FUN_MODEL
    - AISA_MODEL
    - AISA_BASE_URL
    - XIAOHONGSHU_API_BASE
    - LAST30DAYS_REASONING_PROVIDER
    - INCLUDE_SOURCES
    - LAST30DAYS_X_BACKEND
    - LAST30DAYS_YOUTUBE_TRANSCRIPTS
    - LAST30DAYS_REDDIT_COMMENTS
    - GH_TOKEN
    - GITHUB_TOKEN
    - LAST30DAYS_CONFIG_DIR
    - LAST30DAYS_DEBUG
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
    - https://www.reddit.com
    - https://hacker-news.firebaseio.com
    - https://api.github.com
    - https://www.xiaohongshu.com
primaryEnv: AISA_API_KEY
optionalEnv:
- LAST30DAYS_PLANNER_MODEL
- LAST30DAYS_RERANK_MODEL
- LAST30DAYS_FUN_MODEL
- AISA_MODEL
- AISA_BASE_URL
- XIAOHONGSHU_API_BASE
- LAST30DAYS_REASONING_PROVIDER
- INCLUDE_SOURCES
- LAST30DAYS_X_BACKEND
- LAST30DAYS_YOUTUBE_TRANSCRIPTS
- LAST30DAYS_REDDIT_COMMENTS
- GH_TOKEN
- GITHUB_TOKEN
- LAST30DAYS_CONFIG_DIR
- LAST30DAYS_DEBUG
networkTargets:
- https://api.aisa.one
- https://www.reddit.com
- https://hacker-news.firebaseio.com
- https://api.github.com
- https://www.xiaohongshu.com
---

# Last30days Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/last30days/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
