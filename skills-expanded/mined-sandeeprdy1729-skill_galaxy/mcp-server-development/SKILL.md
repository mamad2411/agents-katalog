---
name: mcp-server-development
description: "Build production-grade Model Context Protocol (MCP) servers for Claude Desktop and other MCP clients. Covers stdio/SSE transports, tool design, OAuth integration, Code Mode patterns, and enterprise deployment."
license: Apache 2.0
tags: ["mcp", "model-context-protocol", "claude", "ai-integration", "server-development", "typescript", "anthropic"]
difficulty: advanced
time_to_master: "8-16 weeks"
version: "1.0.0"
---

# MCP Server Development

## Overview

The Model Context Protocol (MCP) is an open-source standard by Anthropic for bidirectional communication between AI models and external data environments. This skill covers building production-grade MCP servers that expose tools, resources, and prompts to Claude Desktop and other MCP-compatible clients.

## When to Use This Skill

- Building a new MCP server to connect Claude to an external API or data source
- Converting an existing REST API into an MCP-compatible tool server
- Designing multi-tool servers with efficient token usage (avoiding Context Bloat)
- Implementing OAuth 2.1 authentication for multi-user MCP deployments
- Optimizing server performance for enterprise-scale tool calling
- Debugging MCP transport issues (stdio, SSE, Streamable HTTP)

## Core Concepts

### MCP Architecture

```
┌──────────────────┐       Transport Layer        ┌──────────────────┐
│    MCP Client    │ ◄──────────────────────────► │    MCP Server    │
│  (Claude Desktop │   stdio | SSE | HTTP          │                  │
│   / VS Code)     │                               │  Tools           │
│                  │   JSON-RPC 2.0 Messages       │  Resources       │
│                  │ ◄──────────────────────────► │  Prompts         │
└──────────────────┘                               └──────────────────┘
```

### Transport Mechanisms

| Transport | Use Case | Multi-user | Auth Support |
|-----------|----------|------------|--------------|
| **stdio** | Local tools, CLI apps | No | N/A (local) |
| **SSE** | Remote servers, web apps | Yes | OAuth 2.1 |
| **Streamable HTTP** | Modern remote servers | Yes | OAuth 2.1 |

### The N × M Problem

MCP solves the integration explosion where N models × M applications = N×M custom integrations. With MCP, each app builds one server, each model builds one client, reducing total integrations to N + M.

## Implementation Guide

### Minimal MCP Server (TypeScript)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-tool-server",
  version: "1.0.0",
});

// Define a tool
server.tool(
  "search_items",
  "Search the database for items matching a query",
  {
    query: z.string().describe("Search keyword"),
    limit: z.number().optional().default(10).describe("Max results"),
  },
  async ({ query, limit }) => {
    const results = await searchDatabase(query, limit);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }],
    };
  }
);

// Connect via stdio
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Tool Design Best Practices

1. **Minimize tool count** — Group related operations into fewer, smarter tools. Avoid "one tool = one API endpoint."
2. **Use descriptive schemas** — Zod descriptions become the model's understanding of each parameter.
3. **Return structured text** — Format results as readable text, not raw JSON dumps.
4. **Validate inputs at the boundary** — All tool inputs come from the model; sanitize them.
5. **Handle errors gracefully** — Return `isError: true` with a helpful message, never crash.

### Avoiding Context Bloat

The #1 implementation problem in the MCP ecosystem. Loading too many tools consumes the model's context window with schema definitions.

**Anti-pattern:** Exposing 50+ granular tools (one per API endpoint)

**Best practice:** Use "Code Mode" — expose a high-level execution tool that lets the model write code against your API:

```typescript
server.tool(
  "execute_query",
  "Execute a JavaScript function against the platform API. Available: api.listUsers(), api.getUser(id), api.createUser(data), api.updateUser(id, data)",
  { code: z.string().describe("JavaScript code to execute") },
  async ({ code }) => {
    // Sandboxed execution of model-generated code
    const result = await sandbox.run(code, { api });
    return { content: [{ type: "text", text: String(result) }] };
  }
);
```

### OAuth 2.1 for Multi-User Servers

For remote, multi-tenant MCP servers:

```typescript
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";

// OAuth 2.1 authorization server metadata
const authConfig = {
  issuer: "https://your-server.com",
  authorization_endpoint: "/oauth/authorize",
  token_endpoint: "/oauth/token",
  registration_endpoint: "/oauth/register",
  response_types_supported: ["code"],
  grant_types_supported: ["authorization_code", "refresh_token"],
  code_challenge_methods_supported: ["S256"], // PKCE required
};
```

**Key requirements:**
- PKCE is mandatory (no client secrets for public clients)
- Support token refresh for long-running sessions
- Scope-based permissions per tool
- Per-user credential isolation

### Binary File Handling

A known gap in the ecosystem. For servers that need to process PDFs, images, or binary files:

```typescript
server.tool(
  "read_document",
  "Read a document from storage (supports PDF, DOCX, images)",
  { file_id: z.string() },
  async ({ file_id }) => {
    const file = await storage.getFile(file_id);

    if (file.mimeType === "application/pdf") {
      const text = await extractPdfText(file.content);
      return { content: [{ type: "text", text }] };
    }

    if (file.mimeType.startsWith("image/")) {
      const base64 = file.content.toString("base64");
      return {
        content: [{
          type: "image",
          data: base64,
          mimeType: file.mimeType,
        }],
      };
    }

    return { content: [{ type: "text", text: file.content.toString() }] };
  }
);
```

## Testing

### Manual stdio Testing

```bash
# Initialize handshake
echo '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"test","version":"1.0.0"}}}' | node index.js

# With delays for multi-message sequences
{ echo '<init_msg>'; sleep 0.2; echo '<initialized_notification>'; sleep 0.2; echo '<tool_call>'; sleep 0.3; } | node index.js
```

### Integration Testing

```typescript
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({ command: "node", args: ["./index.js"] });
const client = new Client({ name: "test-client", version: "1.0.0" });
await client.connect(transport);

const tools = await client.listTools();
assert(tools.tools.length === 4);

const result = await client.callTool("search_items", { query: "test" });
assert(result.content[0].type === "text");
```

## Deployment Patterns

| Pattern | Transport | Use Case |
|---------|-----------|----------|
| Local subprocess | stdio | Claude Desktop, personal tools |
| Docker container | SSE/HTTP | Team deployments |
| Serverless (Cloudflare Workers) | HTTP | Public MCP servers |
| Kubernetes | SSE/HTTP | Enterprise multi-tenant |

## Security Considerations

- Never expose raw database queries or file system access without sandboxing
- Validate and sanitize all tool inputs — the model can produce unexpected values
- Use PKCE for all OAuth flows; never embed client secrets
- Implement rate limiting on remote servers
- Log all tool invocations for audit trails
- Never return sensitive credentials in tool responses

## Resources

- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [Claude Desktop Config Guide](https://modelcontextprotocol.io/quickstart)

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-31 | Initial documentation |

---

*Part of SkillGalaxy - 10,000+ comprehensive skills for AI-assisted development.*
