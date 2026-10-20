---
name: pro-dotnet-memory-management
description: "Knowledge base from \"Pro .NET Memory Management, 2nd Edition\" by Konrad Kokosa, Christophe Nasarre & Kevin Gosse. Use when applying their frameworks for .NET GC internals, heap partitioning (SOH/LOH/POH), allocation, generations, GC flavors/tuning, object lifetime & IDisposable, Span<T>/zero-alloc, memory diagnosis (WinDbg/PerfView/dotnet-trace/ClrMD), studying the book, or referencing its concepts."
---

<!-- argument-hint: [topic, framework name, or chapter number] -->

# Pro .NET Memory Management, 2nd Edition
**Authors**: Konrad Kokosa, Christophe Nasarre, Kevin Gosse | **Pages**: ~780 | **Chapters**: 15 | **Generated**: 2026-07-04

## How to Use This Skill

- **Without arguments** — load core frameworks below for reference
- **With a topic** — ask about `LOH`, `write barrier`, `Span<T>`, `background GC`, `finalization`; I find and read the relevant chapter
- **With chapter** — ask for `ch08`; I load that specific chapter
- **Browse** — ask "what chapters do you have?" for the full index

When you ask about a topic not in Core Frameworks below, I read the relevant chapter file first.

---

## Core Frameworks & Mental Models

**Mutator / Allocator / Collector triad** — the three roles in any managed runtime. Your code is the *Mutator* (mutates the object graph); the *Allocator* hands out memory; the *Collector* reclaims it. GC pauses = Collector suspending Mutators. Reason about every memory problem by asking which role is misbehaving.

**Reachability as a proxy for liveness** — the GC keeps an object if it's *reachable* from a root, not if it's truly *needed*. A memory leak in .NET = an unintended reference keeping a dead object reachable. Diagnosis = find the rooting reference. This is the single most useful lens for leak hunting (Ch 8 root types).

**Heap partitioning — by size and by lifetime.** The managed heap is split so the Collector works cheaply:
- **Size**: **SOH** (Small Object Heap, <85,000 bytes) vs **LOH** (Large Object Heap, ≥85,000 bytes, collected only in gen2, not compacted by default). Plus **POH** (Pinned Object Heap) and **NonGC/frozen** heap.
- **Lifetime**: **generations** gen0/gen1/gen2 — young objects die fast and are collected often & cheaply; survivors get promoted; gen2 is touched rarely. Cross-generation references tracked via **card tables + write barriers**.
- Decision rule: object ≥85K → LOH → gen2 cost. Pool it, split it, or reuse it.

**Bump-pointer allocation** — the fast path. Each thread has an **allocation context**; new objects are placed by incrementing a pointer (a few instructions). Slow paths (free-list scan, commit memory, trigger GC) are what hurt. Perf work = minimize allocations (explicit *and* hidden: boxing, closures, LINQ, string concat, params arrays).

**Condemned generation + allocation budget** — the GC self-tunes. It collects a *condemned generation* and everything younger; timing is driven by per-generation **allocation budgets** (`desired_allocation`). The defaults are almost always right — explicit `GC.Collect()` is usually harmful. Prefer changing allocation behavior over changing the GC.

**The 4 GC phases** — Mark → Plan → Sweep **or** Compact:
- **Mark**: suspend threads, trace from all roots (stack, statics, handles, finalization queue, cross-gen), set mark bits. Unreached = dead.
- **Plan**: *simulate* compaction (plugs & gaps, relocation offsets) then `decide_on_compacting` chooses Sweep vs Compact.
- **Sweep**: turn gaps into free-list entries, no moving (fast, keeps fragmentation).
- **Compact**: move objects, rewrite references (defragments, expensive).

**Four GC flavors** — two orthogonal axes: **Workstation vs Server** (Server = per-core heaps + GC threads, higher throughput, more memory) × **Non-concurrent vs Concurrent/Background** (Background = marks concurrently, shorter pauses). Plus `GCSettings.LatencyMode` and **DATAS** (dynamic heap count adaptation). Benchmark before switching; defaults win by default.

**Object lifetime ≠ resource lifetime.** GC owns *memory*; you own *resources* (files, sockets, native handles). Three bridges: **finalization** (non-deterministic, avoid), **IDisposable/Dispose pattern** (deterministic, prefer), **weak references**. Rule: wrap native handles in **SafeHandle**, never hand-write finalizers.

**Zero-allocation toolkit** — `Span<T>`/`ReadOnlySpan<T>` (sliceable stack-only view over any contiguous memory), `Memory<T>` (heap-storable counterpart), `stackalloc`, `ArrayPool<T>`, ref structs/ref returns, `Unsafe`/`MemoryMarshal`, and `System.IO.Pipelines` for zero-copy I/O. Data-oriented design restructures for cache-friendliness (Ch 2 locality).

**Measure first (Rule 5: Measure GC Early).** Memory is a runtime phenomenon — never guess. Pick tools by overhead-vs-detail and platform: PerfView/dotnet-trace/dotnet-counters/dotnet-gcdump, WinDbg+SOS, VS profilers, ClrMD/TraceEvent for custom tooling. Watch % time in GC, gen sizes over time, allocation rate, gen2 frequency.

---

## Chapter Index

| # | Title | Key Frameworks |
|---|-------|----------------|
| [ch01](chapters/ch01-basic-concepts.md) | Basic Concepts | Mutator/Allocator/Collector, reachability, tracing vs refcount, stack/heap/pointer |
| [ch02](chapters/ch02-low-level-memory-management.md) | Low-Level Memory Management | cache lines, locality, false sharing, virtual memory reserve/commit, NUMA |
| [ch03](chapters/ch03-memory-measurements.md) | Memory Measurements | Measure Early, sampling vs tracing, overhead vs invasiveness, tool catalog |
| [ch04](chapters/ch04-dotnet-fundamentals.md) | .NET Fundamentals | CLR/VES vs GC, value vs reference semantics, boxing, strings, escape analysis |
| [ch05](chapters/ch05-memory-partitioning.md) | Memory Partitioning | SOH/LOH/POH, generations, card tables, write barriers, remembered sets |
| [ch06](chapters/ch06-memory-allocation.md) | Memory Allocation | bump-pointer alloc, allocation context, free-list, allocation quantum, heap balancing |
| [ch07](chapters/ch07-gc-introduction.md) | GC — Introduction | condemned generation, allocation budget, GC pipeline, Workstation/Server, concurrent |
| [ch08](chapters/ch08-gc-mark-phase.md) | GC — Mark Phase | root types, marking traversal, mark stack, GC Info, interior pointers |
| [ch09](chapters/ch09-gc-plan-phase.md) | GC — Plan Phase | plugs & gaps, brick table, binary plug tree, decide_on_compacting, relocation offset |
| [ch10](chapters/ch10-gc-sweep-and-compact.md) | GC — Sweep & Compact | sweep→free-list, compact→move+relocate, UOH sweep |
| [ch11](chapters/ch11-gc-flavors-and-settings.md) | GC Flavors & Settings | 4 flavors, background GC phases, latency modes, DATAS |
| [ch12](chapters/ch12-object-lifetime.md) | Object Lifetime | Dispose pattern, SafeHandle, weak references, finalization queue |
| [ch13](chapters/ch13-miscellaneous-topics.md) | Miscellaneous Topics | dependent handles, ref structs/ref fields, byref, TLS, ConditionalWeakTable |
| [ch14](chapters/ch14-advanced-techniques.md) | Advanced Techniques | Span<T>/Memory<T>, IMemoryOwner, Unsafe, data-oriented design, Pipelines |
| [ch15](chapters/ch15-programmatical-apis.md) | Programmatical APIs | GC/GCSettings, ClrMD, TraceEvent, custom (standalone) GC |

## Topic Index

- **Allocation / bump pointer / allocation context** → ch06
- **ArrayPool / object pooling** → ch06, ch14
- **Background / concurrent GC** → ch11
- **Boxing** → ch04, ch06
- **Card table / write barrier / remembered set** → ch05
- **ClrMD / TraceEvent / diagnostics tooling** → ch03, ch15
- **Compaction** → ch09, ch10
- **Condemned generation / allocation budget** → ch07
- **DATAS** → ch11
- **Data-oriented design / cache locality** → ch02, ch14
- **Dispose pattern / IDisposable** → ch12
- **Escape analysis / stack allocation** → ch04
- **Finalization / finalizer** → ch12
- **Generations (gen0/1/2)** → ch05, ch07
- **GC.Collect / GC / GCSettings APIs** → ch07, ch15
- **GC flavors (Workstation/Server)** → ch07, ch11
- **GC phases (Mark/Plan/Sweep/Compact)** → ch07, ch08, ch09, ch10
- **Latency modes / TryStartNoGCRegion** → ch11, ch15
- **LOH (Large Object Heap) / 85,000-byte threshold** → ch05, ch10
- **Memory<T>** → ch14
- **NUMA / cache lines / false sharing** → ch02
- **Pinning / GCHandle / POH** → ch05, ch08, ch13
- **Ref structs / ref returns / byref / ref fields** → ch13
- **Roots (stack/static/handle/finalization)** → ch08
- **SafeHandle** → ch12
- **Span<T> / stackalloc / zero-alloc** → ch14
- **Strings / interning** → ch04
- **Value vs reference types** → ch04
- **Virtual memory / reserve-commit** → ch02
- **Weak references / ConditionalWeakTable / dependent handles** → ch12, ch13
- **Custom / standalone GC** → ch15

## Supporting Files

- [glossary.md](glossary.md) — key terms with definitions
- [patterns.md](patterns.md) — memory/GC techniques and optimizations
- [cheatsheet.md](cheatsheet.md) — decision rules, thresholds, diagnostic tells

---

## Scope & Limits

Covers the book's content: CoreCLR GC internals as of .NET 8-era, memory diagnosis, and low-allocation coding. For live diagnosis in your codebase, combine with actual tooling (PerfView, dotnet-trace, WinDbg+SOS). Runtime internals evolve per .NET version — verify version-specific details (DATAS, regions vs segments, heap limits) against current docs.
