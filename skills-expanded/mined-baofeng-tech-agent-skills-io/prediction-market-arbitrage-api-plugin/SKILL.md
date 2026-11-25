---
name: prediction-market-arbitrage-api-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `prediction-market-arbitrage-api`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Find arbitrage opportunities across Polymarket and Kalshi prediction markets via AIsa API. Scan sports markets for cross-platform price discrepancies, compare real-time odds, verify orderbook liquidity. Use when user asks about: prediction market arbitrage, cross-platform price differences, sports betting arbitrage, odds comparison, risk-free profit, market inefficiencies.'
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

# Prediction Market Arbitrage API Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/prediction-market-arbitrage-api/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
