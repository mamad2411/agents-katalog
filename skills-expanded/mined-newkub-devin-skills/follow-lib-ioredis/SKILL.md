---
name: follow-lib-ioredis
description: Use ioredis for the Redis client — connection, pipeline, pub/sub, cluster, Sentinel
argument-hint: "[target-or-scope]"
related:
  - follow-secret-manager
  - run-verify
  - run-test

---

## Goal

Use ioredis for the Redis client — connection, pipeline, pub/sub, cluster, Sentinel

## Scope

Use when the task involves ioredis — the Redis client on Node.js/Bun connecting over TCP (lib ioredis)

- On Cloudflare Workers or edge runtimes without TCP sockets → use a REST-based client (e.g. Upstash) instead — this skill does not cover it
- Credentials/`REDIS_URL` are managed via `/follow-secret-manager` — never hardcode
- First-time setup → `workflows/setup-ioredis/SKILL.md`; perf tuning → `workflows/optimize-pool/SKILL.md`

- Latest: `ioredis@6.0.0` (verified 2026-09-13) — v6 major (2026-07-31): requires Node ≥20, uses RESP3 by default (`HELLO 3` with auto-fallback to RESP2 when the server doesn't support it); set `protocol: 2` to keep the v5 wire protocol and `replyStyle: "resp3"` to receive RESP3 reply shapes (default `"legacy"` keeps the old format)
- References: [apis](references/apis.md) 
## Execute

### Workflows

| Topic | Workflow |-------|----------| Setup | `workflows/setup-ioredis/SKILL.md` — install, cluster/sentinel options | Optimize | `workflows/optimize-pool/SKILL.md` — pipelining, connection reuse 
### 1. Setup And Usage

> Goal: use correctly per the official docs

1. Create the client with `new Redis(url)` or `Redis.Cluster` for a cluster — in v6, put Cluster per-node options under `redisOptions`
1. Use `pipeline()`/`multi()` for batch commands
1. Use separate connections for pub/sub (RESP2 subscriber mode blocks other commands; in v6 a RESP3 connection can run regular commands while subscribed)
1. Manage the reconnect strategy with `retryStrategy` and `lazyConnect` per use case
1. In v6 with `enableOfflineQueue: false`, issue commands (including `subscribe()`) from the `ready` listener instead of `connect`, because they may reject before the client is ready

### 2. Verify

> Goal: verify correct usage

1. Run `/run-verify` for lint, typecheck
2. Run `/run-test` if related tests exist
3. Check the latest official docs before using an uncertain API (lib ioredis)

## Rules

- Don't share a subscriber connection with the command client
- Set `maxRetriesPerRequest` appropriately (null for BullMQ)
- Use the TLS option when connecting over public networks
- On Cloudflare Workers use REST/Upstash instead (ioredis requires TCP)

- Use `/follow-secret-manager` if credentials management is needed
- Use `/run-verify` if needed
- Use `/run-test` if needed
- See best-practices/ for recommended patterns and pitfalls

## Expected Outcome

- The library is used correctly per best practices (lib ioredis)
- No known security/performance pitfalls (lib ioredis)
- Lint, typecheck, tests pass
