# MCP Server Module

This directory owns the `mcp-server` repo module — exposes KOTA tools via
the Model Context Protocol over stdio and Streamable HTTP.

- Registers the `kota mcp-server` CLI command. The action handler routes
  through `ctx.client.mcpServer.start(opts)`. The local handler in
  `mcp-server-operations.ts` re-loads the full module set (lifecycle mode
  `"runtime"`) before instantiating `McpServer` so every contributed tool
  is available. The daemon-side handler returns
  `{ ok: false, reason: "daemon_required" }` because the daemon cannot
  start a local MCP server in the operator's process; the CLI maps that to
  a "stop the daemon first" hint.
- Owns the `McpServer` orchestrator, the per-feature handler files, prompt
  and resource helpers, and the co-located server tests. New MCP method
  handlers go in the `mcp-handlers-<feature>.ts` sibling that owns that
  feature area (initialize, resources, prompts, tools, sampling,
  elicitation, completion). `server.ts` only owns lifecycle, transport, and
  method-name dispatch; one feature area per file.
- `streamable-http.ts` is the transport adapter for the HTTP endpoint.
  Keep HTTP header/origin validation there and reuse `McpServer` dispatch
  instead of forking feature handlers.
- Treat MCP as a transport over KOTA capabilities, not a second capability
  registry. Tools, resources, prompts, sampling, roots, and elicitation are
  adapters around existing runtime contracts.
- The MCP client and manager stay in `src/core/mcp/` because the session
  loop and tool runner consume them directly. Do not import from there here
  unless a new genuine runtime primitive appears.
- Exact MCP method names, resource identifiers, prompt names, capability
  flags, and payload shapes belong in source and protocol tests, not in
  durable prose.
- This module owns the `KotaTool` ↔ MCP tool-definition translation at the
  adapter seam (see `src/core/agent-harness/AGENTS.md`).
