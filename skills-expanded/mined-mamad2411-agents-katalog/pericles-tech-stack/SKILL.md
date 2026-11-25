---
name: pericles-tech-stack
version: 2026.05.1
description: >
  The authoritative technology stack for Pericles. Use this WHENEVER you choose a
  library, queue, datastore, agent framework, or AI provider — and ALWAYS when a PRD,
  old note, or a .cursor/rules file points you at VoltAgent, Kafka, Redis, RabbitMQ,
  Celery, or Neon, because those are stale/generic and the doctrine + package.json
  supersede them. Encodes Mastra + PostgreSQL + OpenAI and the deliberate
  no-Kafka/no-Redis decision, verified against the live dependencies.
doctrine_refs: [§2]
depends_on: [pericles-doctrine]
last_reconciled: 2026-05-28
---

# Pericles Tech Stack (build skill)

The runtime changes slowly; Skills (declarative) change constantly without runtime
deploys. Keep that separation for every dependency choice.

## When to use this skill

Picking any infrastructure dependency; setting up a service; reading a PRD's backend
section; or any time Kafka/Redis/VoltAgent is proposed (including from a `.cursor/rules`
file — see the warning below).

## The stack (verified against backend/package.json)

| Layer | Choice | Evidence |
|---|---|---|
| Language | TypeScript on Node (ESM) | `tsc --noEmit`, `.js` import specifiers |
| Agent runtime | **Mastra** | `@mastra/core ^0.24.8`, `@mastra/evals ^0.14.4`, `@mastra/pg ^0.17.10`, `@mastra/memory ^0.15.13`, `@mastra/loggers ^0.10.19`, `@mastra/libsql ^0.16.4` |
| Persistence | **PostgreSQL** via Prisma | `@prisma/client ^6.12`; `getPostgresStore()` for Mastra storage |
| Queue / KV | **PostgreSQL** | `MessageQueue` + `KeyValueStore` models; `monitoring/queue-client.ts`. **No Kafka. No Redis.** |
| AI provider | **OpenAI** (default) / OpenRouter | keys are org-scoped (`org.<provider>_api_key`), no platform fallback — orgs without a key are skipped; scorer judges ride the same org model+key (`updateScorerJudgeModels`) |
| Realtime | **socket.io ^4.8** | websocket push to the frontend (not Kafka) |
| Auth | JWT + bcrypt + Google OAuth | `jsonwebtoken`, `bcrypt`, `google-auth-library` |
| HTTP | **Express 5** | `express ^5.2` (auth-server) |
| Logging | **Pino** | `pino`, `pino-pretty`; Mastra uses `PinoLogger` |
| Validation | **Zod** | `zod ^3.23` (tool input/output schemas) |
| Frontend | **Next.js + React** | `frontend/`, Google Maps for Atlas |
| Local dev | Docker | `docker-compose` (Postgres, pgAdmin, Mastra 4111) |
| External calls | inline `fetch` + `AbortSignal.timeout(10000)` | grandfathered; new sources via MCP |

`package.json` contains **no** `kafkajs`, `ioredis`, `bull`, `amqplib`, or `voltagent`.

## The no-Kafka / no-Redis rule

Postgres-based queue/KV is the deliberate choice for current scale (§2) — confirmed by
the env comment "PostgreSQL-based queue/KV store - no Redis required". Meet PRD
"streaming / real-time propagation" needs with the Postgres queue + socket.io, not
Kafka. No Kafka/Redis/RabbitMQ without an approved ADR.

## ⚠️ Warning: the `.cursor/rules/` library is generic

`.cursor/rules/` includes standards files for technology **this project does not use**,
including `519-kafka`, `520-redis`, `521-zookeeper`, `524-neon`, `635-kafka-ui`,
`703-voltagent`, `636-langgraph`, plus Elixir/Phoenix and Python rule sets. Their
presence is a generic template, **not** an adoption signal. For stack decisions trust
`CLAUDE.md` + `backend/package.json`. The relevant, in-use rules are the Mastra
(`700-ai/701`, `720`), PostgreSQL (`500-architecture/506`), Prisma (`502`), TypeScript
(`307`), Next.js (`401`), and React (`402`) files.

## Reconciling stale PRD infrastructure notes

| PRD says (stale) | Use instead |
|---|---|
| VoltAgent | Mastra |
| Kafka (streaming) | Postgres queue + socket.io |
| Redis (cache) | `KeyValueStore` (Postgres KV) |
| RabbitMQ / Celery / Bull | `MessageQueue` (Postgres queue) |
| Neon Serverless (specific) | PostgreSQL (provider-agnostic) |
| Pinecone/Weaviate, Neo4j/Neptune | behind MCP, swappable |

PRDs remain authoritative for product behavior; only infra choices are stale.

## Verification

Dependency choices match the table or are backed by an approved ADR; review flags new
`kafkajs`/`ioredis`/`bull`/`amqplib`/`voltagent` imports; `npm run type-check` + `lint`
pass.

## Existing standards (read alongside)

`CLAUDE.md`; `backend/package.json`; `.claude/rules/06-mastra.md`,
`.claude/rules/13-infrastructure.md`; `.cursor/rules/700-ai/701`, `500-architecture/506`.

## Open questions

- `@mastra/libsql` is a dependency — confirm whether it backs local/dev memory vs
  Postgres in prod, so memory-layer skills point at the right store.
- Embedding model for Org Memory (OpenAI `text-embedding-3`?) — confirm in `backend/src`.

## Changelog

- 2026.05.1 — Verified versions against package.json; added socket.io/auth/Express/Pino
  rows; added the .cursor/rules generic-library warning; confirmed no Kafka/Redis deps.
- 2026.05.0 — Initial draft.
