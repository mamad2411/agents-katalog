---
name: newna-install-mcp
description: Slash command to install NewNa.AI MCP servers into Claude Code or Codex. Use /newna-install-mcp to set up all servers, or /newna-install-mcp powerbi-knowledge for a specific one.
argument-hint: [server-name|all]
allowed-tools: [Bash, Read, Write, Edit, Grep, Glob]
---

# /newna-install-mcp

Install NewNa.AI MCP servers into your current environment.

**Usage:**
- `/newna-install-mcp` — install all available servers
- `/newna-install-mcp powerbi-knowledge` — install a specific server
- `/newna-install-mcp --codex` — install into Codex instead of Claude Code
- `/newna-install-mcp --both` — install into both Claude Code and Codex

Arguments: $ARGUMENTS

Now follow the full installation procedure from the `install-mcp` skill. Read the `install-mcp` skill's SKILL.md (sibling directory) and execute it with the arguments above.
