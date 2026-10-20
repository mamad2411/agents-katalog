---
name: multi-agents
metadata:
  author: Mohamed
description: >
  Coordinate multiple agents on cross-cutting software work, especially
  multi-tenant systems, by assigning boundaries, sharing contracts, and
  reviewing integration risks before changes are combined.
---

# Multi-Agents Skill

Use this skill when work is split among agents or when several services/stacks
must implement one consistent architectural boundary.

## Coordination workflow

1. Write a short task contract: outcome, repositories/services in scope,
   constraints, acceptance tests, and files owned by each agent.
2. Assign one agent to define the shared contract and threat model before stack
   agents implement framework-specific details.
3. Give each agent explicit ownership. Avoid parallel edits to the same files.
4. Require agents to report assumptions, changed interfaces, tests, and unresolved
   risks in a consistent handoff.
5. Run an integration review for context propagation, authorization, naming,
   migrations, cache keys, jobs, and error behavior.

## Multi-tenant delegation

For any tenant isolation work, the source of truth is
`Skills/multi-tenant/SKILL.md`. Load its architecture reference first, then
load only the stack reference needed by the assigned agent:

- Express.js, NestJS: `Skills/multi-tenant/references/node-backends.md`
- Vue.js: `Skills/multi-tenant/references/vue-frontend.md`
- Go `net/http`, Gin: `Skills/multi-tenant/references/go-backends.md`
- Data model and threat decisions: `Skills/multi-tenant/references/architecture.md`

The coordinating agent must ensure every implementation agrees on:

- canonical tenant identity and resolution sources;
- the request/context contract and missing-context behavior;
- authorization and platform-admin rules;
- persistence, cache, file, event, and job scoping;
- cross-tenant denial tests and migration/rollback expectations.

Do not merge locally correct framework implementations that disagree on these
cross-service invariants.

## Handoff format

Each agent reports:

- Scope and files changed.
- Tenant assumptions and trust boundaries.
- Public contracts or schema changes.
- Tests run and important negative cases.
- Remaining risks, follow-up work, or blocked dependencies.

