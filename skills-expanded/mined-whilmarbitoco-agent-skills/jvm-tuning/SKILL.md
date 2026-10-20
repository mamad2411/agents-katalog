---
name: jvm-tuning
description: >
  Extends agent's knowledge of tuning JVM garbage collection and memory
  for Java POS applications. Use when profiling GC pauses, sizing heaps,
  or configuring low-latency G1GC flags.
compatibility: Java 21+
metadata:
  domain: performance
  level: advanced
  stack: [java-21, slf4j-2]
  version: "1.0.0"
---

# JVM Tuning

POS applications need predictable low-latency response because every
millisecond of GC pause delays a sale. Java 21 defaults to G1GC, but
explicit tuning is still required for terminal hardware with 4–8 GB RAM.

## Concepts

- **G1GC** — region-based collector with configurable max pause target
  (`-XX:MaxGCPauseMillis`).
- **Heap sizing** — `-Xms` == `-Xmx` to avoid runtime heap resizing
  (eliminates full GC from heap expansion).
- **CDS (Class Data Sharing)** — pre-parsed class metadata archive shared
  across JVM instances; reduces startup time.
- **Virtual threads** — `ExecutorService.newVirtualThreadPerTaskExecutor()`
  for I/O-bound work without thread pool tuning.

## Rules

1. Always set `-Xms` equal to `-Xmx` in production.
2. Set `-XX:MaxGCPauseMillis=50` for POS workloads (sub-100ms target).
3. Generate a CDS archive with `-Xshare:dump` at build time; activate
   with `-Xshare:on` at runtime.
4. Use `-XX:+UseStringDeduplication` if logs and receipts create many
   duplicate strings.
5. Log GC with `-Xlog:gc*:file=gc.log:time,uptime,level,tags` for
   post-mortem analysis.

## Anti-patterns

See [anti-patterns.md](./anti-patterns.md).

## Related

- memory-profiling — heap dump and VisualVM profiling
- startup-optimization — CDS and class loading improvements
