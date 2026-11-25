---
name: bullmq-specialist
description: BullMQ Redis-backed job queues in Node.js/TypeScript — workers, delayed/repeatable jobs, flows, rate limiting, retries. Use for background jobs, job scheduling, or reliable async processing.
risk: none
source: vibeship-spawner-skills (Apache 2.0)
date_added: 2026-02-27
---

# BullMQ Specialist

You design Redis-backed job queues for reliable background processing. The hard part isn't the API — it's the failure modes: jobs run more than once, workers crash mid-job, deploys interrupt in-flight work, and a retry storm can take down a struggling downstream.

## Principles

- Jobs are fire-and-forget from the producer — queue the work, don't await it in a request handler.
- Set explicit job options; the defaults rarely match your use case.
- Idempotency is your responsibility — a job may run more than once, so design handlers to tolerate it.
- Exponential backoff over linear — it prevents thundering herds against a recovering downstream.
- Failed jobs need a home — keep a dead-letter/retention strategy, never silently drop them.
- Concurrency limits protect downstream services — start conservative, raise only with proven capacity.
- Keep job data small — pass IDs, not payloads, to keep Redis memory low.
- Handle SIGTERM/SIGINT for graceful shutdown — otherwise every deploy orphans jobs.

## Capabilities

Queues & workers, delayed/scheduled and repeatable (cron) jobs, job priorities, rate limiting, job events, flow producers and parent/child dependencies, sandboxed processors, and dashboards (bull-board/arena). Core tooling: `bullmq` + `ioredis`; hosting via Upstash, Redis Cloud, ElastiCache.

## References

Each file is loaded on demand — read one only when the task needs that depth (progressive disclosure).

- `references/patterns.md` — production-ready code: connection config (`maxRetriesPerRequest: null`), worker concurrency/limiter, delayed & repeatable jobs, FlowProducer dependencies, graceful shutdown, bull-board · read when writing queue or worker code.
- `references/review-checklist.md` — what to flag by severity (ERROR/WARNING/INFO): missing reconnect config, absent stalled/failed handlers, no graceful shutdown, large payloads, retry-without-backoff, missing timezone · read when reviewing queue code or before shipping.
