---
name: cache-aware-performance-reviewer
description: Review slow code, algorithms, data structures, database-heavy flows, loops, allocations, collections, serialization, and hot paths through hardware-aware performance thinking. Use when asked why something is slow, whether Big-O is enough, how to optimize, how to choose array vs map/tree/list, or how to reason about memory access, cache locality, allocations, async overhead, and real runtime behavior.
---

# Cache-Aware Performance Reviewer

## Purpose
Use this skill to analyze performance with the assumption that software runs on real processors, real memory, real runtimes, real networks, and real databases — not in an idealized Big-O universe.

The goal is not premature optimization. The goal is to stop making performance decisions from the wrong abstraction level.

## Core philosophy

- Big-O is useful but incomplete.
- Real performance often depends on memory access patterns, locality, allocation, branch behavior, IO, serialization, database shape, and runtime overhead.
- A theoretically better algorithm can lose to a simpler contiguous scan on real data.
- Managed languages still run on hardware.
- Browser, VM, cloud, and serverless platforms hide hardware; they do not remove it.
- Measure first when possible, but know what to measure.

## When to use this skill
Use this skill for requests like:

- “Bu neden yavaş?”
- “Hangisi daha performanslı?”
- “Array mi dictionary mi?”
- “Big-O olarak hangisi iyi?”
- “Bu sorgu/loop/refactor performansı etkiler mi?”
- “Bunu optimize eder misin?”
- “Bu kod production’da sıkıntı çıkarır mı?”
- “Cache, memory, allocation açısından bak.”
- “React/.NET/SQL tarafında performans yorumu yap.”

## Review process

### 1. Find the hot path
Do not optimize random code. Identify:

- how often this runs
- expected input size
- worst realistic input size
- whether it is user-facing
- whether it blocks a request, render, job, transaction, or queue
- whether it is CPU-bound, memory-bound, IO-bound, network-bound, DB-bound, or lock-bound

If this information is missing, state assumptions and continue with a best-effort analysis.

### 2. Separate theoretical complexity from runtime cost
Give both:

- Algorithmic complexity: Big-O, when relevant.
- Runtime reality: locality, allocation, pointer chasing, hashing, branches, cache behavior, DB/network trips, serialization, garbage collection, framework overhead.

Never stop at Big-O if the user is asking about real performance.

### 3. Inspect data layout and access pattern
Look for:

- contiguous arrays/lists vs scattered object graphs
- tree/list node chasing
- repeated dictionary lookups
- repeated LINQ/enumeration allocations
- multiple passes over the same data
- N+1 database queries
- unnecessary materialization
- repeated JSON serialization/deserialization
- large DTO copying
- deep object mapping
- boxing/unboxing
- closure allocations
- unnecessary async state machines
- unnecessary defensive copying

### 4. Inspect branches and contracts
Look for:

- validation repeated inside tight loops
- polymorphic calls in hot paths
- generic abstractions that hide concrete behavior
- branches that never apply for this call path
- error handling in inner loops
- logging in hot loops
- reflection/dynamic dispatch where static shape is known

### 5. Consider platform-specific realities
For C#/.NET:

- LINQ readability vs allocations and multiple enumeration
- `List<T>` vs `IEnumerable<T>` when repeated traversal matters
- structs/classes and copying behavior
- async overhead in very small operations
- EF tracking vs no-tracking queries
- projection before materialization
- batching database calls
- `Span<T>`/memory APIs only when justified

For React/TypeScript:

- repeated renders
- unstable object/function identities
- expensive derived data in render
- large lists without virtualization
- state shape causing unnecessary tree updates
- network waterfalls
- serialization size

For SQL/database:

- indexes
- query plan
- cardinality
- N+1 patterns
- filtering on server vs client
- pagination
- transaction scope
- lock contention

For LLM/API workflows:

- token count
- repeated context loading
- unnecessary tool calls
- large prompt serialization
- repeated extraction of the same facts
- lack of caching for deterministic preprocessing

### 6. Recommend measurement
Give concrete verification steps:

- benchmark shape
- profiler to use
- metrics to capture
- production telemetry to check
- before/after comparison
- data size for test

Do not invent benchmark results. If no measurements exist, say “hypothesis”.

## Output format

### Performance Verdict
One of:

- Fine as-is
- Probably fine; measure only if hot
- Suspicious; profile this path
- Likely bottleneck
- Algorithmic issue
- Memory/access-pattern issue
- IO/database/network issue
- Abstraction overhead issue

### Hot Path Assumptions
- Frequency:
- Data size:
- User impact:
- Bound type:

### Big-O vs Real Runtime
| View | Finding |
|---|---|
| Big-O |  |
| Real runtime |  |

### Access Pattern Audit
| Area | Risk | Why it matters |
|---|---|---|
| Data layout |  |  |
| Allocation |  |  |
| Branching |  |  |
| IO/DB/network |  |  |
| Runtime/framework |  |  |

### Best First Optimization
Give the smallest useful optimization first.

### Measurement Plan
List exact checks or commands if possible.

### Do Not Optimize Yet
Mention what should not be touched unless profiling proves it matters.

## Style rules

- Prefer practical engineering language over academic performance talk.
- Do not shame high-level languages; reveal what they hide.
- Do not recommend C/C++ rewrites unless the user explicitly asks and the case is extreme.
- Prefer simple changes: fewer passes, better query, fewer allocations, better data shape, batching, caching, avoiding N+1.
- Keep the user focused on real bottlenecks.

## Example

### Input
“Tree ile logN search yapıyorum ama array scan daha hızlı çıktı. Mantıklı mı?”

### Output shape

### Performance Verdict
Memory/access-pattern issue. The tree has better theoretical complexity, but the array may win on realistic sizes because contiguous memory access is cheaper than pointer chasing.

### Big-O vs Real Runtime
| View | Finding |
|---|---|
| Big-O | Tree search is O(log n), scan is O(n). |
| Real runtime | Tree nodes may be scattered in memory; each step can miss cache. Array scan can stream contiguous memory. |

### Best First Optimization
Measure with realistic data sizes. If the array wins and the size is bounded, keep the array and document the reason.
