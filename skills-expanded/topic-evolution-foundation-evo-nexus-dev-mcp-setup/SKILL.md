---
name: dev-mcp-setup
description: Configure MCP servers for the workspace — web search, filesystem, GitHub, Stripe, etc. Use when adding a new integration that needs MCP-level access.
---

# Dev MCP Setup

Derived from oh-my-claudecode (MIT, Yeachan Heo). Adapted for the EvoNexus Engineering Layer.

Configure MCP (Model Context Protocol) servers for the workspace. When a new integration needs access at the MCP layer (rather than via skill-level API calls), this skill walks through the configuration.

## Use When
- Adding a new MCP-backed integration (web search, GitHub, Notion, etc.)
- Diagnosing why an existing MCP server isn't responding
- Setting up a fresh EvoNexus workspace with all standard MCPs

## Do Not Use When
- The integration is API-based (use the appropriate `int-*` skill instead)
- You just need to invoke an existing MCP tool (just use it)

## EvoNexus Standard MCPs

These are typically configured in `~/.claude/settings.json` or `.claude/settings.json`:

| MCP | Purpose | Setup |
|---|---|---|
| google-calendar | Calendar events | OAuth |
| gmail | Email read/send | OAuth |
| linear-server | Linear issues/projects | API key |
| github | GitHub PRs/issues/files | GitHub token |
| canva | Design files | OAuth |
| claude_ai_Notion | Notion pages | OAuth |
| computer-use | Desktop control | local |
| figma | Design files | OAuth |
| plugin_telegram | Telegram bot | bot token |

## Workflow

1. **Identify** which MCP server you need to add
2. **Check current config** — read `.claude/settings.json` (project) or `~/.claude/settings.json` (user)
3. **Add the server entry** with its required env vars or auth
4. **Restart Claude Code** to load the new MCP
5. **Verify** by listing tools — the new MCP's tools should appear with `mcp__<server>__*` prefix
6. **Document** the addition in `workspace/development/research/[C]mcp-setup-{server}-{date}.md`

## Configuration Example

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## Diagnostics

If an MCP isn't working:
1. Check Claude Code logs for spawn errors
2. Verify env vars are set
3. Test the MCP server independently if possible
4. Check that the MCP package is installed

## Pairs With
- `update-config` (built-in skill for settings.json edits)
- `@scout-explorer` (to find existing MCP configurations)
