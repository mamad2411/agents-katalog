---
name: stock-portfolio-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-portfolio`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Manage investment portfolios with live P&L tracking via AIsa API. Create, add, update, remove positions, rename, and show portfolio summary with real-time profit/loss. Use when the user wants to track investments, manage a portfolio, check P&L, or add/remove holdings.
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

# Stock Portfolio Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-portfolio/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
