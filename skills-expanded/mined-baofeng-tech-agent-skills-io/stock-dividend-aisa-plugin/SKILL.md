---
name: stock-dividend-aisa-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-dividend-aisa`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Analyze read-only dividend metrics for stocks via AIsa API. Provides yield, payout ratio, growth CAGR, safety score, income rating, and Dividend Aristocrat/King status without placing trades, making purchases, or managing brokerage accounts. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.'
version: 1.0.2
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
    - AISA_MODEL
    - AISA_BASE_URL
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
optionalEnv:
- AISA_MODEL
- AISA_BASE_URL
networkTargets:
- https://api.aisa.one
---

# Stock Dividend AIsa Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-dividend-aisa/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
