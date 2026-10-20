---
name: backend-architecture-orchestrator
description: "Route a backend task to the right skill among 8 server-side specialists — architecture boundaries (hexagonal/ports-and-adapters), REST API design, HTTP connector building, NestJS structure, MCP servers, deployment/CI-CD, and decision records. USE WHEN a user is designing, building, integrating, or shipping a backend service but hasn't named the specific concern."
cluster: backend-architecture
version: 1.0.0
---

# Backend Architecture Orchestrator

The single entry skill for server-side work. It locates the task on the **layer × concern**
map and delegates to one of 8 specialist spokes. The cross-cutting model every backend shares
— the dependency-inversion boundary (domain → ports → adapters), the layering contract, the
API/transport conventions, and the runtime/tooling matrix — lives in `backend-architecture-core`;
read it before drawing a module boundary, designing an endpoint, or wiring an integration.

## Routing map (intent → spoke)

**Shape the architecture**
- "How should I structure this service?" / boundaries, testability, decoupling → `hexagonal-architecture`  *(model in `backend-architecture-core`)*
- General server-side patterns — repository/service/controller layers, caching, background jobs, query optimization → `backend-patterns`
- Framework-specific structure (NestJS modules, providers, guards, interceptors, DTO validation) → `nestjs-patterns`

**Design the API surface**
- REST contracts — resource naming, status codes, pagination, filtering, versioning, error shapes, rate limiting → `api-design`
- Add an outbound integration / provider that matches the repo's existing pattern → `api-connector-builder`
- Expose tools/resources/prompts to an AI assistant (Model Context Protocol) → `mcp-server-patterns`

**Ship & remember why**
- Deploy, containerize, CI/CD, health checks, rollback, production readiness → `deployment-patterns`
- Record an architectural decision (context, alternatives, rationale) → `architecture-decision-records`

## Sibling clusters

- A pure DB query, indexing, migration, or engine-tuning ask → `databases-data`. This cluster owns app-layer data patterns (repository, transactions via ports, API design over the data), not DB engine internals.

## Standard Operating Flow

1. Locate the task: which layer (domain → application → adapter → transport → deploy) and which concern.
2. If it touches **boundaries, the layering contract, or transport conventions**, pull the model from `backend-architecture-core` first — these are interlocking, not independent.
3. Delegate to the spoke(s). Multi-step asks fan out in layer order (e.g. "build and ship a new integration" → `hexagonal-architecture` (port) → `api-connector-builder` (adapter) → `deployment-patterns`).
4. When a non-obvious trade-off is settled along the way, capture it via `architecture-decision-records`.
5. Return: chosen spoke(s), the boundary/contract changes implied, the deployment surface touched, and the next action.

## Guardrails

See `backend-architecture-core`. In short: **dependencies point inward** — domain logic never
imports a framework, a driver, or an HTTP client; those live behind ports. Match the host repo's
existing pattern instead of inventing a second architecture. Validate every input at the
transport boundary; treat any new public-API contract, persisted schema, or outbound integration
as a deliberate change worth stating. The cluster's value is keeping business rules independent
of I/O — don't quietly leak infrastructure into the core.

## Loading spokes on demand

To keep CLI startup context lean, this cluster's spokes are **not** separately registered as skills — only this orchestrator and its `*-core` are enumerated. When you route to a spoke named above, **load it on demand** by reading its file:

`~/.agents/skill-clusters/skills/<spoke-name>/SKILL.md`  (or `skills/<spoke-name>/SKILL.md` inside the skill-clusters repo).
