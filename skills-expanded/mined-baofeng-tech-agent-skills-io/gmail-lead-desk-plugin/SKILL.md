---
name: gmail-lead-desk-plugin
description: 'Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `gmail-lead-desk`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Gmail Lead Desk — standalone sales/CS Gmail skill via the AISA gateway: OAuth connect, scan unread leads, summarize threads, draft template replies (default draft-only), archive with labels. Keywords: Gmail Lead Desk, Gmail, lead desk, sales, customer support, follow-up, unread, inquiry summary, draft reply, archive, OAuth, AISA, connected account, thread_id. Use when: the user needs this workflow''s domain-specific automation or guidance.'
version: 1.0.0
license: MIT
requires:
  bins: []
  env:
  - AISA_API_KEY
metadata:
  aisa:
    requires:
      env:
      - AISA_API_KEY
    primaryEnv: AISA_API_KEY
    networkTargets:
    - https://api.aisa.one
primaryEnv: AISA_API_KEY
networkTargets:
- https://api.aisa.one
---

# Gmail Lead Desk Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/gmail-lead-desk/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
