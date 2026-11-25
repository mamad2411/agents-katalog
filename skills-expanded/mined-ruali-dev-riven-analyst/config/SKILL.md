---
name: config
description: Change an installed Riven Analyst configuration. Use when the player wants to change the external vision endpoint, model, API key, bounded web research, or permissions.
---

# Riven Analyst Config

Change only the requested option and preserve the installation scope and unrelated Claude settings.

1. Summarize the current requested change: Provider fields, web research, or permission
   scope. Screenshot directories remain a host-level, per-session permission and are not plugin config.
2. On Claude Code, open the native Riven Analyst plugin configuration for all option changes. On
   Codex, use the host's MCP environment configuration. Sensitive API keys must stay in masked or
   environment-backed secret storage; never request or repeat them in chat.
3. When enabling external vision or bounded web research for the first time, read
   `../setup/SKILL.md` and use its permission preview/apply sequence. Existing permissions need not
   be rewritten when only a model name, endpoint, or key changes.
4. Ask Claude Code to `/reload-plugins`, or start a new Codex task, then state what changed without
   exposing secret values.

Do not create a second config file, edit the plugin cache, run broad diagnostics, or silently alter
the plugin installation scope.
