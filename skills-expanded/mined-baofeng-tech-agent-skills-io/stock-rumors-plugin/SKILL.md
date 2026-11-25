---
name: stock-rumors-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-rumors`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Rumor Scanner — find early signals including M&A rumors, insider activity, analyst upgrades/downgrades, social whispers, and SEC/regulatory activity via AIsa API. Ranked by impact score. Use when the user asks about rumors, insider trading, M&A activity, analyst changes, or early market signals.
version: 1.0.0
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
    optionalEnv:
    - AISA_BASE_URL
    - AISA_MODEL
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
optionalEnv:
- AISA_BASE_URL
- AISA_MODEL
networkTargets:
- https://api.aisa.one
---

# Stock Rumors Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-rumors/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
