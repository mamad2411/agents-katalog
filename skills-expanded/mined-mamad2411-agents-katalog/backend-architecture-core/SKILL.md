---
name: backend-architecture-core
description: "Shared reference for the backend-architecture cluster: the dependency-inversion boundary (domain → ports → adapters), the layering contract, REST/transport conventions, and the runtime/framework matrix. USE WHEN drawing a module boundary, designing an API, wiring an integration, or planning a deploy — the interlocking rules every backend spoke shares."
cluster: backend-architecture
version: 1.0.0
---

# Backend Architecture Core

Shared model for the `backend-architecture` cluster. The architecture, API, integration, and
deploy spokes all depend on these interlocking concepts — keep them consistent here so no spoke
contradicts another.

## 1. The decision this cluster turns on: dependencies point inward

Every spoke is an application of one rule — **the domain depends on abstractions, never on
infrastructure**. Business logic is pure; frameworks, drivers, and HTTP clients live at the edges
behind ports. This is the ports-and-adapters (hexagonal) boundary, and it is what makes a backend
testable, framework-swappable, and resistant to rot.

```
            (driving / inbound)                       (driven / outbound)
HTTP · CLI · queue · cron ──> [Port] ──> Domain + Use cases ──> [Port] ──> DB · API · bus · cache
        adapters                          (no framework imports)            adapters
```

- **Domain / use case** — pure business rules and orchestration; imports nothing from the framework, ORM, or transport. → `hexagonal-architecture`
- **Port** — an interface the core owns and depends on (e.g. `UserRepository`, `PaymentGateway`).
- **Adapter** — a concrete implementation at the edge (Express handler, NestJS controller, Prisma repo, an outbound API connector). Adapters depend on the core; the core never depends on them.

**Rule:** if removing a library would force you to rewrite a use case, the dependency is pointing
the wrong way — put a port between them.

## 2. The layering contract

| Layer | Owns | Depends on | Spoke |
|---|---|---|---|
| Transport | HTTP/MCP/CLI shape, (de)serialization, status codes | Application | `api-design`, `mcp-server-patterns`, `nestjs-patterns` |
| Application | use-case orchestration, transactions, validation | Domain (via ports) | `hexagonal-architecture`, `backend-patterns` |
| Domain | entities, business invariants | nothing external | `hexagonal-architecture` |
| Adapter (driven) | DB access, outbound calls, caching, jobs | Domain ports | `backend-patterns`, `api-connector-builder` |

Validate at the transport boundary; never trust an inbound request. Keep controllers thin —
they translate transport ⇄ use case, nothing more.

This cluster owns the app-layer view of data — the repository adapter, transactions via ports, the
API over it. A pure DB query, indexing, migration, or engine-tuning ask belongs to `databases-data`.

## 3. API & transport conventions

- **REST**: nouns + plurals for resources, correct status codes, cursor/offset pagination,
  consistent error envelope, explicit versioning, rate limiting on public surfaces. → `api-design`
- **Outbound integrations**: match the host repo's connector layout, config schema, auth model,
  error handling, and registration wiring — one pattern, not two. → `api-connector-builder`
- **MCP**: tools/resources/prompts with Zod-validated inputs; choose stdio vs Streamable HTTP by
  deployment. → `mcp-server-patterns`
- Treat a new public contract or persisted schema as a breaking-change candidate; record the call
  with `architecture-decision-records`.

## 4. Runtime / framework matrix

| Surface | Default | Spoke |
|---|---|---|
| Node service / API routes | Node + TypeScript (Express / Next.js routes) | `backend-patterns` |
| Structured TS backend | NestJS (modules, providers, guards, interceptors) | `nestjs-patterns` |
| Multi-language domain core | TS / Java / Kotlin / Go behind ports | `hexagonal-architecture` |
| AI tool server | MCP TypeScript SDK | `mcp-server-patterns` |
| Release | Docker + CI/CD (blue-green / canary / rolling), health checks, rollback | `deployment-patterns` |

SDK and framework APIs evolve — verify current method names against official docs/Context7 rather
than trusting memory.

## 5. Shared guardrails

- **Dependencies point inward**: domain imports no framework, driver, or HTTP client; edges go behind ports.
- Validate all inputs at the transport boundary; controllers stay thin.
- Match the existing repo pattern; don't introduce a second architecture for one more feature.
- State every contract change (public endpoint, persisted schema, outbound integration) explicitly.
- Capture non-obvious architectural trade-offs as ADRs so the "why" outlives the PR.
- Confirm health checks, rollback path, and env config **before** a production deploy.
