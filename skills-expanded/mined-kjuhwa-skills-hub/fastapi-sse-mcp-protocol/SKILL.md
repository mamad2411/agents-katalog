---
name: fastapi-sse-mcp-protocol
description: Host a hosted MCP (Model Context Protocol) server over FastAPI's StreamingResponse using API-key auth, a session dict, and a tool registry surfaced via the 2025-03-26 Streamable HTTP spec.
category: fastapi-streaming-endpoints
version: 1.0.0
version_origin: extracted
confidence: high
tags: [fastapi, mcp, sse, streaming-response, llm-tools, model-context-protocol]
source_type: extracted-from-git
source_url: https://github.com/BasedHardware/omi.git
source_ref: main
source_commit: 1c310f7fc4c37acf7e1bedb014e3a4adfd56546e
source_project: omi
imported_at: 2026-04-18T00:00:00Z
---

# Pre-hosted MCP Server via FastAPI Streamable HTTP

Expose your LLM-tool surface as a pre-hosted MCP server — clients (Claude Desktop, Cursor, custom agents) talk HTTP instead of spawning a local stdio process. Built on FastAPI `APIRouter` + `StreamingResponse`, a lightweight `MCPSession`, API-key auth, and a plain JSON tool registry.

## When to use

- You own a backend with rich internal tools (DB queries, user memories, vector search) and want Claude / Cursor to invoke them remotely.
- You prefer Bearer API keys per user instead of shipping a client binary.
- You want tools discoverable via the standard MCP `tools/list` handshake without an extra daemon.

## Core pattern

1. **Router**: `router = APIRouter()` mounted under `/mcp` in your FastAPI app.
2. **Session object**: `MCPSession(session_id=str, user_id=str)` with `created_at` + `initialized` flag. Keep them in `active_sessions: dict` (or Redis if multi-instance).
3. **Auth**: `authenticate_api_key(Authorization)` accepts `Bearer <key>` or raw `<key>`, enforces a prefix (`omi_mcp_`), and looks up the user via a dedicated `mcp_api_key` table.
4. **Tool registry**: `MCP_TOOLS = [{name, description, inputSchema}, ...]` — schema is JSON Schema with `type: object`, enums sourced from `MemoryCategory` / `CategoryEnum` Python enums.
5. **Transport**: endpoints return `StreamingResponse(async_gen, media_type="text/event-stream")` for SSE, `JSONResponse` for one-shot ops.

## Steps

1. Define your tool list in code (not YAML): one dict per tool with `name`, `description`, `inputSchema`. Source enum values from your Pydantic models so they can't drift.
2. Implement `authenticate_api_key(authorization)` — return `user_id` or `None`. Use a prefix sentinel to reject stray Bearer tokens.
3. Implement `POST /mcp` — accept JSON body per MCP spec (`initialize`, `tools/list`, `tools/call`). Route by `method` field.
4. For streaming results, yield `data: {json}\n\n` SSE events from an `async def` and wrap with `StreamingResponse(..., media_type="text/event-stream")`.
5. Rate-limit per user with `check_rate_limit_inline(user_id, limit, bucket)` on every call site.
6. Use `uuid.uuid4()` for `session_id`; stash in `active_sessions` only for stateful tools.
7. Serve enum-backed JSON Schema so MCP clients get autocomplete without extra docs.

## Implementation notes

- MCP clients expect `{ "jsonrpc": "2.0", "id": <n>, "result": {...} }` envelopes — wrap tool outputs accordingly.
- `tools/list` returns the raw `MCP_TOOLS` array — no transformation needed.
- Use separate top-level endpoints for `sse` and one-shot `POST` so load balancers with short timeouts don't kill long SSE connections.
- API key format `omi_mcp_xxxx` — the prefix doubles as a fast reject for unrelated tokens without a DB hit.
- Reuse your existing services (`memories_db`, `conversations_db`, `vector_db`) — MCP is a transport, not a new data layer.

## Evidence in source

- `backend/routers/mcp_sse.py` — MCPSession, authenticate_api_key, MCP_TOOLS, StreamingResponse usage
- `backend/routers/chat.py` — WebSocket + StreamingResponse reference implementation
- `backend/main.py` — FastAPI app composition

## Reusability

Any FastAPI product with a meaningful internal tool surface can adopt the same layout. The tool registry is transport-agnostic; you can bolt on stdio MCP later from the same `MCP_TOOLS` list.
