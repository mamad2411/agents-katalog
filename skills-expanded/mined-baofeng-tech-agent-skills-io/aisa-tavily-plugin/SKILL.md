---
name: aisa-tavily-plugin
description: 'Requires node, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `aisa-tavily`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search the web and extract public page content through AIsa''s Tavily-backed API relay. Use when: the user needs open-web research, source discovery, current news lookup, or public URL extraction. Supports concise result sets, deeper research, and news-focused queries.'
version: 1.0.0
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

# AIsa Tavily Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-tavily/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
