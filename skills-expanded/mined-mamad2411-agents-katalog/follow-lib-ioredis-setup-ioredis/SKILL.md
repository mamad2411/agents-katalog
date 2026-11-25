---
name: follow-lib-ioredis-setup-ioredis
description: Install ioredis and set up the client — standalone, cluster, sentinel options
argument-hint: "[mode-or-url]"
related:
  - follow-lib-ioredis
  - follow-secret-manager
  - learn
  - resolve-errors
---

## Goal

Install `ioredis` and create a Redis client — standalone, Cluster or Sentinel — that actually connects and runs commands — first-time setup only

## Scope

- Use when the project has no ioredis yet (if present → verify only)
- Covers: install, `new Redis()`, `Redis.Cluster`, Sentinel options, retry strategy
- Does not cover perf tuning — do `workflows/optimize-pool/SKILL.md` instead

## Execute

### 1. Check Precondition

> Goal: check the environment before setup

1. Read `package.json` — if `ioredis` is there → skip to verify; check the version (v6 requires Node ≥20, RESP3 default)
2. Identify the Redis topology: standalone, Sentinel or Cluster — if unknown → ask the user or check the infra config
3. Check `REDIS_URL`/credentials — if missing → stop and tell the user; store via `/follow-secret-manager`
4. Check the runtime — ioredis needs TCP; on Cloudflare Workers use REST/Upstash instead

### 2. Install

> Goal: install ioredis as a runtime dependency

1. Run `bun add ioredis` (or the package manager matching the lockfile)
2. Confirm `ioredis` is in `dependencies`

### 3. Create Client

> Goal: a client matching the topology

1. Standalone: `new Redis(process.env.REDIS_URL)` or `new Redis({ host, port, password })`
2. Cluster: `new Redis.Cluster([{ host, port }], { redisOptions: {...} })` — in v6 per-node options go under `redisOptions`
3. Sentinel: `new Redis({ sentinels: [{ host, port }], name: "<master-name>" })` — see official docs for extra options
4. Set `retryStrategy` to fit the use case; `lazyConnect: true` if the connect must be deferred
5. TLS (`tls: {}`) when connecting across a public network
6. Export a single client instance — pub/sub needs a separate connection (the RESP2 subscriber blocks other commands)

### 4. Basic Usage

> Goal: basic commands work

1. `get`/`set`/`del`/`expire` etc. are promise-based — `await redis.set("k", "v")`
2. `pipeline()`/`multi()` for batching (details in `optimize pool`)
3. Set `maxRetriesPerRequest` appropriately — `null` when used with BullMQ
4. v6 + `enableOfflineQueue: false` → send commands from the `ready` listener, not `connect`

### 5. Verify

> Goal: the smoke command really passes

1. `await redis.set("smoke", "1")` then `get` it back — value matches
2. Check `redis.status` is `ready`; for a cluster check that all nodes were discovered
3. Run lint/typecheck — if verify fails → do `/resolve-errors` max 3 rounds, then stop and report; passes → `/suggest-next-action`

## Rules

- Idempotent — if already set up, verify only; never create a duplicate client
- Credentials/URL always from env — never hardcode
- One client instance per role (command, subscriber, publisher on separate connections)
- If the topology/option is unclear → do `/learn-from-web` on the official docs (github.com/redis/ioredis)
- Use `/follow-lib-ioredis` for the overview and best practices

## Expected Outcome

- `ioredis` installed, client matches the topology (standalone/cluster/sentinel)
- Smoke command passes, status `ready`
- Ready for `workflows/optimize-pool/SKILL.md` if perf tuning is needed
