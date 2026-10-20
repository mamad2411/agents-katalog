# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

Blackveil DNS Security Scanner — a Claude Desktop Extension (MCP) that proxies JSON-RPC requests over stdio to a remote hosted worker at `https://dns-mcp.blackveilsecurity.com/mcp`. The extension exposes 51 DNS/email security tools (SPF, DMARC, DKIM, DNSSEC, SSL, CAA, MTA-STS, subdomain discovery, supply-chain mapping, compliance, drift analysis, and more) to Claude Desktop. Listed on the MCP Registry as `com.blackveilsecurity/dns`.

License: BUSL-1.1 (converts to Apache 2.0 after 4 years).

## Commands

```bash
npm run build          # Bundle src/server.ts → dist/server.js via tsup
npm run dev            # Run the proxy: node dist/server.js
npm run typecheck      # TypeScript check (tsc --noEmit)
npm run mcpb:validate  # Validate manifest.json against MCPB spec
npm run mcpb:pack      # Build + pack into .mcpb extension file
npm run mcpb:clean     # Remove .mcpb artifacts
```

No test framework is configured. No linter is configured.

## Architecture

**Single-file proxy** (`src/server.ts`): The entire runtime is one file (~130 lines). It reads JSON-RPC from stdin, POSTs to the remote worker, and writes responses to stdout.

Key design decisions:
- **stdout is reserved for JSON-RPC only** — `console.log` is reassigned to `console.error` so all logging goes to stderr
- **Sequential request processing** — requests are queued via a promise chain (`pending`) to maintain ordering
- **SSE support** — handles `text/event-stream` responses by parsing Server-Sent Events and extracting `data:` lines
- **Session management** — captures `mcp-session-id` from the initialize response and sends it on subsequent requests
- **Zero runtime dependencies** — tsup bundles everything into a single self-contained file with a shebang header

**Configuration:**
- `BV_API_KEY` env var (optional) — injected by MCPB from `user_config.bv_api_key` in manifest.json
- Remote URL is hardcoded (`MCP_URL` constant)

## Build & Distribution

tsup bundles with `noExternal: [/.*/]` — all dependencies are inlined. The output `dist/server.js` is a standalone Node.js executable requiring no `node_modules`.

`.mcpb` packaging (via `@anthropic-ai/mcpb`) creates the distributable extension file. `.mcpbignore` excludes source, configs, and secrets from the bundle.

**CI:** GitHub Actions builds and publishes `.mcpb` to GitHub Releases on `v*` tags.

## Conventions

- ES modules (`"type": "module"`) with ES2022 target
- Strict TypeScript — `strict: true`, `isolatedModules: true`
- Prefix log messages with `[bv-proxy]`
