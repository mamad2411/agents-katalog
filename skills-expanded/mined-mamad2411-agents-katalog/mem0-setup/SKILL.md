---
name: mem0-setup
description: Set up Mem0, including platform API keys, SDK install, the hosted MCP server, and the open-source self-hosted library. Use when connecting to Mem0 for the first time or picking between platform and OSS.
---

# Mem0 Setup

## Platform vs OSS library

- **Mem0 Platform** (recommended start): managed API, dashboard, analytics.
  Sign up at https://app.mem0.ai, create an API key in the dashboard.
- **OSS library**: `from mem0 import Memory` runs the memory engine in your
  process against your own vector store, LLM, and embedder. No Mem0 account,
  but you configure and host the dependencies.

## Platform keys

```bash
export MEM0_API_KEY="..."
```

- The SDKs (`MemoryClient`) read `MEM0_API_KEY` automatically; you can also
  pass `api_key` explicitly.
- Treat it like any secret: secret manager or untracked `.env`, never in
  code, chat, or client-side bundles.
- Use separate keys per environment so revocation does not take down prod.

Install SDKs:

```bash
pip install mem0ai
npm install mem0ai
```

Verify: one `client.add(...)` then `client.search(...)` round trip (see
`mem0-integration`), and check the memory appears in the dashboard.

## Hosted MCP server

This plugin bundles Mem0's official hosted MCP server:

- URL: `https://mcp.mem0.ai/mcp` (streamable HTTP)
- Auth: your `MEM0_API_KEY` as a bearer token, supplied through the MCP
  client's auth flow or environment, never inlined in config files.

It exposes 11 tools covering the full lifecycle: `add_memory`,
`search_memories`, `get_memories`, `get_memory`, `update_memory`,
`delete_memory`, `delete_all_memories`, `delete_entities`, `list_entities`,
`list_events`, `get_event_status`.

For a fully local alternative with the same MCP surface, see
`mem0-openmemory`.

## OSS self-host sketch

```python
from mem0 import Memory

m = Memory.from_config({
    "vector_store": {"provider": "qdrant", "config": {"host": "localhost"}},
    "llm": {"provider": "openai", "config": {"model": "gpt-5-mini"}},
})
m.add("I prefer dark mode", user_id="user123")
```

The OSS path needs an LLM key for extraction and an embedder; supported
providers and exact config keys are listed in the docs
(https://docs.mem0.ai). Data residency and cost are yours to manage.

## Troubleshooting

- 401 from platform or MCP: key missing, revoked, or wrong environment.
- `add` returns but nothing stored: extraction found no durable fact, or the
  async job failed; check `list_events` / `get_event_status`.
- Search misses obvious facts: confirm the same scope ids were used at add
  time and in search filters.
