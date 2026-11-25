---
name: stock-watchlist-plugin
description: Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-watchlist`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Manage a stock/crypto watchlist with price target and stop-loss alerts via AIsa API. Add, remove, list, and check tickers with live price alerts. Use when the user wants to track stocks, set price alerts, manage a watchlist, or check triggered alerts.
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

# Stock Watchlist Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-watchlist/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
