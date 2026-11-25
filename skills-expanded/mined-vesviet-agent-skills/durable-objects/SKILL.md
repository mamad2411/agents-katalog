---
name: durable-objects
description: Create and review Cloudflare Durable Objects. Use when building stateful coordination (chat rooms, multiplayer games, booking systems), implementing RPC methods, SQLite storage, alarms, WebSockets, or reviewing DO code for best practices. Covers Workers integration, wrangler config, and testing with Vitest. Biases towards retrieval from Cloudflare docs over pre-trained knowledge.
allowed-tools: [read_file, write_file, edit_file, create_file, search_code, run_tests, run_linter, run_build, wrangler_deploy, execute_command]
---

# Durable Objects

Build stateful, coordinated applications on Cloudflare's edge using Durable Objects backed by embedded SQLite.

## Retrieval Sources

Your knowledge of Durable Objects APIs and configuration may be outdated. **Prefer retrieval over pre-training** for any Durable Objects task.

| Resource | URL |
| :--- | :--- |
| Docs | `https://developers.cloudflare.com/durable-objects/` |
| API Reference | `https://developers.cloudflare.com/durable-objects/api/` |
| Best Practices | `https://developers.cloudflare.com/durable-objects/best-practices/` |
| Examples | `https://developers.cloudflare.com/durable-objects/examples/` |

## When to Use

- creating new Durable Object classes for stateful coordination
- implementing RPC methods, alarms, or WebSocket handlers
- reviewing existing DO code for SQLite and concurrency best practices
- configuring `wrangler.jsonc` for DO bindings and `new_sqlite_classes` migrations
- writing tests with `@cloudflare/vitest-pool-workers`
- designing sharding strategies and parent-child entity hierarchies

## Core Principles

### Use Durable Objects For

| Need | Example |
| :--- | :--- |
| Coordination | Chat rooms, multiplayer games, collaborative documents |
| Strong consistency | Inventory reservation, booking systems, turn-based games |
| Per-entity storage | Multi-tenant SaaS, per-user state, Agent memory |
| Persistent connections | WebSockets, real-time push, streaming LLM tokens |
| Scheduled work per entity | Subscription renewals, inactivity timeouts, alarms |

### Do NOT Use For

- Stateless request handling (use plain Workers)
- Maximum global read distribution needs (use KV or Cache API)
- High fan-out independent queries across millions of entities

## Core Rules

1. **Model around coordination atoms** — One DO per chat room/game/user entity, never one global DO.
2. **Use `getByName()` for deterministic routing** — Same entity ID maps deterministically to the same DO instance.
3. **Use SQLite storage engine** — Configure `new_sqlite_classes` in `migrations` and use `this.ctx.storage.sql.exec(...)`.
4. **Initialize in constructor** — Use `blockConcurrencyWhile()` only in constructor for schema setup; never in request handlers.
5. **Use RPC direct methods** — Expose actions via TypeScript class methods; avoid legacy `fetch()` handlers.
6. **Persist first, cache second** — Always commit state to SQLite before updating in-memory caches.
7. **One alarm per DO** — Calling `setAlarm()` replaces any existing alarm; design a schedule table in SQLite for multiple deadlines.
8. **Enforce dual observability** — Ensure `wrangler.jsonc` includes `"observability": { "enabled": true, "traces": { "enabled": true } }`.

## Anti-Patterns (NEVER)

- Single global DO handling all application requests (bottleneck).
- Invoking `blockConcurrencyWhile()` on every request handler (kills throughput).
- Storing critical transactional state only in memory (lost on isolate eviction/crash).
- Using `await` between related storage writes without `transactionSync()` (breaks atomicity).
- Holding `blockConcurrencyWhile()` across external network `fetch()` calls.

## Suggested Process

1. Model the coordinated entity as a distinct class extending `DurableObject`.
2. Configure bindings and `new_sqlite_classes` storage migration in `wrangler.jsonc`.
3. Establish initial table schema synchronously inside the constructor wrapped in `blockConcurrencyWhile()`.
4. Expose actions using RPC direct methods instead of raw `fetch()` handlers.
5. Run `wrangler types` to generate TypeScript interfaces for the DO stub.
6. Create Vitest suites using `@cloudflare/vitest-pool-workers` to verify state transitions and alarms.

## Checklist

- [ ] Durable Object class is defined, exported, and extends `DurableObject`.
- [ ] Bindings and `new_sqlite_classes` migration are declared in `wrangler.jsonc`.
- [ ] Schema initialization uses `blockConcurrencyWhile()` inside the constructor only.
- [ ] Object logic leverages direct RPC methods with typed return values.
- [ ] Unit and integration tests are written using `@cloudflare/vitest-pool-workers`.
- [ ] Outbound connections verified: DOs stay alive for active outbound connections up to 15 minutes.
- [ ] SQLite storage monitored: 10 GB per-DO limit enforced; `VACUUM` run after bulk deletions.

## Output Contracts

When this skill is invoked as part of a coordinated multi-role delivery, emit:

- **`contracts/schemas/edge-deployment-spec.json`** — capture the DO bindings, SQLite migrations, RPC interface signatures, and rollback strategy. Set `produced_by_role` to `cloudflare-engineer`.

## Failure Modes

- **Single global DO**: a single DO handles all requests, creating a hot partition. Mitigation: model around coordination atoms; one DO per entity.
- **`blockConcurrencyWhile` on request path**: schema setup rerun on every request halts concurrent handlers. Mitigation: use `blockConcurrencyWhile` only in constructor.
- **In-memory only state**: critical state lives only in memory and evaporates upon isolate eviction. Mitigation: persist first to SQLite, then update cache.
- **Alarm overwrite**: a DO sets multiple alarms via parallel `setAlarm()` calls. Mitigation: maintain a scheduled queue in SQLite and set the alarm for the earliest item.
- **Missing migration tag**: adding a DO without `new_sqlite_classes` in `migrations` causes runtime binding errors. Mitigation: register migration in `wrangler.jsonc`.

## Security Guardrails (OWASP ASI)

- **ASI03 Identity & Privilege Abuse**: DO bindings must follow least-privilege scoping; reject DO classes that expose state mutations to unauthenticated callers.
- **ASI04 Supply Chain**: `@cloudflare/vitest-pool-workers` and `cloudflare:workers` versions must be verified against package manifests.
- **ASI05 RCE Guard**: always parameterize SQL queries: `ctx.storage.sql.exec("SELECT * FROM tbl WHERE id = ?", id)`; never concatenate raw input.
- **ASI07 Inter-Agent Communication**: emit structured edge deployment specifications when coordinating releases across roles.
- **ASI09 Human-Agent Trust Exploitation**: do not present a DO architecture as horizontally scalable without validating entity atomicity.

## Related Skills

- **wrangler**: Manage deployment environments, bindings, and DO migrations.
- **agents-sdk**: Build stateful AI agents and durable workflows atop Durable Objects SQLite.
- **workers-best-practices**: Review async execution patterns, memory hygiene, and observability.
- **debug-workers-edge**: Troubleshoot execution at the edge and inspect live tail logs.
