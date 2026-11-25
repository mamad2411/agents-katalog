---
name: mcp-integration
description: Select, scaffold, or integrate Model Context Protocol (MCP) servers with a Claude Code plugin. Use when the user asks to "add an MCP", "which MCP for X", "connect to [service]", "find a server for [API/tool]", "wrap [tool] as an MCP", ".mcp.json", "MCP server config", or when a domain needs external tools Claude doesn't have (Blender, Figma, ClickUp, arxiv, a CAD program, etc.). Covers MCP discovery via registry, config schema, env/userConfig wiring, and fallback to CLI when no MCP exists.
---

# MCP Integration

An MCP server exposes tools to Claude over a standard protocol. Plugins can bundle MCPs or connect to remote ones.

## Decision flow for a new domain

1. **Search the MCP registry first**: use `search_mcp_registry` with domain keywords. Examples: `["blender", "3d", "modeling"]`, `["figma", "design"]`, `["arxiv", "papers"]`.
2. **If registry has a match**: use `suggest_connectors` to surface it to the user for one-click connect. Wire the MCP in `.mcp.json`.
3. **If no match**: evaluate
   - (a) wrap the domain's CLI via the Bash tool (cheapest),
   - (b) write a thin MCP server that shells out to the CLI (reusable),
   - (c) write a full MCP server with a native SDK binding (highest leverage).
4. **Fallback**: for GUI-only tools, orchestrate via Playwright browser MCP.

## `.mcp.json` schema

```json
{
  "mcpServers": {
    "blender-bpy": {
      "command": "${CLAUDE_PLUGIN_ROOT}/bin/blender-mcp",
      "args": ["--blender-path", "${user_config.blender_path}"],
      "env": {
        "PYTHONPATH": "${CLAUDE_PLUGIN_DATA}/venv/lib/python3.11/site-packages"
      }
    }
  }
}
```

## Inline vs. file

Small MCPs can go inline in `plugin.json` under `mcpServers`. Prefer `.mcp.json` when config gets non-trivial or you want to edit without bumping the plugin version.

## Dependency install pattern

Use `SessionStart` hook to install deps into `${CLAUDE_PLUGIN_DATA}` lazily:

```json
{
  "hooks": {
    "SessionStart": [{
      "hooks": [{
        "type": "command",
        "command": "diff -q \"${CLAUDE_PLUGIN_ROOT}/requirements.txt\" \"${CLAUDE_PLUGIN_DATA}/requirements.txt\" >/dev/null 2>&1 || (cp \"${CLAUDE_PLUGIN_ROOT}/requirements.txt\" \"${CLAUDE_PLUGIN_DATA}/\" && python3 -m venv \"${CLAUDE_PLUGIN_DATA}/venv\" && \"${CLAUDE_PLUGIN_DATA}/venv/bin/pip\" install -r \"${CLAUDE_PLUGIN_DATA}/requirements.txt\")"
      }]
    }]
  }
}
```

## Writing your own MCP server

- Use the official MCP SDK (TypeScript or Python) — https://modelcontextprotocol.io.
- Expose tools with tight schemas (JSONSchema for each param).
- Keep tool names verb-first and specific: `blender_render_scene`, not `do_thing`.
- Return structured JSON, not prose.
- Log to stderr; stdout is the protocol.

## Anti-patterns

- Embedding API keys in `mcpServers.env`. Use `userConfig` with `sensitive: true`.
- Long-running tools without timeouts. Every tool call should have a sane upper bound.
- MCP servers that do 10 things. Split into focused servers per capability cluster.

## References

- @../../agents-architect/references/mcp-selection.md — decision tree + registry usage

## Output

When integrating MCPs for a domain:

1. Run registry search and present options.
2. If bundling: add to `.mcp.json` + any `requirements.txt` or install script.
3. If remote: document connect flow in README.
4. Add `userConfig` entries for any tokens/paths.
5. Validate: spin up a Claude Code session with the plugin and verify tools appear in `/mcp`.
