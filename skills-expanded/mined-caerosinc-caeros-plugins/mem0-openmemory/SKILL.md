---
name: mem0-openmemory
description: Run OpenMemory, Mem0's local-first private memory server with an MCP interface and dashboard, and choose between it and the hosted Mem0 MCP. Use when the user wants self-hosted, private, cross-tool memory.
---

# OpenMemory (Local-First Memory)

OpenMemory is Mem0's local, private memory server: a shared memory layer that
multiple MCP clients on your machine can read and write, with nothing synced
to a cloud. Source lives in the `openmemory` directory of the
`mem0ai/mem0` GitHub repository.

## Architecture

- FastMCP-based server exposing memory tools over SSE and streamable HTTP.
- Storage fully local: Postgres for structured data plus Qdrant as the vector
  store, both run via Docker.
- Dashboard UI showing which client apps read or wrote which memories, with
  per-app pause/revoke and audit logs for every access.
- An LLM key (OpenAI by default) is required for fact extraction.

## Run it

```bash
git clone https://github.com/mem0ai/mem0.git
cd mem0/openmemory
# put OPENAI_API_KEY=... in the backend .env (see repo README for the path)
make build   # build images
make up      # start API server, vector DB, MCP server
# then start the frontend dashboard per the README
```

Default MCP endpoint pattern (SSE):

```
http://localhost:8765/mcp/<client-name>/sse/<username>
```

Each client app connects with its own client name, which is how the dashboard
attributes reads and writes and lets you revoke one app without touching
others.

## Hosted alternative

If local infrastructure is not wanted, the official hosted Mem0 MCP server
(`https://mcp.mem0.ai/mcp`, bundled with this plugin) provides the same
memory lifecycle backed by the Mem0 platform and a `MEM0_API_KEY`. Decision
guide:

- OpenMemory: privacy-sensitive data, offline work, no per-request cost,
  you operate Docker.
- Hosted platform: zero ops, memories available across machines and deployed
  apps, platform features (entities, events, analytics).

Both speak MCP, so client configuration is the only switch.

## Practices

- Back up the Postgres and Qdrant volumes if local memories matter; wiping
  containers wipes memory.
- Use one username consistently across clients, otherwise memories fragment
  per user namespace.
- Keep the extraction key funded; failed extraction means silent no-op adds.
- Verify current setup steps against the repo README before installing: the
  compose layout and make targets evolve. The repo is the authoritative
  source (https://github.com/mem0ai/mem0/tree/main/openmemory).
