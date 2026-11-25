---
name: architecture
description: >-
  Guides system design decisions using docs/ARCHITECTURE.md and related docs.
  Use for cross-service flows, module boundaries, deployment, or when adding
  features that touch frontend, API, database, or external integrations.
---

# Architecture

## Read first

- `docs/ARCHITECTURE.md` — services, modules, core flows
- `docs/DATA_MODEL.md` — entities and relationships
- `docs/REQUIREMENTS.md` — scope boundaries
- `.agents/skills/project-context/SKILL.md` — layout and stack

## Design goals

1. Keep the primary data store as the source of truth for domain state.
2. Prefer configuration and data over hardcoding product content in UI or services.
3. Deliver user-visible value early; avoid speculative platforms.
4. Prefer simple deployment (e.g. Docker Compose) before complex orchestration.
5. Stateless services where practical; config via environment variables.

## Service boundaries

Document concrete paths in `project-context`. Typical monorepo split:

| Layer         | Responsibility                                            |
| ------------- | --------------------------------------------------------- |
| Frontend app  | UI, forms, results, admin UI                              |
| Backend app   | REST (or RPC), domain logic, auth, aggregations           |
| Database      | Durable domain data                                       |
| External APIs | Narrow integrations (email, AI narrative, payments, etc.) |

## When proposing changes

- Prefer extending existing modules over new microservices.
- Keep domain rules documented in code and the relevant `docs/` specs.
- Any new external dependency needs env vars in `.env.example` and README notes.
- Record significant choices in `docs/DECISIONS.md` and `docs/adrs/` when warranted.
