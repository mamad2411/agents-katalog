---
name: crypto-market-data-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `crypto-market-data`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Query real-time and historical cryptocurrency market data via CoinGecko through AIsa — simple prices, coin details, historical charts, OHLC candles, token prices by contract address, market-cap rankings, exchange data and tickers, categories, trending searches, and crypto news. Use when you need crypto market research, price tracking, token lookup, portfolio analysis, or market-cap screening. Use when: the user needs market data, stock analysis, dividend research, or read-only financial data workflows.'
version: 1.0.1
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

# Crypto Market Data Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/crypto-market-data/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
