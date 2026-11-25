---
name: twitter-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one/apis/v1/twitter. Native-first ClawHub plugin for `twitter`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Searches and reads X (Twitter): profiles, timelines, mentions, followers, tweet search, trends, lists, communities, and Spaces. Publishes posts, likes/unlikes tweets, and follows/unfollows users after the user completes OAuth in the browser. Use when the user asks about Twitter/X data, social listening, posting, or interacting with tweets/users without sharing account passwords.'
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
    - TWITTER_RELAY_BASE_URL
    - TWITTER_RELAY_TIMEOUT
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one/apis/v1/twitter
primaryEnv: AISA_API_KEY
optionalEnv:
- TWITTER_RELAY_BASE_URL
- TWITTER_RELAY_TIMEOUT
networkTargets:
- https://api.aisa.one/apis/v1/twitter
---

# Twitter Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/twitter/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
