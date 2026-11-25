---
name: mcp-client
description: Call tools on a remote MCP (Model Context Protocol) server over streamable HTTP. Use whenever a connector is an MCP server (e.g. the “MCP server” connector type), or the user asks to list or invoke an MCP server’s tools, prompts, or resources.
license: Apache-2.0
compatibility: Tines 3B
---

# Using a remote MCP server

An MCP server is a JSON-RPC 2.0 API behind a single HTTP endpoint. Talk to it with plain `fetch` from `execute` or a step, with the MCP connector attached — the platform injects authentication on matching requests, so never set Authorization headers yourself, and never print or store tokens.

Read the body of every error response, as the helper below does. A `403` with `"error": "connector_not_connected"` means the user hasn’t connected their own account to a visitor-mode connector. In a workflow’s chat (not a personal chat), call `connectChatToApp` with `connectorId` set to the `app` parameter of its `connect_url`, which waits until the user has connected, then retry. Otherwise show them the body’s `message`, and its `connect_url` as a link if present, then retry once they’ve connected. A `403` whose body is a JSON-RPC error saying a tool “is not allowed by this connector” means the connector only allows the tools its message lists: don’t retry or reconnect, use an allowed tool or tell the user that a connector manager can allow this one. Any other 401 or 403 means the user needs to reconnect the connector; tell them so rather than attempting an auth flow yourself.

## Request basics

Every request is a POST to the server URL with `Content-Type: application/json` and `Accept: application/json, text/event-stream`. The response is either plain JSON or an SSE stream; for SSE, parse each `data:` line as JSON and take the message whose `id` matches your request. This helper handles both:

```ts
let sessionId: string | undefined;

async function mcp(
  url: string,
  method: string,
  params?: Record<string, unknown>,
  id?: number
) {
  const res = await fetch(url, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Accept: "application/json, text/event-stream",
      ...(sessionId ? { "Mcp-Session-Id": sessionId } : {}),
    },
    body: JSON.stringify({
      jsonrpc: "2.0",
      method,
      ...(params ? { params } : {}),
      ...(id !== undefined ? { id } : {}),
    }),
  });
  sessionId = res.headers.get("Mcp-Session-Id") ?? sessionId;
  const text = await res.text();
  if (!res.ok)
    throw new Error(`${method}: HTTP ${res.status}: ${text.slice(0, 500)}`);
  if (id === undefined) return; // notification, no response expected
  const messages = res.headers
    .get("Content-Type")
    ?.includes("text/event-stream")
    ? text
        .split("\n")
        .filter((line) => line.startsWith("data:"))
        .map((line) => JSON.parse(line.slice(5)))
    : [JSON.parse(text)];
  const reply = messages.find((m) => m.id === id);
  if (!reply) throw new Error(`${method}: no response with id ${id}`);
  if (reply.error) throw new Error(`${method}: ${JSON.stringify(reply.error)}`);
  return reply.result;
}
```

## Session lifecycle

1. Send `initialize` with `protocolVersion: "2025-06-18"`, `capabilities: {}`, and your `clientInfo`. If the server rejects the protocol version, retry with the version it offers in the error.
2. If the response carries an `Mcp-Session-Id` header, echo it on every subsequent request (the helper above does this).
3. Send a `notifications/initialized` notification (no `id`).
4. When finished, send a DELETE to the endpoint with the session header if the server supports it; ignore a 405.

```ts
await mcp(
  SERVER_URL,
  "initialize",
  {
    protocolVersion: "2025-06-18",
    capabilities: {},
    clientInfo: { name: "3B", version: "1.0" },
  },
  1
);
await mcp(SERVER_URL, "notifications/initialized");
```

## Tools, prompts, and resources

- `tools/list` returns tool names, descriptions, and JSON Schema inputs. Page with `cursor` if the result has `nextCursor`. Cache the list in a file instead of re-fetching every turn.
- `tools/call` takes `{ name, arguments }`. The result has `content` blocks (usually `{ type: "text", text }`); check `isError` before trusting the output.
- `prompts/list`, `prompts/get`, `resources/list`, and `resources/read` follow the same request shape.

```ts
const { tools } = await mcp(SERVER_URL, "tools/list", {}, 2);
const result = await mcp(
  SERVER_URL,
  "tools/call",
  {
    name: "some_tool",
    arguments: { query: "example" },
  },
  3
);
if (result.isError) throw new Error(result.content?.[0]?.text);
```

Prefer one short-lived session per task. If a long-running call streams progress notifications over SSE, ignore messages without your request `id` — only the matching response carries the result.
