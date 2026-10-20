---
name: repo-backend-service-review
description: Reviews backend service changes for boundaries, runtime behavior, resilience, configuration, security-sensitive paths, health checks, observability, and operational readiness. Use when changing handlers, routes, controllers, services, workers, jobs, queues, middleware, runtime config, or backend deployment behavior.
---

# Repo Backend Service Review

Use this skill to review backend changes before implementation or before finalizing a diff.

## Review Process

1. Identify the backend responsibility being changed.
2. Inspect nearby patterns before recommending changes.
3. Check service boundaries and dependency direction.
4. Check runtime behavior, configuration, and environment assumptions.
5. Check failure handling, retries, timeouts, and idempotency.
6. Check data mutation, authorization, and privacy impact.
7. Check health/readiness and operational visibility.
8. Identify validation and rollback needs.
9. Provide actionable review findings with severity.

Use `workflows/backend-service-review-workflow.md` for a structured review and `resources/backend-service-review-checklist.md` as the checklist.

Scripts owned by this skill live in `scripts/`. Run them with `--help` before manual use.
