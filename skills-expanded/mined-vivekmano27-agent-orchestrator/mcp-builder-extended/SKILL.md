---
name: mcp-builder-extended
description: Build MCP (Model Context Protocol) servers for Claude Code. Covers server structure (tools, resources, prompts), transport types (stdio, SSE), tool parameter design, error handling, testing, and TypeScript examples using @modelcontextprotocol/sdk.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# MCP Builder Extended

## When to Use

- Building a new MCP server to give Claude Code custom tools
- Adding tools, resources, or prompts to an existing MCP server
- Designing tool parameters and return types
- Choosing between stdio and SSE transports
- Testing MCP servers locally

## Patterns

### MCP Server Primitives

| Primitive | Purpose | Example |
|-----------|---------|---------|
| **Tools** | Actions the AI can invoke | `create_issue`, `run_query` |
| **Resources** | Read-only data the AI can access | `db://users/123`, `config://settings` |
| **Prompts** | Reusable prompt templates | `code-review`, `test-plan` |

### Server Setup with Tools

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({ name: "my-project-tools", version: "1.0.0" });

server.tool(
  "search_database",
  "Search the project database with a filter",
  {
    table: z.enum(["users", "projects", "tasks"]).describe("Table to search"),
    filter: z.string().describe("Filter condition, e.g. 'status = active'"),
    limit: z.number().min(1).max(100).default(20).describe("Max results"),
  },
  async ({ table, filter, limit }) => {
    try {
      const results = await db.query(table, filter, limit);
      return { content: [{ type: "text", text: JSON.stringify(results, null, 2) }] };
    } catch (error) {
      return {
        content: [{ type: "text", text: `Query failed: ${(error as Error).message}` }],
        isError: true,
      };
    }
  },
);
```

### Resources and Prompts

```typescript
server.resource("config", "config://app-settings", async (uri) => ({
  contents: [{ uri: uri.href, mimeType: "application/json", text: JSON.stringify(await loadConfig()) }],
}));

server.prompt(
  "code-review",
  "Structured code review prompt",
  { language: z.string().describe("Programming language") },
  ({ language }) => ({
    messages: [{ role: "user", content: { type: "text",
      text: `Review this ${language} code for correctness, performance, security, readability.` } }],
  }),
);

const transport = new StdioServerTransport();
await server.connect(transport);
```

### Transport Types

**stdio (local)** -- configure in `.mcp.json` or `~/.claude/mcp.json`:

```json
{ "mcpServers": { "my-tools": { "command": "npx", "args": ["tsx", "src/index.ts"] } } }
```

**SSE (remote)** -- for shared/hosted servers:

```typescript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";
const app = express();
app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});
app.listen(3100);
```

### Tool Parameter Design

- `z.describe()` on every parameter -- Claude reads these descriptions
- `z.enum()` for finite option sets instead of free-form strings
- `z.default()` for sensible defaults; `z.optional()` for truly optional params
- `.min()` / `.max()` for range validation
- Keep under 6 parameters per tool; split if needed

### Error Handling

Never throw from tool handlers. Return error content:

```typescript
// CORRECT
return { content: [{ type: "text", text: `Error: ${err.message}` }], isError: true };

// WRONG -- unhandled throw crashes the server
const result = await execute(query);
```

### Testing

Test with the MCP inspector: `npx @modelcontextprotocol/inspector npx tsx src/index.ts`
Test with Claude Code: `claude --mcp-server "my-tools: npx tsx src/index.ts"`

### Project Structure

Organize as `src/` with `index.ts` (entry + transport), `tools/` (one file per group), `resources/`, `prompts/`, and `lib/` (shared utilities).

## Anti-Patterns

- **Throwing in tool handlers** -- always return `{ isError: true }` content
- **Missing `.describe()` on parameters** -- Claude cannot infer what a parameter does
- **Giant monolithic tools** -- 10+ parameters should be split into focused tools
- **`console.log` in stdio mode** -- stdout is the transport; use `console.error` (stderr)
- **No input validation** -- always validate with Zod schemas
- **Using `any` in schemas** -- defeats type safety and gives Claude no guidance

## Checklist

- [ ] Server uses `@modelcontextprotocol/sdk` with `McpServer` class
- [ ] Every tool parameter has `.describe()` annotation
- [ ] All handlers use try/catch and return `{ isError: true }` on failure
- [ ] Transport chosen: stdio for local, SSE for remote
- [ ] MCP config added to `.mcp.json` or `~/.claude/mcp.json`
- [ ] Tested with `npx @modelcontextprotocol/inspector`
- [ ] Logging uses `console.error`, never `console.log` in stdio mode
- [ ] Tools kept focused (under 6 parameters each)
- [ ] Resources expose read-only data with proper MIME types
