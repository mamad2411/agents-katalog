---
name: stateless-streamable-http-mcp
description: Use StreamableHTTPServerTransport with sessionIdGenerator:undefined to serve MCP over HTTP without session affinity — multiple subprocess clients share one server, every request is independent.
category: architecture
version: 1.0.0
version_origin: extracted
tags: [mcp, http, stateless, streamable-http]
confidence: medium
source_type: extracted-from-git
source_url: https://github.com/lukilabs/craft-agents-oss.git
source_ref: main
source_commit: 61f7d48a5b4fd0a8094f002c9e3aea5f3824dcfb
source_project: craft-agents-oss
source_path: packages/shared/src/mcp/pool-server.ts
imported_at: 2026-04-18T00:00:00Z
---

# Stateless Streamable-HTTP MCP

## When to use
- Building an MCP server meant to be consumed by MULTIPLE client subprocesses (Codex, Copilot, CLI).
- Don't want the complexity of MCP's session-aware SSE transport.
- Tools are stateless - any client can call any tool at any time.

## How it works
1. Instantiate the transport with `sessionIdGenerator: undefined`:
   ```ts
   new StreamableHTTPServerTransport({ sessionIdGenerator: undefined })
   ```
   This puts the transport in **stateless** mode - no session cookie, no server-side session registry, no sticky routing.
2. Connect a single `Server` instance to the transport. All clients share it.
3. Mount at a single path (`/mcp`). Route every method (POST, GET, DELETE) to `transport.handleRequest(req, res)` - the transport does the JSON-RPC dispatch internally.
4. Each incoming request is fully processed before the socket closes; no long-polling session state.
5. Clients use `StreamableHTTPClientTransport(new URL(serverUrl))`. In stateless mode, they don't persist a session ID between calls.

## Example
```ts
import { createServer } from 'node:http';
import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';

const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
const mcp = new Server({ name: 'pool', version: '1.0.0' }, { capabilities: { tools: {} } });
mcp.setRequestHandler(ListToolsRequestSchema, async () => ({ tools: await collectTools() }));
mcp.setRequestHandler(CallToolRequestSchema, async (req) => runTool(req.params.name, req.params.arguments));
await mcp.connect(transport);

createServer(async (req, res) => {
  if (new URL(req.url!, 'http://127.0.0.1').pathname !== '/mcp') { res.writeHead(404).end(); return; }
  await transport.handleRequest(req, res);
}).listen(0, '127.0.0.1');
```

## Gotchas
- Resource subscriptions and server-initiated notifications DO require a session ID; stateless mode disables them.
- Bind to loopback if you don't have auth - the HTTP layer doesn't check anything.
- `handleRequest` expects a Node `http.IncomingMessage`/`ServerResponse` pair, not Fetch `Request`/`Response` - wrap if you're in a Fetch-native framework.
- When tools are expensive, add your own rate limiting upstream - stateless means no built-in coalescing.
- Random port (`listen(0)`) works nicely - read `server.address()` after listen to learn the port.
