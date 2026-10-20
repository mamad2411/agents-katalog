---
name: virtual-threads
description: >
  Extends agent's knowledge of Java 21 virtual threads for scalable concurrent I/O.
  Use when creating concurrent tasks, replacing thread pools for blocking I/O, or
  avoiding thread pinning with synchronized blocks.
compatibility: Java 21+
metadata:
  domain: core-java
  level: intermediate
  stack: [java-21]
  version: "1.0.0"
---

# Virtual Threads

Virtual threads (JEP 444) are lightweight threads managed by the JVM, not the OS.
Use them for I/O-bound work: HTTP calls, DB queries, file reads.

## Concepts

- `Thread.ofVirtual().start(runnable)` — create and start a virtual thread
- `Thread.startVirtualThread(runnable)` — shorthand
- `StructuredTaskScope` (JEP 453) — structured concurrency withshutdown on failure/cancellation
- Pinning — a virtual thread pins its carrier thread inside `synchronized`, blocking the carrier
- `ReentrantLock` — drop-in replacement for `synchronized`; does NOT pin

## Rules

1. Use virtual threads for I/O-bound tasks; keep platform threads for CPU-bound.
2. Replace `ExecutorService` fixed pools with `Executors.newVirtualThreadPerTaskExecutor()`.
3. Never use `synchronized` on long-running or I/O sections in virtual threads — use `ReentrantLock`.
4. Use `StructuredTaskScope` to fan-out concurrent subtasks with automatic cancellation.
5. Virtual threads are short-lived; do NOT pool or cache them.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- concurrency-fundamentals — ExecutorService, CompletableFuture, ReentrantLock
- exception-strategy — domain exceptions, logging
