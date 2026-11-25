---
name: repo-mcp-tool-selection
description: Selects appropriate MCP servers for repository-level developer tooling. Use when deciding whether an MCP belongs in this plugin, a separate integration plugin, a technology-specific plugin, or should be omitted.
---

# Repo MCP Tool Selection

Use this skill when adding or evaluating MCP servers.

## Decision Principles

1. Add MCP only when it improves real work.
2. Prefer official or vendor-maintained servers.
3. Keep source-control, issue tracking, browser automation, database, cloud, observability, and CI/CD MCPs in separate plugins.
4. Keep servers disabled by default.
5. Prefer narrow tools over broad, credentialed, write-capable tools.
6. Avoid duplicating built-in editor capabilities.

## Use the Matrix

Use `resources/mcp-selection-matrix.md` to decide whether an MCP server belongs here.

## Workflow

Use `workflows/mcp-tool-selection-workflow.md` when adding or reviewing a new MCP candidate.

