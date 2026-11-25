---
name: aisa-multi-search-engine-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `aisa-multi-search-engine`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Multi-source search engine powered by AIsa API. Combines Tavily web search, Scholar academic search, Smart hybrid search, and Perplexity deep research — all through a single AIsa API key. Includes confidence scoring and AI synthesis. Use when: the user needs web search, research, source discovery, or content extraction.'
version: 1.0.2
license: MIT
requires:
  bins:
  - python3
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      bins:
      - python3
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# AIsa Multi Search Engine Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-multi-search-engine/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
