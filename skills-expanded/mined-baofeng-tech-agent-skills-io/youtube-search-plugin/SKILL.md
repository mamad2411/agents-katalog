---
name: youtube-search-plugin
description: 'Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `youtube-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. YouTube Search API via AIsa unified endpoint. Search YouTube videos, channels, and playlists with a single AIsa API key — no Google API key or OAuth required. Use this skill when users want to search YouTube content. For other AIsa capabilities (LLM, financial data, Twitter, web search), see the aisa-core skill. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.'
version: 1.0.0
license: Apache-2.0
requires:
  bins: []
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# Youtube Search Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/youtube-search/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
