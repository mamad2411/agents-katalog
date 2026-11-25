---
name: aisa-tavily-search-plugin
description: 'Requires node, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `aisa-tavily-search`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run web, multi-source, or last-30-days research through AIsa. Use when: the user needs search, synthesis, competitor scans, or trend discovery. Supports research-ready outputs and structured retrieval.'
version: 1.0.3
license: Apache-2.0
requires:
  bins:
  - node
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      bins:
      - node
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# AIsa Tavily Search Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-tavily-search/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
