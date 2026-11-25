---
name: openclaw-twitter-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `openclaw-twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Search X/Twitter profiles, tweets, trends, lists, communities, and Spaces through the AISA relay, then publish approved posts with OAuth. Use when: the user asks for Twitter/X research, monitoring, or posting without sharing passwords. Supports read APIs, authorization links, and media-aware posting.'
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
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one/apis/v1/twitter
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one/apis/v1/twitter
---

# Openclaw Twitter Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/openclaw-twitter/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
