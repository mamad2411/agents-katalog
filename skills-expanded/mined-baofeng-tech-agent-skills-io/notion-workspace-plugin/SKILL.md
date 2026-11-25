---
name: notion-workspace-plugin
description: 'Requires AISA_API_KEY. Uses the supplied AISA_API_KEY to send requests to https://api.aisa.one. Native-first ClawHub plugin for `notion-workspace`. Ships the packaged AIsa skill with an `openclaw.plugin.json` manifest and a Claude-compatible bundle fallback. Manage Notion workspace: search pages and databases, read markdown, create pages, insert rows, triggers, MCP. Powered by AISA gateway (Notion toolkit). Requires AISA_API_KEY and curl. Keywords: notion, workspace, page, database, block, markdown, wiki, task board, insert row, OAuth. Use when: the user needs web search, research, source discovery, or content extraction.'
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

# Notion Workspace Plugin

This root manifest mirrors the packaged skill runtime so ClawHub registry scans can read the same requirements declared in the native plugin manifests.

- Packaged skill: `skills/notion-workspace/`
- Native manifest: `openclaw.plugin.json`
- Claude-compatible fallback: `.claude-plugin/plugin.json`
