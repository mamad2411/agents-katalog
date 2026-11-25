---
name: chat-bridge
description: Opt-in skill to surface TeaAgent daily brief and prompt-mode runs via chat (Slack, Discord, Telegram) using MCP HTTP.
---

# Chat bridge (opt-in)

Use this skill when you want chat surfaces to trigger read-only daily briefs or approved prompt-mode runs — **not** as a core harness feature.

## Prerequisites

- `teaagent init` with provider configured
- `teaagent mcp serve --http` reachable from your bridge host
- Chat bot token stored outside the repo (env vars only)

## Workflow

1. Start MCP HTTP: `teaagent mcp serve --http --host 127.0.0.1 --port 7331`
2. Map chat commands to MCP tool calls or shell wrappers:
   - `/daily` → `teaagent daily` (read-only JSON)
   - `/status` → `teaagent status --short`
   - `/approve <tool>` → `teaagent approval grant <tool> --scope session`
3. Never expose `danger-full-access` or raw shell mutate tools to public channels.

## Security

- Treat the bridge as **untrusted input**; keep permission mode `read-only` or `prompt` with HITL.
- Audit every tool call; rotate tokens if the channel is compromised.

See [examples/ergonomics/](../../../examples/ergonomics/) for desktop launcher recipes.
