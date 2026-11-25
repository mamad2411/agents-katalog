---
name: stock-analysis-plugin
description: Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `stock-analysis`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Analyze stocks and cryptocurrencies with 8-dimension scoring via AIsa API. Provides BUY/HOLD/SELL signals with confidence levels, entry/target/stop prices, and risk flags. Supports single or multi-ticker analysis with optional fast mode and JSON output. Use when the user asks to analyze a stock, check a ticker, or compare investments.
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

# Stock Analysis Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/stock-analysis/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
