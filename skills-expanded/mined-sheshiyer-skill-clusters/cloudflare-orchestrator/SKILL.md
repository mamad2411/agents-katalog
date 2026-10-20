---
name: cloudflare-orchestrator
description: "Route a Cloudflare task to the right spoke among the platform specialists — Workers and Pages compute, the wrangler CLI and binding/config model, storage (KV, R2, D1), Durable Objects for stateful coordination, the Agents SDK and Sandbox SDK, transactional email, and deploy/auth debugging. USE WHEN a user is building, configuring, or shipping something on Cloudflare's edge but hasn't named the specific service."
cluster: cloudflare
version: 1.0.0
---

# Cloudflare Orchestrator

The single entry skill for Cloudflare edge work. It locates the task on the **compute ×
primitive** map and delegates to one of the specialist spokes. The cross-cutting model every
Cloudflare app shares — a Worker (or Pages Function) reaching stateful primitives **only through
bindings** declared in `wrangler.jsonc` under a pinned `compatibility_date` — lives in
`cloudflare-core`; read it before adding a binding, choosing a storage primitive, or writing
config.

## Routing map (intent → spoke)

**Deploy & operate (the front door)**
- "Deploy a Worker / MCP server / Pages site", auth/token failures, deploy debugging → `cloudflare`
- Account-level management (deploy + KV + R2 + Pages + DNS/routes via scripts, API token setup) → `cloudflare-manager`

**The CLI & config (everything routes through here)**
- Any `wrangler` command, `wrangler.jsonc`, `compatibility_date`, `wrangler types`, secrets, `wrangler dev/tail/deploy` → `wrangler`  *(binding model in `cloudflare-core`)*

**Write & review Worker code**
- New Worker, code review, anti-patterns (streaming, floating promises, global state, secrets, bindings, observability) → `workers-best-practices`

**Stateful coordination**
- Chat rooms, multiplayer, booking/locking, per-entity state, alarms, WebSockets, SQLite-in-DO, RPC methods → `durable-objects`  *(DO is a binding too — see `cloudflare-core`)*

**Build AI agents**
- Stateful agents, durable workflows, scheduled tasks, MCP servers, chat/voice agents, React `useAgent` hooks, queues/retries/observability → `agents-sdk`

**Run untrusted / arbitrary code**
- Code interpreters, CI/CD sandboxes, AI code execution, interactive dev environments, preview URLs (container-backed) → `sandbox-sdk`

**Email**
- Send transactional email (Workers `send_email` binding or REST API), receive/route email, `onEmail()`/`replyToEmail()`, SPF/DKIM/DMARC, `wrangler email` setup → `cloudflare-email-service`

**Publish & validate static artifacts on R2**
- NotebookLM/portal artifacts on R2: public URLs, MIME types, cache headers, audio/video playback, inventory/visibility claims → `r2-notebooklm-artifact-portal`

## Standard Operating Flow

1. Locate the task: which **compute surface** (Worker / Pages / Durable Object / Agent / Sandbox) and which **primitive** (KV / R2 / D1 / queue / email) it touches.
2. If it adds or changes a **binding, storage choice, or `compatibility_date`**, pull the model from `cloudflare-core` first — bindings, config, and the deploy step are interlocking, not independent.
3. Almost every change ends at the CLI: route config/deploy/secret work through `wrangler`, and verify deploys via `cloudflare` (auth-token gotchas live there).
4. Delegate to the spoke(s). Multi-step asks fan out in build order (e.g. "stateful chat agent" → `agents-sdk` + `durable-objects` + `wrangler` binding + `cloudflare` deploy).
5. Return: chosen spoke(s), the bindings/config implied, the `compatibility_date` to set, and the next action.

## Guardrails

See `cloudflare-core`. In short: **declare every dependency as a binding** — never hardcode
secrets or account IDs in code (`wrangler secret put`); **pin `compatibility_date`** to a recent
date and regenerate types after config changes (`wrangler types`); pick the **right primitive**
(KV = read-heavy cache, R2 = large objects/no egress, D1 = relational, Durable Object =
strongly-consistent per-entity state); and **prefer retrieval over pre-trained knowledge** — these
APIs move fast, so fetch the current Cloudflare docs the spokes link before relying on a signature.
The auth-token trap is real: env tokens often lack Pages permissions, so unset them for OAuth
(`cloudflare`).

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as
skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named
above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
