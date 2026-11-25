---
name: backend-design
description: Design backend architecture, service boundaries, domain models, data flow, async jobs, reliability strategy, error handling, observability, and deployment shape. Use before implementing significant backend systems, APIs, services, queues, integrations, or refactors.
---

# Backend Design

## Workflow

1. Define domain boundaries, responsibilities, and owned data.
2. Choose synchronous API, async queue, scheduled job, or event flow based on user impact and reliability needs.
3. Specify transaction boundaries, idempotency keys, retries, timeouts, and failure handling.
4. Define configuration, secrets, logging, metrics, traces, and health checks.
5. Identify rollout, migration, compatibility, and rollback strategy.

## Design Requirements

- Keep business rules out of thin controllers when the codebase supports services or domain modules.
- Make data consistency explicit: strong consistency, eventual consistency, or compensating action.
- Avoid distributed transactions unless the existing system already uses them safely.
- Design for partial failure in external integrations.
- Prefer boring, maintainable architecture over new infrastructure.

## Output

Provide module boundaries, sequence or data flow, key interfaces, failure paths, and verification plan. Keep implementation details aligned with the existing stack.

## Bundled Resources

- `references/service-boundaries.md`: route/application/domain/repository/integration boundaries and reliability review questions.
