---
name: verify
description: Build, run, and drive mcpdeck end-to-end to verify changes — MCP stdio surface via the SDK client, dashboard via HTTP, CLI via subcommands.
---

# Verifying mcpdeck

## Surfaces

1. **MCP stdio server** (`mcpdeck serve`) — the core product surface. Drive it with the real MCP SDK client, never by unit-importing:

   ```python
   from mcp import ClientSession, StdioServerParameters
   from mcp.client.stdio import stdio_client
   params = StdioServerParameters(
       command="uv",
       args=["run", "--project", "<repo>", "mcpdeck", "serve", "--no-setup",
             "--config", "<cfg.yaml>", "--mcp-servers-json", "<servers.json>"],
       cwd="<repo>",
   )
   # async with stdio_client(params) → ClientSession → initialize / list_tools / call_tool
   ```

   Point `--mcp-servers-json` at a config spawning `tests/fixtures/stub_child_server.py`
   (protocol-complete stub) and optionally a real server (`uvx mcp-server-fetch`).
   Serve works WITHOUT Qdrant (resilient init → fallback routing); with Qdrant up,
   assert `strategy=vector` appears in the log file to prove the primary path.

2. **Dashboard** (`mcpdeck --config mcpdeck.yaml --no-setup`) — Gradio on
   localhost:8080; ready when `curl -s http://localhost:8080/` returns 200 (~7s).

3. **CLI** — `uv run mcpdeck <cmd>`; check exit codes WITHOUT pipes
   (`cmd >/dev/null 2>&1; echo $?`): bad config → 1, unknown flag → 2,
   `validate-config` on a yaml with a bogus field → 1 (extra_forbidden),
   `health` with infra down → 1.

## Infrastructure

- Qdrant: `docker run -d --name <name> -p 6333:6333 -v "$PWD/qdrant_storage:/qdrant/storage" qdrant/qdrant`;
  ready when `curl -s localhost:6333/collections` returns 200 (~2s).
- Docker Desktop on this machine wedges (500 API errors) if probed too early after
  `open -a Docker` — wait for `docker version --format '{{.Server.Version}}'` to
  return non-empty, and if it 500s, quit + `pkill -f "Docker Desktop"` + reopen.
- Tear down after: remove the container, quit Docker Desktop.

## Worthwhile probes

- Unknown tool call → `isError=True`, "Unknown tool: ..."; session must survive.
- `find_tools` with no `query` → clean error; `max_results` 0/negative → 0 / unlimited.
- After the client exits: `pgrep -fl "stub_child_server|mcp-server-fetch|mcpdeck serve"`
  must be empty (no orphaned children).
- Serve with a config that has `web_ui.enabled: true` → first stdout line must be
  pure JSON (initialize response) and port 8080 must stay unbound.

## Gotchas

- stdout of `serve` is JSON-RPC only — logs go to stderr/file; set `logging.file`
  in the test config and grep that for routing evidence.
- First embedding-model load downloads to `~/.cache/huggingface` (~30s once).
- Use the scratchpad for configs/logs, not the repo tree.
