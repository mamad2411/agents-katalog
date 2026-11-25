---
name: multicore-default
description: Multi-core by default CPU architecture using lane-based parallelism. Use when implementing threading, parallelizing work, splitting loops across cores, synchronizing threads, or when the user asks about multithreading, job systems, or CPU parallelism.
---

# Multi-Core by Default (CPU Shader Architecture)

You are an expert in lane-based multi-core programming for game engines. When helping with threading or parallelism, follow these principles strictly.

## Core Philosophy

**All CPU cores enter the exact same entry point and execute the exact same code simultaneously, like a GPU shader.**

Do NOT use traditional job systems with worker pools, scattered async tasks, or detached thread lifetimes. Instead, treat CPU threads as "lanes" — identical execution paths that mathematically subdivide work.

## Architecture

### 1. Universal Entry Point

Launch one thread per CPU core into the same function at startup:

```
bootstrap :: proc() {
    threads: [NUMBER_OF_CORES]Thread
    for i in 0..<NUMBER_OF_CORES {
        threads[i] = launch_thread(entry_point, transmute(rawptr)i)
    }
    for t in threads { join_thread(t) }
}
```

Every core runs the exact same code path. Single-core is simply `lane_count = 1`.

### 2. Lane Context (Thread-Local)

Each thread knows its place via thread-local helpers:

- `lane_idx()` → this thread's index (0 through N-1)
- `lane_count()` → total number of threads

### 3. Going Wide (Uniform Work Distribution)

When hitting a heavy loop, mathematically divide the range:

```
range := lane_range(total_count)  // each lane gets a unique chunk
for i in range.min..<range.max {
    // process items[i] — no overlap, no locks
    lane_sum += values[i]
}
```

`lane_range(count)` divides `count` items evenly across `lane_count()` lanes, handling remainders. Each lane processes a strictly non-overlapping chunk — **zero locks, zero mutexes**.

#### Dynamic Work Stealing (Variable Cost Items)

If per-item cost varies wildly, use an atomic counter instead of fixed ranges:

```
for {
    idx := atomic_add(&global_counter, 1)
    if idx >= total_count do break
    process(items[idx])
}
```

This keeps all cores saturated even with uneven workloads.

### 4. Going Narrow (Masking)

Operations that must happen once (allocating memory, opening files, printing):

```
if lane_idx() == 0 {
    fmt.println("Sum:", sum)  // Only prints once
}
```

### 5. Barrier Synchronization

When lanes must wait for each other before proceeding:

```
lane_sync()  // All threads block here until every thread arrives
```

### 6. Broadcasting

When Lane 0 produces a value (e.g., allocates memory, reads file size) that all lanes need:

```
values_count: i64 = 0
values: [^]i64 = nil

if lane_idx() == 0 {
    values_count = get_size_from_file(file)
    values = allocate(values_count)
}

lane_sync_broadcast(&values_count, 0)  // broadcast from lane 0 to all
lane_sync_broadcast(&values, 0)

// Now ALL lanes have the pointer and can work in parallel
range := lane_range(values_count)
file_read(file, range, values[range.min:])
```

## Benefits

- **Perfect stack traces**: every thread has an identical, linear call stack — debugging is trivial
- **Single-threaded mode is free**: set `lane_count = 1`, exact same code path
- **No scattered control flow**: no callbacks, no job graphs, no detached futures
- **No mutexes needed**: mathematical subdivision guarantees non-overlapping writes

## Rules When Writing Multi-Core Code

- Default to going wide — parallelize every heavy loop
- Use `lane_sync()` barriers between phases, not locks
- Only go narrow for inherently serial operations (file open, GPU submit, print)
- Use `lane_sync_broadcast` to share lane 0's results with all lanes
- Never use mutex/lock for data parallelism — use lane ranges instead
- Atomic counters only when per-item cost varies significantly

## Anti-Patterns (Never Do This)

- Never spin up temporary worker threads for individual tasks
- Never use complex job dependency graphs
- Never use mutexes for bulk data processing
- Never scatter async callbacks across the codebase
- Never detach thread lifetimes from the main loop
- Never assume code runs single-threaded by default — it's multi-core by default
