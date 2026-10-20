---
name: ether-claude-memory
description: Consult read-only ether memories and Claude Code session transcripts through the local ether-mcp-claude MCP server when the user asks about past work or session history.
metadata:
  short-description: Read Claude's ether memory safely
allowed-tools: Read, Edit, Write, Grep, Glob, Bash
---

# Claude ether memory

Use the `ether-mcp-claude` MCP server for `.ether` memory and `.claude/projects` transcripts. Do not inspect `.ether` files, databases, or transcript files directly from the agent.

Available tools:

- `session_summaries`: recent archived session summaries; use `last` to bound results.
- `search_memories`: read-only keyword search across problems, learnings, and observations; always provide a focused `query` and a bounded `limit`.
- `claude_sessions`: locate recent top-level Claude sessions before reading one.
- `read_claude_session`: retrieve a bounded recent excerpt by `session_id`; do not request entire transcripts unless the user explicitly needs them.

This skill is read-only. Use the `.void`-scoped ether CLI for Codex's own memory and never mix the two stores. Treat missing or empty results as valid results.
