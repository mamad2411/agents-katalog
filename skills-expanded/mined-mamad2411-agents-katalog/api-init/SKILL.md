---
name: api-init
description: "Initialize or refresh API contracts from frontend user flows using the dev++ clarification-first workflow. Use when the user invokes /api-init or asks to audit APIs, DTOs, frontend API clients, permissions, errors, user flows, or full-stack contracts."
---

# api-init

Initialize or refresh API documentation for the requested scope.

Use any text supplied after the slash command as the requested scope, domain, route, feature, or path.

Rules:
- Start from frontend user stories and user flows; do not scan backend endpoints in isolation.
- Map each flow to frontend clients, backend handlers, DTOs, permissions, errors, side effects, and tests.
- Reconcile frontend-sent fields with backend-accepted request fields and frontend-used response fields.
- Record missing APIs, broken chains, unhandled errors, dead UI, and contract drift.
- Prefer existing docs. If none exist, propose `docs/ai-context/api/`.
- Do not edit files until the user explicitly approves the exact docs location and write plan.
- Mark unknowns as unknown; ask instead of inventing contracts.
