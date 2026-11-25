---
name: seo-keyword-research-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `seo-keyword-research`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Use this skill when a user asks for SEO keyword research, keyword discovery, search volume analysis, keyword difficulty, search intent mapping, topic clusters, content opportunities, competitor keyword gaps, or a keyword strategy for a domain, URL, product, market, or seed topic. When a website is provided, crawl and interpret the site first, then use AIsa API access to DataForSEO keyword, SERP, trend, Labs, and OnPage endpoints plus AIsa LLM reasoning to find non-brand keyword opportunities. Use when: the user needs web search, research, source discovery, or content extraction.'
version: 1.0.0
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

# Seo Keyword Research Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/seo-keyword-research/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
