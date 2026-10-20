---
name: concurrency-and-thread-safety
version: 1.0.0
description: Intra-process concurrency hazards — race conditions, deadlock, thread safety, async/await pitfalls, and memory visibility. Use whenever software-engineer writes code with shared mutable state, multiple threads/workers, or async code, and whenever qa-engineer or performance-engineer investigates a race condition or lock contention. Do NOT use for cross-process concerns — network failure, consistency models, ordering across services — that is `distributed-systems`; this skill is what happens inside one process.
---

# Concurrency and Thread Safety

## The core hazards
- **Race condition** — outcome depends on the relative timing of two or more operations that should be independent. The defining symptom: it works almost always, and fails under load, under a specific interleaving, or only in production — never reliably in a quick manual test.
- **Deadlock** — two or more threads each hold a resource the other needs and neither releases. Classic cause: acquiring the same set of locks in inconsistent order across different code paths. Prevention: establish and enforce a single global lock-ordering convention; never acquire locks in an order that could differ between call sites.
- **Livelock** — threads actively responding to each other but making no progress (e.g., both back off and retry in lockstep forever). Looks alive in monitoring; isn't.
- **Starvation** — a thread is perpetually denied a resource because others are prioritized ahead of it, even without deadlock.

## Memory visibility
A value written by one thread isn't guaranteed to be visible to another thread without an explicit synchronization point (a lock, an atomic operation, a memory barrier, a language-level guarantee like `volatile` or its equivalent). This is a different failure from a race condition on the same variable — it's possible for two threads to never even see the same value at the same time, independent of ordering. "It works on my machine" often hides exactly this: a single-core or lightly-loaded environment masks visibility bugs that a multi-core, heavily-loaded one exposes.

## Async/await pitfalls
Async code removes some concurrency hazards and introduces its own:
- **Fire-and-forget** — starting an async operation without awaiting or otherwise tracking it. Its failure is silently lost, and its side effects race against whatever runs next.
- **Unhandled rejection/exception in an async task** — depending on the runtime, this can crash the process, be silently swallowed, or surface far from where it actually happened.
- **Accidental sequential execution** — `await` inside a loop, one iteration at a time, when the operations were intended to run concurrently. This isn't a correctness bug, but it's a common and quiet performance one (see `debugging-methodology` for how to actually localize why something intended to be concurrent isn't).
- **False concurrency** — async/await describes non-blocking I/O interleaving, in many runtimes on a single thread; it is not automatically parallelism. Code that assumes true simultaneous execution across cores because it's written with `async` will be wrong on that assumption specifically.

## Testing and detecting concurrency bugs
- A concurrency bug that doesn't reproduce on the first several runs is not confirmed absent — race conditions are probabilistic, not deterministic, and "it passed" is much weaker evidence here than for ordinary logic.
- Prefer tooling built for this: thread/race sanitizers, deterministic scheduling/interleaving-exploration tools where the language ecosystem has them, and stress/soak tests that run the suspect path under sustained concurrent load rather than a single pass.
- When a race is suspected but not yet reproduced, don't fix speculatively — increase the odds of reproduction first (more concurrent load, artificially widened timing windows, forced interleaving if tooling allows), confirm via `debugging-methodology`'s hypothesis-and-falsify discipline, then fix.

## Design preferences that reduce hazard surface
- Prefer immutable data and message-passing over shared mutable state where the language/framework makes it practical — most concurrency bugs require mutable state shared across threads to exist at all.
- Keep lock scope as narrow as possible, and hold at most one lock at a time where feasible — every additional simultaneously-held lock multiplies deadlock-ordering risk.
- Prefer well-tested concurrency primitives (queues, atomics, established concurrent collections) over hand-rolled locking — a hand-rolled double-checked-locking pattern or a custom lock-free structure is exactly the kind of code that looks correct on inspection and fails only under real contention.
