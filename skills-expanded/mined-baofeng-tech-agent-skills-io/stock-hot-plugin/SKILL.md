---
name: stock-hot-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-hot`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Hot Scanner — find the most trending and high-momentum stocks and crypto right now via AIsa API. Top gainers, losers, most active by volume, crypto highlights, news catalysts, and top 5 watchlist picks. Use when the user asks about trending stocks, what's hot, market movers, or momentum plays.
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

# Stock Hot Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-hot/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
