---
name: kol-creator-discovery-plugin
description: 'Requires python3, and AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `kol-creator-discovery`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Use this skill when a user needs KOL or influencer research, creator email lookup, similar-creator discovery, outreach-list building, influencer prospecting, or a contact table from TikTok, Instagram, or YouTube profile URLs. It uses AIsa''s WaveInflu APIs to find verified creator emails, match similar YouTube or TikTok creators, enrich each recommended profile with contact emails, and return an outreach-ready Markdown table without inventing missing data. Use when: the user needs YouTube search, trend discovery, channel research, or SERP analysis.'
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

# Kol Creator Discovery Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/kol-creator-discovery/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
