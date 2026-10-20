---
name: bullmq-5-queue-architecture
description: Designs, implements, tests, and reviews BullMQ 5 queues, workers, producers, FlowProducer flows, Job Schedulers, Redis connection handling, and migration plans. Use when the task mentions BullMQ, background jobs, queues, workers, schedulers, retries, rate limits, or BullMQ 4 to 5 migration.
license: MIT
compatibility: Requires a Node.js project using BullMQ 5.x. Scripts require Node.js 18 or newer.
---

# BullMQ 5 Queue Architecture Skill

Use this skill to produce practical BullMQ 5 code and reviews that are safe for production.

## When to Use

Use this skill when the task involves:

- Adding or refactoring BullMQ 5 producers, queues, workers, or QueueEvents listeners.
- Designing job names, payload types, result types, retries, backoff, delays, deduplication, or retention.
- Implementing scheduled recurring jobs.
- Migrating BullMQ 4 code to BullMQ 5.
- Reviewing queue code for production readiness.
- Writing tests for queue and worker behavior.

## Core Operating Rules

1. Confirm the installed BullMQ major and minor before using minor-sensitive APIs.
2. Keep queue architecture explicit: queue name, job names, payload schema, result schema, retry policy, retention policy, idempotency key, and downstream limits.
3. Always pass explicit Redis `connection` configuration to BullMQ 5 classes.
4. For `Worker` with custom ioredis, ensure `maxRetriesPerRequest: null`.
5. Prefer Job Schedulers over legacy repeatable jobs when BullMQ is 5.16.0 or newer.
6. Do not default to `QueueScheduler` for BullMQ 5.
7. Use idempotent processors and safe retry classification.
8. Keep payloads small, JSON-serializable, and free of secrets.
9. Close queues, workers, QueueEvents, FlowProducers, and Redis clients on shutdown.
10. Add tests or update existing tests for queue behavior.

## Workflow References

Use these workflows when the task is repetitive or high-risk:

- [queue-feature-design-workflow](workflows/queue-feature-design-workflow.md): Use for adding a new queue feature or worker.
- [job-scheduler-design-workflow](workflows/job-scheduler-design-workflow.md): Use for scheduled or recurring jobs.
- [migration-from-bullmq-4-workflow](workflows/migration-from-bullmq-4-workflow.md): Use for BullMQ 4 to BullMQ 5 migration.

## Resource References

- [bullmq-5-api-patterns](resources/bullmq-5-api-patterns.md): Common implementation patterns.
- [job-design-checklist](resources/job-design-checklist.md): Review checklist for job shape and behavior.
- [redis-connection-matrix](resources/redis-connection-matrix.md): Connection guidance by BullMQ class.

## Examples

- [queue-and-worker.ts](examples/queue-and-worker.ts): Minimal typed queue and worker pattern.
- [job-scheduler.ts](examples/job-scheduler.ts): Job Scheduler pattern for BullMQ 5.16.0+.
- [vitest-worker-test.ts](examples/vitest-worker-test.ts): Example test shape.

## Scripts

Run scripts with `--help` before using them.

```bash
node scripts/bullmq-project-scan.mjs --help
node scripts/bullmq-final-check-reminder.mjs --help
node scripts/bullmq-worker-test-trigger.mjs --help
```

The project scan script is heuristic. Use it to find review targets, not as a substitute for reading code.

## Related Skills

For dedicated idempotency, retry, payload privacy, and critical-flow reviews, use `bullmq-5-idempotency-review`.
