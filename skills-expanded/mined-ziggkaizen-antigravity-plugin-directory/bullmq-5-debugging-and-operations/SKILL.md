---
name: bullmq-5-debugging-and-operations
description: Diagnoses and operates BullMQ 5 queues, workers, Redis-backed job states, QueueEvents listeners, failed jobs, stalled jobs, scheduler issues, incidents, and safe runtime inspections. Use when debugging failures, latency, stuck jobs, Redis issues, or production BullMQ behavior.
license: MIT
compatibility: Requires a Node.js project using BullMQ 5.x. Runtime scripts may require Redis access through REDIS_URL.
---

# BullMQ 5 Debugging and Operations Skill

Use this skill when troubleshooting BullMQ 5 runtime behavior or reviewing operational safety.

## When to Use

Use this skill for:

- Failed jobs.
- Jobs stuck in waiting, active, delayed, paused, or waiting-children states.
- Unexpected retries or missing retries.
- Scheduler jobs not appearing at expected times.
- Worker crashes, Redis disconnects, or slow processing.
- QueueEvents monitoring.
- Redis memory, keyspace, or ACL concerns related to BullMQ.
- Incident response.

## Operating Principles

1. Diagnose before changing state.
2. Confirm queue name, prefix, Redis database, environment, and deployment target.
3. Prefer read-only commands and BullMQ getters for inspection.
4. Avoid destructive operations until the user confirms the exact queue, Redis URL, and environment.
5. Treat job payloads and failure reasons as potentially sensitive.
6. Check both application logs and Redis/BullMQ state.
7. Capture queue counts before and after operational changes.
8. Distinguish producer problems, worker problems, Redis problems, and downstream dependency problems.
9. Preserve failed jobs long enough for root-cause analysis.
10. Write a brief incident note with cause, impact, remediation, and prevention.

## Workflow References

- [failed-job-triage-workflow](workflows/failed-job-triage-workflow.md): Use for failed or retrying jobs.
- [production-incident-workflow](workflows/production-incident-workflow.md): Use for live incidents or suspected production impact.

## Resource References

- [operations-runbook](resources/operations-runbook.md): Operational checks and safe actions.
- [observability-checklist](resources/observability-checklist.md): Logging, metrics, traces, and QueueEvents checklist.

## Examples

- [queue-events-listener.ts](examples/queue-events-listener.ts): QueueEvents listener example.

## Scripts

Run scripts with `--help` before using them.

```bash
node scripts/bullmq-command-safety.mjs --help
node scripts/bullmq-queue-counts.mjs --help
```

Use `bullmq-queue-counts.mjs` only with a Redis URL and queue name that the user has approved for inspection.
