---
name: bullmq-5-idempotency-review
description: Reviews BullMQ 5 jobs for idempotency, deduplication, retry safety, sensitive payload exposure, privacy-safe notification behavior, and critical-flow dependency risks. Use when checking whether jobs can be retried, duplicated, delayed, failed, replayed, or safely inspected.
license: MIT
compatibility: Requires a Node.js project using BullMQ 5.x. Scripts require Node.js 18 or newer.
---

# BullMQ 5 Idempotency Review Skill

Use this skill to review BullMQ 5 job behavior before production rollout, incident remediation, or risky refactoring.

## When to Use

Use this skill when the task involves:

- Checking whether a processor is safe to retry.
- Reviewing custom `jobId`, deduplication, debounce, throttle, or uniqueness behavior.
- Reviewing sensitive job payloads, failed-job retention, logs, traces, and QueueEvents.
- Designing privacy-safe notification jobs such as email, SMS, push, webhook, or in-app notification dispatch.
- Checking whether critical correctness depends on a BullMQ job succeeding.
- Reviewing a retry policy, backoff, dead-letter handling, poison payload handling, or replay plan.

## Core Review Rules

1. Assume BullMQ jobs can be delivered at least once and may run more than once.
2. Require idempotency for all processors with side effects.
3. Use stable string idempotency keys for external side effects.
4. Do not put secrets or unnecessary sensitive data in payloads.
5. Bound retries and classify failures before retrying.
6. Preserve enough failure context for debugging without retaining sensitive payloads indefinitely.
7. Keep critical source-of-truth state outside job success unless an explicit durable workflow is designed.
8. Prefer read-only inspection before operational changes.

## Workflow References

- [idempotency-and-dedupe-review-workflow](workflows/idempotency-and-dedupe-review-workflow.md): Use for retry/dedupe/idempotency review.
- [retry-and-payload-safety-review-workflow](workflows/retry-and-payload-safety-review-workflow.md): Use for retry limits, sensitive payloads, and failed-job retention review.

## Resource References

- [idempotency-review-checklist](resources/idempotency-review-checklist.md): Review checklist for idempotency and dedupe.
- [retry-policy-matrix](resources/retry-policy-matrix.md): Retry classification guidance.
- [sensitive-payload-patterns](resources/sensitive-payload-patterns.md): Payload and logging privacy guidance.

## Examples

- [idempotent-notification-job.ts](examples/idempotent-notification-job.ts): Generic privacy-safe notification job pattern.

## Scripts

Run scripts with `--help` before using them.

```bash
node scripts/bullmq-code-safety-scan.mjs --help
node scripts/bullmq-proposed-change-check.mjs --help
```

The scan scripts are heuristic. Treat findings as review prompts, not as proof of a vulnerability or correctness bug.
