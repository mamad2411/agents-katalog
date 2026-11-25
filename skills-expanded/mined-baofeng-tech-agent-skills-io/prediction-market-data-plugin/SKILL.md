---
name: prediction-market-data-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `prediction-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Access prediction market data from Polymarket and Kalshi, including markets, prices, trades, orderbooks, positions, and cross-platform market matching. Use when you need current odds, historical market data, or wallet-level prediction market analysis.
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

# Prediction Market Data Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/prediction-market-data/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
