---
name: purebasic-mcp-authoring
description: MCP server authoring workflow for PureBasic. Use when designing, creating, reviewing, or extending a PureBasic MCP stdio server, adding MCP tools, writing probe input, defining input schemas, handling initialize/tools/list/tools/call, or enforcing stdout/stderr and safety policy.
---

# PureBasic MCP Authoring

## Server Shape

Default to a console target controlled by `.pbp`.

Start with `purebasic/mcp/new-server` when drafting a new server. Treat its
output as a reviewable scaffold, not an automatic file generator.

Required pieces:

- `*_server.pb` stdio entrypoint
- `*_tool.pbi` or equivalent tool implementation include
- `.pbp` with explicit Console targets
- probe input `.ndjson`
- compiled probe when practical
- README and safety notes
- tests for registration, `tools/list`, `tools/call`, errors, and bounded output

## Protocol Rules

- Register MCP lifecycle with `MCP_RegisterLifecycle()`.
- Register tools with `MCP_RegisterTool()` and `MCP_RegisterToolHandler()`.
- Use `MCP_RegisterToolsList()` and `MCP_RegisterToolsCall()`.
- Use `MCP_Tools_TextResult()` for simple text tool results.
- Keep stdout protocol-only.
- Put diagnostics and logs on stderr.
- Bound command output and query output.
- Draft probe input with `purebasic/mcp/probe`.
- Validate probe or captured transcript text with `purebasic/mcp/validate-stdio`
  before treating it as a correct MCP stdio example.

## Tool Authoring

- Use `purebasic/mcp/add-tool` to draft tool name, title, description, input
  schema, handler pattern, registration pattern, result policy, and tests.
- Return JSON-RPC `-32602` for invalid tool arguments.
- Return MCP `isError: true` for execution failures after arguments are valid.
- Pair every `ParseJSON()` or `CreateJSON()` ownership path with `FreeJSON()`.
- Save authoring drafts only under `.local/` unless the human promotes them into
  tracked documentation or source.

## Safety Defaults

- Reject path escapes by default.
- Prefer explicit allowed roots for filesystem tools.
- Document when a tool is admin/developer-facing rather than sandboxed.
- Ask the human to decide policy boundaries before implementation.

## Verification

Run the server with probe input and run the compiled dispatcher probe. Then run
the repository harness:

```sh
./tools/verify-projects.sh
./tools/verify-docs.sh
./tools/build.sh
./tools/check.sh
```
