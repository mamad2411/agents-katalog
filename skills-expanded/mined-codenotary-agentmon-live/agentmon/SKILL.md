---
name: agentmon
description: Open AgentMon Live's web view, which shows every Codex chat on this machine live. Use when the person asks for AgentMon, the AgentMon page, or to watch their chats in the browser.
---

# AgentMon Live

1. Make sure the server runs: `node "<plugin root>/server/web.mjs" ensure 47311`. The plugin's SessionStart hook normally started it already.
2. Give the person the link `http://127.0.0.1:47311/`. Open it with `xdg-open` (Linux) or `open` (macOS) only when they ask you to.

The page lists each chat's turns, tool calls, checks, edited files, context and limits. For feedback to the makers, use the `feedback` tool of the `agentmon-live` MCP server: it returns a link the person submits themselves.
