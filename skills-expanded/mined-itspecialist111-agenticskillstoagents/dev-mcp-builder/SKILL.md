# dev/mcp-builder — skill payload

> Machine-readable contract: [`../mcp-builder.manifest.json`](../mcp-builder.manifest.json).

## What this skill does

Scaffolds a FastMCP Python MCP server from a tool-list spec. Generated
files include:

- `server.py` with `FastMCP(name=...)` and one `@mcp.tool` stub per
  declared tool, wired for both `stdio` and `streamable-http` transports
  via an `MCP_TRANSPORT` env var.
- `requirements.txt` pinning `fastmcp` and friends.
- `Dockerfile` with the standard `uvicorn` entry point for HTTP transport.
- `tests/test_server.py` with one passing smoke test per tool.

## When to use it

- You're standing up a new MCP server from scratch.
- A new skill needs its own endpoint (one MCP host per plugin — see the
  Cowork limitations doc) and you want a starter that already passes the
  smoke tests in this repo.

## When **not** to use it

- You're adding a tool to an *existing* MCP server — edit the existing
  `server.py` directly.
- Your target is a non-Python MCP server (TypeScript, Go) — this skill
  only emits Python.

## Determinism and risk

Determinism: **medium** — file paths are deterministic; comments and
docstrings vary slightly. Risk: **low** — generated files are reviewable
before commit.

## How it composes

Often paired with `dev/skill-creator` for end-to-end "new capability →
new server" bootstrapping, and `dev/webapp-testing` for the post-deploy
verification step.
