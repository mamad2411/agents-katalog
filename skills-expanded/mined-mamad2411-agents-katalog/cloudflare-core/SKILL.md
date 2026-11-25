---
name: cloudflare-core
description: "Shared reference for the Cloudflare cluster: the edge-compute + binding model every Worker turns on, wrangler.jsonc conventions, compatibility_date, the storage-primitive decision matrix (KV vs R2 vs D1 vs Durable Objects), secrets, and the auth-token gotcha. USE WHEN adding a binding, choosing a storage primitive, writing wrangler config, or debugging a Cloudflare deploy — the interlocking rules every Cloudflare spoke shares."
cluster: cloudflare
version: 1.0.0
---

# Cloudflare Core

Shared model for the `cloudflare` cluster. The compute, storage, and deploy spokes all depend on
these interlocking concepts — keep them consistent here so no spoke contradicts another.

## 1. The compute + binding model (Cloudflare's defining shape)

Everything you ship is **compute at the edge** that reaches the rest of the platform **only through
bindings**. There is no ambient global state and no import of a database client — a resource exists
to your code only if it is declared as a binding:

```
Request ──> Worker / Pages Function ──binding──> KV · R2 · D1 · Durable Object · Queue · AI · send_email · Service
                                       (declared in wrangler.jsonc, injected on env)
```

- **Worker** — the unit of compute; a `fetch`/`scheduled`/`email`/`queue` handler running on every edge node. New code & reviews → `workers-best-practices`; deploys → `cloudflare`.
- **Pages / Pages Functions** — static assets + file-routed Workers. Deploy → `cloudflare`.
- **Binding** — a named capability on the `env` object, declared in `wrangler.jsonc`. This is the *only* way compute touches a primitive; adding one is a config change, not just code. CLI/config → `wrangler`.
- **Durable Object** — also reached via a binding, but it *is* compute + storage: a single-threaded, strongly-consistent actor per id. → `durable-objects`.

**Rule:** declare every dependency as a binding; never hardcode secrets, account IDs, or
endpoints that a binding or secret should carry.

## 2. wrangler.jsonc & compatibility_date (the config contract)

- Prefer **`wrangler.jsonc`** over `wrangler.toml` — newer features are JSON-only. → `wrangler`
- **`compatibility_date`** pins the runtime's behavior; set a recent date (within ~30 days) and add `compatibility_flags` only as needed. Changing it can change runtime semantics — treat it as a real decision.
- After any config/binding change, **regenerate types**: `wrangler types` (keeps `env` typed).
- `wrangler dev` for local, `wrangler deploy` to ship, `wrangler tail` for live logs.

## 3. Secrets & auth (where deploys actually break)

- Runtime secrets → `wrangler secret put NAME` (never commit `.env`; never inline a token in code).
- **The auth-token gotcha:** API tokens in the environment frequently lack **Pages** permissions and silently override OAuth. For Pages — and often Workers — **unset** `CF_API_TOKEN`/`CLOUDFLARE_API_TOKEN` so wrangler's OAuth login is used. This single trap causes most "works locally, 403 on deploy" failures. → `cloudflare`
- Account-scoped management with an explicit API token (KV/R2/Pages/DNS via scripts) → `cloudflare-manager`.

## 4. Storage-primitive decision matrix (pick one per use)

| Primitive | Consistency | Best for | Avoid for | Spoke |
|---|---|---|---|---|
| **KV** | Eventual (~60s global) | Read-heavy cache, config, feature flags | Frequent writes, read-after-write | `wrangler` (bind), `cloudflare-manager` |
| **R2** | Strong per-object | Large/binary objects, media, no egress fees | Querying, relational data | `wrangler`, `r2-notebooklm-artifact-portal` (public serving) |
| **D1** | Strong (SQLite) | Relational data, joins, transactions | Massive write throughput, huge blobs | `wrangler` |
| **Durable Object** | Strong, single-writer | Per-entity state, coordination, locks, WebSockets, alarms | Bulk analytics, sharable read cache | `durable-objects` |
| **Queues** | At-least-once | Async/decoupled work, retries, batching | Synchronous request/response | `agents-sdk`, `wrangler` |

Rule of thumb: **KV = read-heavy cache, R2 = objects, D1 = relational, Durable Object =
strongly-consistent per-entity state.** Reach for a DO only when you need a single coordinator;
it is the most expensive default.

## 5. Higher-level SDKs (built on the same bindings)

- **Agents SDK** — stateful AI agents, durable workflows, scheduled tasks, MCP servers, chat/voice, React hooks. Sits on Durable Objects + Workers under the hood. → `agents-sdk`
- **Sandbox SDK** — container-backed isolated execution for untrusted/arbitrary code, code interpreters, CI/CD, preview URLs (requires Docker locally; a `containers` binding). → `sandbox-sdk`
- **Email** — send via the Workers `send_email` binding or REST API; receive/route via Email Routing and `onEmail()`. → `cloudflare-email-service`

## 6. Retrieval over pre-training (a cluster-wide convention)

These APIs, flags, and config fields change fast. The spokes deliberately **bias toward fetching
the current Cloudflare docs** rather than trusting baked-in knowledge — do the same before relying
on a signature, binding shape, or wrangler flag. Authoritative sources: the spoke's linked
`developers.cloudflare.com` page, `@cloudflare/workers-types`, and
`node_modules/wrangler/config-schema.json`.

## 7. Shared guardrails

- **Bindings, not hardcoding**: every external dependency is a declared binding; secrets via `wrangler secret put`.
- **Pin `compatibility_date`** (recent) and run `wrangler types` after config changes.
- **Right primitive for the access pattern** (matrix above); a Durable Object is not a default cache.
- **State every binding/config change** — a new binding, scope, or secret is an infra change worth naming.
- **Unset env API tokens for Pages/OAuth deploys** — the token trap is the #1 deploy failure.
- **Retrieve current docs** before trusting an API signature; prefer `wrangler` over hand-rolled API calls.
- **Workers vs other edges**: this cluster is Cloudflare-specific; the binding model and `compatibility_date` are Cloudflare conventions, not portable to generic Node/serverless.
