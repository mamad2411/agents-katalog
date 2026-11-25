---
name: saas-gateway-plugin
description: 'Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `saas-gateway`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Unified SaaS integration gateway via api.aisa.one (AISA gateway, v3.1): manage OAuth auth for third-party SaaS apps (Gmail/Slack/GitHub/Notion etc.), tool execution, tool-router sessions, triggers, webhooks, MCP servers, and usage stats. Use when connecting third-party SaaS accounts, running cross-SaaS tools, managing MCP servers, setting up triggers, or checking usage. Keywords: SaaS gateway, connect app, OAuth link, run tool, auth config, tool router, MCP server, trigger, webhook, connected account, usage stats'
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

# Saas Gateway Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/saas-gateway/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
