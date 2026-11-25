---
name: aisa-twitter-api-command-center-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `aisa-twitter-api-command-center`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X research, monitoring, watchlists, and OAuth-gated posting through AIsa. Use when: the user needs one flagship Twitter skill for trend tracking, competitor monitoring, or publish-ready workflows. Supports search, watchlists, and approved posting.'
version: 1.0.3
license: Apache-2.0
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
    - https://api.aisa.one/apis/v1/twitter
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one/apis/v1/twitter
---

# AIsa Twitter API Command Center Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-twitter-api-command-center/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
