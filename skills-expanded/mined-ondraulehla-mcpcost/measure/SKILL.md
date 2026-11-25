---
name: measure
description: Measure what the MCP servers in the user's configs cost in context tokens, with npx mcpcost. Use when the user asks what their MCP servers cost, which server is heaviest, or whether to drop one.
---

# Measure the token cost of the user's MCP servers

Every MCP server hands the agent its tool definitions at the start of a session. Those definitions are tokens, paid in every turn. The `mcpcost` CLI starts each configured server, lists its tools and counts the tokens.

## Run

1. Run the measurement from the project root:

   ```bash
   npx -y mcpcost --tools 5
   ```

   With no option, it reads the configs of Claude Code (`.mcp.json`, `~/.claude.json`), Claude Desktop, Cursor, VS Code, Windsurf and Gemini CLI. Add `--config <file>` when the user names one file. Add `--json` when you need the numbers in a structured form.

2. When `ANTHROPIC_API_KEY` is set in the environment, add `--claude`. The counts are then exact for Claude, from the free `count_tokens` endpoint. Without the key the counts are an `o200k_base` estimate; the exact Claude count is about 1.9 times the estimate.

3. Local servers start with the command, args and env from the config, the same way the client starts them. Add `--no-stdio` when the user does not want local servers started.

## Report

- Give the total and the share of a 200k window, then one line per server with its tool count and cost.
- Name the servers above 10 000 tokens and their most expensive tools. Shorter descriptions, fewer optional parameters and fewer tools cut the cost.
- A server with the result `needs auth` is reachable but not measured until its header is in the config.
- Claude Code defers MCP tool definitions with tool search, so the per-turn cost there is lower than the measured total. Cursor, Windsurf and Gemini CLI load every definition up front, so there the total applies as measured.
- For a project that commits its `.mcp.json`, suggest `npx mcpcost --budget <tokens>` in CI. It exits with code 1 when the total is above the budget. The GitHub Action is `ondraulehla/mcpcost@v1`.

## Look up a server before it is added

The `mcpcost` MCP server of this plugin answers for every server in the official MCP registry: `lookup_server`, `search_servers`, `compare_servers` (two to five servers side by side), `check_server` (a live probe of any URL) and `registry_summary`. Use it when the user considers a server and wants to know if it is alive and what it costs before it goes into the config.
