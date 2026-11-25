---
name: last30days-zh-plugin
description: 'Requires python3, bash, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `last30days-zh`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. 聚合最近 30 天的 Reddit、X/Twitter、YouTube、TikTok、Instagram、Hacker News、Polymarket 和 web search 结果. Use when: the user needs recent multi-source research across the last 30 days.'
version: 1.0.9
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
    - LAST30DAYS_RERANK_MODEL
    - AISA_MODEL
    - LAST30DAYS_PLANNER_MODEL
    - AISA_BASE_URL
    - XIAOHONGSHU_API_BASE
    - LAST30DAYS_REASONING_PROVIDER
    - INCLUDE_SOURCES
    - LAST30DAYS_X_BACKEND
    - LAST30DAYS_YOUTUBE_TRANSCRIPTS
    - LAST30DAYS_REDDIT_COMMENTS
    - LAST30DAYS_CONFIG_DIR
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
    - https://www.reddit.com
    - https://hacker-news.firebaseio.com
    - https://www.xiaohongshu.com
primaryEnv: AISA_API_KEY
optionalEnv:
- LAST30DAYS_RERANK_MODEL
- AISA_MODEL
- LAST30DAYS_PLANNER_MODEL
- AISA_BASE_URL
- XIAOHONGSHU_API_BASE
- LAST30DAYS_REASONING_PROVIDER
- INCLUDE_SOURCES
- LAST30DAYS_X_BACKEND
- LAST30DAYS_YOUTUBE_TRANSCRIPTS
- LAST30DAYS_REDDIT_COMMENTS
- LAST30DAYS_CONFIG_DIR
networkTargets:
- https://api.aisa.one
- https://www.reddit.com
- https://hacker-news.firebaseio.com
- https://www.xiaohongshu.com
---

# Last30days Zh Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/last30days-zh/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
