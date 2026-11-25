---
name: follow-lib-mcp-sdk
description: Use @modelcontextprotocol/sdk to build MCP servers/clients — tools, resources, prompts
argument-hint: "[target-or-scope]"
related:
  - follow-lib-zod
  - follow-create-mcp
  - use-mcp
  - run-verify
  - run-test

---

## Goal

Use @modelcontextprotocol/sdk to build MCP servers/clients — tools, resources, prompts

## Scope

Use when the task involves `@modelcontextprotocol/sdk` — creating/modifying an MCP server or client with the TypeScript SDK (lib mcp sdk)

- Scaffolding a new MCP project from scratch → `/follow-create-mcp` first, then come back to this skill for SDK details
- Consuming/configuring MCP servers on the Devin side (not writing a server) → `/use-mcp`
- Tool input schemas use zod — for deeper validation → `/follow-lib-zod`

- Latest: `@modelcontextprotocol/sdk@1.30.0` (verified 2026-09-13)
- References: [apis](references/apis.md) | [cli](references/cli.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-server/SKILL.md` — `McpServer`, tools/resources/prompts registration | Deploy | `workflows/deploy-mcp/SKILL.md` — transport options, remote hosting, client config 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Create `new McpServer({name,version})` then register with `server.registerTool()`, `registerResource()`, `registerPrompt()` — each returns a handle for `.update()`/`.remove()` (the `server.tool()` shorthand still works)
1. Use `StdioServerTransport` for local or `StreamableHTTPServerTransport` for remote — HTTP+SSE transport is deprecated (backward compat only)
1. Define tool schemas with zod — name, description, inputSchema (Zod raw shape)
1. Client side uses `Client` + the same transport — test with MCP Inspector
1. Use elicitation when a tool needs extra user input mid-execution — `mode: 'form'` for non-sensitive data, `mode: 'url'` for secrets/OAuth

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib mcp sdk)

## Rules

- Every tool needs a clear description — the LLM uses it to pick tools
- Always return the `{content:[{type:text,text}]}` format
- Handle errors as an `isError: true` response, don't throw
- Version the server to match the spec

- Use `/follow-lib-zod` if writing complex input schemas
- Use `/follow-create-mcp` if scaffolding a new MCP project
- Use `/use-mcp` if consuming MCP servers on the client side
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib mcp sdk)
- No known security/performance pitfalls (lib mcp sdk)
- Lint, typecheck, tests pass
