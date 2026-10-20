---
name: infra-cloudflare-workers
description: Use when shipping Cloudflare Workers via Wrangler — wrangler.toml, bindings (KV, R2, D1, Queues, Durable Objects), local dev, deployment, observability.
metadata:
  added: 2026-05-18
  last_reviewed: 2026-05-18
  type: domain
  status: active
  invokes_shell: false
  shell_reviewed: "valksor 2026-05-18"
  related: [typescript, node-essentials, security, observability-essentials, ci-github-actions]
---

# Infra Cloudflare Workers

**Iron Law: every binding declared in `wrangler.toml`, every secret via `wrangler secret put`, never in code. `compatibility_date` is pinned and bumped intentionally — it controls runtime behavior, not just node-compat. Use `wrangler tail` + Logpush; without them you have no observability.**

**Versions:** Current Wrangler `4.x` · `workerd` runtime tracked via `compatibility_date` (use latest at deploy time, e.g. `2026-05-15`) — _Wrangler 4 is the supported CLI as of 2026; Wrangler 3 still works but new features land on 4. `compatibility_date` is the real version pin — runtime behavior changes are gated by it, not by Wrangler version._

## What a Worker is (vs Pages, vs Functions)

| Thing              | When                                                                        |
| ------------------ | --------------------------------------------------------------------------- |
| **Worker**         | script run on every request to a route — full programmatic control          |
| **Pages**          | static site host with optional **Pages Functions** (file-based API routes)  |
| **Durable Object** | stateful Worker — one instance per ID, single-threaded, in-memory + storage |

Pages for static site + a few API routes (Next, Astro, SvelteKit). Workers for API-first.

## wrangler.toml

```toml
name = "myapp-api"
main = "src/index.ts"
compatibility_date = "2026-05-15"                # pin; bump intentionally
compatibility_flags = ["nodejs_compat"]          # node:buffer / node:crypto / etc.
# account_id via CLOUDFLARE_ACCOUNT_ID env or `wrangler login`

[vars]                                            # plaintext, non-secret
ENVIRONMENT = "development"
API_BASE = "https://api.example.com"

[[kv_namespaces]]
binding = "CACHE"; id = "abcdef..."; preview_id = "00000..."

[[r2_buckets]]
binding = "ASSETS"; bucket_name = "myapp-assets-prod"; preview_bucket_name = "myapp-assets-dev"

[[d1_databases]]
binding = "DB"; database_name = "myapp-prod"; database_id = "xxxx-..."

[[queues.producers]]
binding = "JOBS"; queue = "myapp-jobs-prod"

[[queues.consumers]]
queue = "myapp-jobs-prod"
max_batch_size = 10; max_batch_timeout = 30; max_retries = 3
dead_letter_queue = "myapp-jobs-dlq"

[[durable_objects.bindings]]
name = "SESSION"; class_name = "Session"; script_name = "myapp-api"

[[migrations]]
tag = "v1"; new_classes = ["Session"]             # DO classes MUST be declared in migrations

[[hyperdrive]]
binding = "PG"; id = "yyyy-..."                   # PG pooler at the edge

[[services]]
binding = "AUTH"; service = "auth-worker"         # Worker→Worker without DNS

[env.production]
vars = { ENVIRONMENT = "production" }
routes = [{ pattern = "api.example.com/*", zone_name = "example.com" }]

[env.staging]
vars = { ENVIRONMENT = "staging" }
routes = [{ pattern = "api.staging.example.com/*", zone_name = "example.com" }]

[triggers]
crons = ["0 */6 * * *"]
```

`wrangler deploy --env production` reads `[env.production]` over the base config.

## Bindings — pick the right primitive

| Binding             | Consistency                   | Use for                                                |
| ------------------- | ----------------------------- | ------------------------------------------------------ |
| **KV**              | eventual (~60s globally)      | session lookup, feature flags, configs — cache, not DB |
| **R2**              | strong                        | assets, uploads, media; S3-compatible, no egress fees  |
| **D1**              | strong (single-region writes) | small relational data (< a few GB)                     |
| **Queues**          | at-least-once                 | async jobs, fan-out, decoupling                        |
| **Durable Objects** | strong, in-region             | per-entity state, WS coordination, rate limiters       |
| **Service binding** | RPC                           | Worker → Worker without DNS hop                        |
| **Hyperdrive**      | normalized over PG            | reuse existing Postgres without conn-storm             |
| **Vectorize**       | append-only                   | RAG, semantic search                                   |

KV is **eventually** consistent — same-region write→read within 60s may return stale. For read-after-write use D1 or a DO. **Never put session-invalidation or permission-revocation in KV alone** — a revoked session stays valid for up to 60s. Authoritative state for "is this token still valid" / "was this user banned" belongs in D1 or a Durable Object; KV is fine as a read-through cache in front of it.

## Secrets vs vars

```bash
wrangler secret put SENTRY_DSN --env production
wrangler secret put STRIPE_SECRET_KEY --env production
wrangler secret list --env production
```

Both read as `env.X` in code. Difference is at-rest: secrets encrypted in CF's vault, vars plaintext on the dashboard. **Never put a key under `[vars]`** — leaks to deploy logs and anyone with account access.

**Bindings have no per-request access control.** Once a Worker is invoked, _any_ code path inside it can read/write `env.KV`, `env.R2`, `env.DB`. Authenticate and authorize the request in your handler BEFORE touching bindings — never assume "the binding is private" implies "only authorized callers reach it."

## Local dev — Miniflare via `wrangler dev`

```bash
wrangler dev                                      # local; preview KV/R2 IDs
wrangler dev --remote                             # real CF edge (prod-shaped infra)
wrangler dev --env staging
```

`--local` (default) runs `workerd` + Miniflare-backed bindings in `.wrangler/state/`. Use `--remote` sparingly — burns through prod quotas.

## Deploy flow

```bash
wrangler deploy --env staging
wrangler deploy --env production
wrangler versions list
wrangler versions deploy <id> --percentage 10     # gradual rollout (paid only)
wrangler rollback                                  # revert
```

Gradual rollouts require a Paid plan. Without them, every `deploy` is 100% cutover — small changes, deploy often, watch `wrangler tail`.

## Observability

```bash
wrangler tail --env production                   # live log stream
wrangler tail --status error --sampling-rate 0.1
```

- **Workers Analytics Engine** — `env.MY_ANALYTICS.writeDataPoint(...)`; SQL API / Grafana CF plugin.
- **Logpush** — request logs to R2 / S3 / GCS / Sentry / Datadog (per-zone in dash).
- **OTel** — `@microlabs/otel-cf-workers` + standard OTLP exporter. See `Skill(observability-opentelemetry)`.
- **Sentry** — `@sentry/cloudflare`; wrap handlers with `withSentry`. See `Skill(observability-sentry)`.

## Routes vs custom domains

- **Routes** — wildcard pattern (`api.example.com/*`) on a CF zone. Flexible, multiple Workers per zone.
- **Custom domains** — Worker IS the origin; CF auto-creates DNS. Cleaner, one Worker per FQDN.

Default to routes. Custom domains for "Worker is the entire backend".

## Cron triggers

```typescript
export default {
  async fetch(request, env, ctx): Promise<Response> { ... },
  async scheduled(event, env, ctx): Promise<void> {
    await env.JOBS.send({ task: "nightly-rollup", at: event.scheduledTime });
  },
};
```

No request context in `scheduled`. Test: `wrangler dev --test-scheduled` → hit `http://localhost:8787/__scheduled`. Cron has separate CPU budget (30s free, 15min paid).

## Limits to design around

| Limit                     | Free    | Paid                                                   |
| ------------------------- | ------- | ------------------------------------------------------ |
| CPU time / request        | 10ms    | 30s (50ms default; bump via `[limits] cpu_ms = 30000`) |
| Wall clock / request      | 30s     | 30s fetch / 15min scheduled                            |
| Script size (compressed)  | 1 MB    | 10 MB                                                  |
| Subrequests / req         | 50      | 1000                                                   |
| Memory / isolate          | 128 MB  | 128 MB                                                 |
| Request body              | 100 MB  | 500 MB (larger: stream to R2)                          |
| KV value                  | 25 MB   | 25 MB                                                  |
| `eval` / `Function()`     | blocked | blocked (static analysis only)                         |
| `setTimeout` between reqs | blocked | blocked (use Cron / DO)                                |

`compatibility_flags = ["nodejs_compat"]` enables `node:buffer`/`node:crypto`/`node:stream`, NOT `fs`/`net`/`child_process`.

## When NOT to use Workers

- Long-running jobs (>30s scheduled, >5min CPU) — use a VM / Cloud Run / Fargate.
- Heavy native deps (`sharp`, ffmpeg, headless Chromium) — use containers.
- Full Node compat needs (raw TCP beyond `connect()`, fs writes, gRPC) — Node runtime.
- Persistent in-process state across requests — isolates recycle; use KV / DO.

## Anti-patterns

- Secrets in `[vars]` or hardcoded in `src/` — leaks to dashboard + deploy logs.
- Bumping `compatibility_date` without reading the changelog — runtime semantics shift silently. KV write→read in the same region within ~60s may return stale; use a DO for read-after-write.
- One mega DO for "all users" — single-threaded, serializes everything. Shard by entity.
- `wrangler dev --remote` constantly — burns prod quotas. Default `--local`.
- Logging request bodies/headers unredacted — `wrangler tail` shows them.
- Bundling 5+ MB packages (`aws-sdk`) — exceeds script size; use lighter clients.
- Missing `event.waitUntil(...)` for fire-and-forget — isolate may terminate the promise.

## Red flags

| Thought                                | Reality                                                                                                                       |
| -------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------- |
| "KV is fast storage"                   | KV is eventually-consistent cache. Write→read in the same region within 60s may return stale.                                 |
| "We'll just bump `compatibility_date`" | Some bumps change request body handling, header casing, error formats. Read the diff.                                         |
| "Durable Objects scale infinitely"     | Per-DO is single-threaded; a hot DO is a bottleneck. Shard by entity ID.                                                      |
| "Cron handlers are reliable timers"    | They fire at least once per minute they're scheduled, may run multiple times across a brief window. Make handlers idempotent. |

## Hand-off

For the TS/Node side of the Worker (handlers, fetch API patterns): `Skill(typescript)`, `Skill(node-essentials)`. For OTel instrumentation inside the Worker: `Skill(observability-opentelemetry)`. For Sentry-on-Workers: `Skill(observability-sentry)`. For CI that runs `wrangler deploy --env production` on tag push: `Skill(ci-github-actions)`. For the secret-management posture and KMS alternatives: `Skill(security)`.
