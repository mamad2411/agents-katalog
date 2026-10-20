---
name: repo-api-error-idempotency-review
description: Reviews API error semantics, retry safety, idempotency, timeouts, concurrency, rate limits, async jobs, bulk operations, and partial failures. Use when designing or changing operations that can fail, retry, create resources, mutate state, or process batches.
---

# Repository API Error and Idempotency Review

Use this skill to make API failure behavior explicit and safe.

## When to Use This Skill

Use when API work involves create, update, delete, payment-like operations, client retries, network timeouts, idempotency keys, async jobs, webhooks, rate limits, optimistic concurrency, conflicts, bulk operations, partial success, partial failure, or validation errors.

## Process

1. Identify side effects.
2. Define retry safety.
3. Define idempotency behavior.
4. Define timeout and cancellation behavior.
5. Define error shapes and stable error codes.
6. Define conflict and concurrency handling.
7. Define tests for duplicate requests, timeouts, conflicts, and partial failures.

## Workflow

Use `workflows/api-error-idempotency-review-workflow.md`.

## Resources

- `resources/api-error-idempotency-checklist.md`
