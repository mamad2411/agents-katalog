---
name: aisa-twitter-engagement-suite-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `aisa-twitter-engagement-suite`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Research Twitter/X profiles, tweets, and trends, then complete approved engagement or posting follow-through through the AIsa relay. Use when: the user needs Twitter/X research plus likes, follows, unfollows, posting, or post-action follow-through without sharing passwords. Supports relay-based reads, OAuth-approved writes, and media-capable posting flows.'
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

# AIsa Twitter Engagement Suite Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/aisa-twitter-engagement-suite/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
