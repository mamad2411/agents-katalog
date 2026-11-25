---
name: cloudflare-workers
description: "Build on Cloudflare Workers: the isolate runtime and its limits, KV/D1/R2/Durable Objects choice, caching and edge middleware, and local testing with Wrangler."
type: procedural
category: cloud
domain: cloud
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: intermediate
triggers:
  - cloudflare worker limits
  - wrangler dev deploy
  - durable objects vs kv
  - worker cpu time limit
  - edge middleware cloudflare
aliases:
  - workers
keywords:
  - cloudflare
  - workers
  - wrangler
  - kv
  - d1
  - r2
  - durable-objects
  - edge
mcp_servers:
  - cloudflare
  - filesystem
source: custom
enabled: true
---

# Cloudflare Workers

## Purpose

Build on Cloudflare Workers: the isolate runtime and its limits, KV/D1/R2/Durable Objects choice, caching and edge middleware, and local testing with Wrangler.

## When to Use

- Latency or cost demands running logic at the edge.
- A static site needs dynamic behaviour without a full origin.
- The workload needs globally consistent state or object storage.

## When NOT to Use

- The workload needs long-running processes or native binaries.
- Heavy CPU or large memory is required beyond the isolate limits.
- The team cannot operate a global edge deployment.

## Capabilities

- Work within CPU-time, memory and subrequest limits by design.
- Pick the right storage primitive for the access pattern.
- Implement caching and cache invalidation correctly at the edge.
- Write middleware that composes instead of duplicating logic.
- Test locally with Wrangler and deploy with rollback.

## Inputs

- The request path and its latency budget.
- Data access patterns: read-heavy, write-heavy, consistency needs.
- The compatibility date and the runtime APIs you intend to use.

## Workflow

1. Model the request lifecycle and count subrequests and CPU time per request.
2. Choose storage: KV for cache-like reads, D1 for relational, R2 for objects, Durable Objects for coordination.
3. Set a compatibility date explicitly so behaviour does not shift under you.
4. Add caching with correct `Cache-Control` and a purge strategy.
5. Test with `wrangler dev` and the same bindings as production.
6. Deploy with a versioned rollout and a tested rollback.

## Tools

- wrangler
- cloudflare
- miniflare
- vitest

## Examples

- `A Worker has no persistent memory between requests; module-scope caches are best-effort only.`
- `Durable Objects serialise writes per object, which is what makes them right for coordination and wrong for bulk throughput.`

## Safety

- Never put secrets in `wrangler.toml`; use secrets bindings.
- Edge code sees user traffic worldwide; validate and rate-limit at the boundary.

## MCP Requirements

| Server | Transport | Tier | Risk | Required env |
| :--- | :--- | :--- | :--- | :--- |
| `cloudflare` | http | full | medium | — |
| `filesystem` | stdio | core | low | — |

Install the connectors above with `allskills mcp install --harness <harness> --profile full`,
or list the same ids in your harness config. Full detail per server: [`docs/MCP-CATALOG.md`](MCP-CATALOG.md) and [`mcp/registry.json`](../mcp/registry.json).

## Source

All-Skills canonical library (`skills/cloud/cloudflare-workers`). First-party skill, maintained in this repository.

## Notes

- CPU time limit is not wall-clock time; waiting on I/O does not count the same way.
- `wrangler tail` is the fastest way to debug a production-only failure.
- Pairs with: `platform-engineering`, `disaster-recovery`.
