---
name: memory-profiling
description: >
  Extends agent's knowledge of JavaFX memory leak detection and profiling.
  Use when diagnosing high memory usage, UI slowdowns, or OutOfMemoryError.
compatibility: Java 21+
metadata:
  domain: performance
  level: advanced
  stack: [java-21, javafx]
  version: "1.0.0"
---

# Memory Profiling

JavaFX-specific memory leak patterns and tools to diagnose them.

## Core Concepts
- Listener leaks — most common JavaFX memory leak
- WeakListener / WeakChangeListener — automatic cleanup
- Heap dumps — capture and analyze with VisualVM
- Epsilon GC test — isolate memory leaks

## Rules
1. Check for listener leaks first — `Platform.runLater` inside listeners, anonymous lambdas that capture Scene
2. Use WeakListener for bindings that outlive the observable
3. Monitor with VisualVM during development — look for growing `ObservableList` or `Node` counts
4. Test with `-XX:+HeapDumpOnOutOfMemoryError` — get a dump for post-mortem analysis
5. Unbind properties when screen closes — don't hold references to disposed UI

## Anti-patterns
- Anonymous lambdas capturing Node/Scene references
- Forgetting to remove listeners on screen close
- Using `Platform.runLater(Runnable)` stored in a list that never clears

## Relates to
- jvm-tuning
- javafx-threading
- javafx-observable-state
