---
name: twitter-post-aisa-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `twitter-post-aisa`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Run Twitter/X likes, follows, replies, and OAuth-gated posting through AIsa. Use when: the user already knows which account, tweet, or campaign to act on and needs explicit engagement workflows. Supports read context, engagement actions, and approved posting.'
version: 1.0.3
license: MIT-0
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

# Twitter Post AIsa Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/twitter-post-aisa/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
