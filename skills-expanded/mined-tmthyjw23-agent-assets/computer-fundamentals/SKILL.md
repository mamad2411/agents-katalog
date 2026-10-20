---
name: computer-fundamentals
description: >
  Ground designs in how computers actually work. Use for processes vs threads,
  concurrency vs parallelism, memory management (paging/segmentation), deadlocks,
  garbage collection, byte ordering, CPU/IO, OS models, and systems primitives.
  Triggers: "process vs thread", "concurrency", "deadlock", "memory", "garbage
  collection", "how does it run", "endianness".
---

# Computer Fundamentals

The machine-level facts that explain why systems behave as they do.

## When to use
- Reasoning about concurrency, blocking, and resource usage.
- Explaining performance limits (CPU, memory, IO).
- Debugging deadlocks, leaks, or contention.
- Interview fundamentals.

## Execution model
- **Process vs thread:** processes isolate memory; threads share memory within a
  process. Context switching cost, IPC mechanisms.
- **Concurrency vs parallelism:** concurrency = dealing with many things at
  once; parallelism = doing many things at once. Not the same.
- **Scheduling:** time slicing, blocking vs non-blocking, async IO.
- **User space vs kernel space;** syscalls are expensive; batch them.
- **Inter-process communication** on Linux (pipes, sockets, shared memory,
  signals).

## Memory
- Hierarchy: registers → L1/L2/L3 → RAM → SSD/HDD → network. Latency differs by
  orders of magnitude.
- Paging vs segmentation; virtual memory; page faults.
- Garbage collection: tracing (mark-sweep, generational), pause times, tuning.
- Memory leaks, fragmentation, and why caching holds memory.

## Concurrency hazards
- Deadlock: conditions (mutual exclusion, hold-and-wait, no preemption,
  circular wait); prevention (ordering, timeouts, avoidance).
- Race conditions, data races, atomicity, memory visibility.
- Blocking vs non-blocking queues; backpressure.

## Numbers to internalize
- Latency numbers every engineer should know (L1/L2/RAM/SSD/disk/DC/RTT).
- Limits: memory bandwidth, network round trips, syscall overhead.

## Checklist
- [ ] Concurrency model chosen (threads/async/actor) deliberately.
- [ ] Shared state minimized; synchronization correct (not over-locked).
- [ ] Deadlock risk assessed; lock ordering defined.
- [ ] Memory footprint and GC pauses considered.
- [ ] IO blocking vs non-blocking understood per path.
- [ ] Latency budget grounded in real hardware numbers.

## Common pitfalls
- Confusing concurrency with parallelism.
- Over-locking → contention; under-locking → races.
- Unbounded memory growth from caches/queues.
- Assuming disk/RAM/network are fast.
- Ignoring GC pauses in latency-sensitive services.

## References
- `...\what-is-the-difference-between-process-and-thread.md`
- `...\concurrency-is-not-parallelism.md`
- `...\what-is-a-deadlock.md`
- `...\how-does-garbage-collection-work.md`
- `...\what-are-the-differences-between-paging-and-segmentation.md`
- `...\types-of-memory.md`, `...\types-of-memory-and-storage.md`, `...\big-endian-vs-little-endian.md`
- `...\how-do-processes-talk-to-each-other-on-linux.md`, `...\how-do-computer-programs-run.md`, `...\linux-boot-process-explained.md`
- `...\blocking-vs-non-blocking-queue.md`
- `...\10-key-data-structures-we-use-every-day.md`, `...\top-6-multithreading-design-patterns-you-must-know.md`
- `...\which-latency-numbers-should-you-know.md`
Base: `D:\Agent-Assets\system-design-101\data\guides\`

## Related skills
`backend-architecture`, `scalability-and-performance`, `networking-fundamentals`,
`developer-productivity`.
