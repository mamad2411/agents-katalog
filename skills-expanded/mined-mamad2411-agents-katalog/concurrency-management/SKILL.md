---
name: concurrency-management
description: Manage concurrency in backend code. Use when handling threads,
  async tasks, and shared resources safely.
metadata:
  tags: concurrency, management
---

# Concurrency Management

## Use this skill when
- Writing safe concurrent code (threads/async)
- Managing shared state and race conditions
- Choosing async/parallel strategies

## Do not use this skill when
- Single-request simple flows
- Distributed coordination (use distributed-locking)

## Instructions
1. Prefer immutable data and message passing over shared mutable state.
2. Use structured concurrency: bounded pools, context/cancellation propagation.
3. Guard shared state with the narrowest lock; prefer atomic ops.
4. Avoid blocking calls inside async code (thread pool starvation).
5. Define concurrency limits for fan-out and batch jobs.
6. Detect and fix race conditions with stress tests and race detectors.
7. Prefer task queues over unbounded spawn.

## Checklist
- No unbounded concurrency
- Shared state is synchronized or immutable

## Output Format
- Concurrency model | resources | guards | limits

## Common Mistakes
- Per-item synchronous API calls in a loop
- Blocking the event loop with CPU work
- Silent swallowed exceptions in spawned tasks
