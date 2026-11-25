---
name: swift-performance-engineering
description: Design, generate, modify, refactor, and review Swift and iOS code with performance as a first-class constraint. Use whenever an agent is writing new Swift code, editing existing Swift or SwiftUI/UIKit code, implementing features in iOS projects where startup time, UI responsiveness, memory use, battery, throughput, or concurrency matter, or performing Swift performance reviews, code reviews, profiling follow-up, startup analysis, rendering investigation, allocation analysis, or threading and contention diagnosis.
---

# Swift Performance Engineering

## Overview

Use this skill to shape Swift, SwiftUI, UIKit, and iOS code while it is being designed, generated, modified, or reviewed. Optimize for lower CPU time, fewer allocations, tighter memory behavior, faster startup, less main-thread work, smoother rendering, and lower contention without trading away correctness or maintainability.

## Working Mode

Start with the execution path the user cares about: launch, first render, scrolling, animation, networking, persistence, background work, or a specific regression.

Use this skill in two modes:

- `Build mode`: when generating or modifying Swift code. Design the code to avoid predictable performance problems before they are introduced.
- `Review mode`: when auditing existing code or profiler output. Identify and prioritize bottlenecks and cleanup opportunities.

Treat claims in one of three buckets:

- `Measured`: Backed by profiler output, metrics, traces, or a reproducible benchmark.
- `Likely`: Strongly implied by code structure and known platform behavior.
- `Possible`: Plausible but not yet verified. Keep these clearly labeled.

Prefer changes that:

- Remove work instead of relocating it.
- Reduce repeated allocations, copying, diffing, decoding, layout, or synchronization.
- Move non-UI work off the main actor without breaking isolation or ordering guarantees.
- Tighten lifecycle ownership so expensive resources are created once and released predictably.

## Workflow

1. Identify the hottest path or likely-sensitive path before writing code.
2. Read the relevant code and trace object lifetimes, thread hops, data movement, invalidation scope, and rendering triggers.
3. Apply the checklist in [references/review-checklist.md](references/review-checklist.md).
4. If you are generating or editing code, incorporate the checklist into the implementation, not as a post-pass.
5. If you need citations or current platform guidance, load [references/official-performance-sources.md](references/official-performance-sources.md) and ground advice in current Apple or Swift sources.
6. When reviewing, return findings ordered by impact: startup, frame drops, contention, memory pressure, battery, then cleanup opportunities.
7. For every recommendation or code change, state the expected win, the tradeoff, and how to verify it with Instruments, benchmarks, or production telemetry.

## Build Rules

When writing or modifying code, apply these rules by default:

- Keep expensive work out of `body`, cell configuration, view lifecycle callbacks, and launch paths unless the feature strictly requires it.
- Reuse expensive helpers and shared resources when configuration is stable.
- Choose data structures and ownership patterns before writing loops and transforms.
- Avoid main-actor work for parsing, decoding, image preparation, persistence, and other non-UI computation.
- Design cancellation, batching, caching, and lazy initialization into the first implementation when the feature is latency-sensitive.
- Prevent accidental quadratic work, repeated diffing, repeated decoding, and avoidable copy-on-write before it lands in the codebase.
- If a simpler implementation is slightly slower but clearly outside any hot path, keep it simple and note that the path is not performance critical.

## Core Standards

Apply these standards by default:

- Favor stable, measurable improvements over speculative micro-optimizations.
- Keep hot paths allocation-light, branch-light, and synchronization-light.
- Do not create work on the main thread that can be prepared, cached, batched, or deferred.
- Prefer the simplest data structure that matches lookup, mutation, ordering, and memory needs.
- Avoid hidden copying, repeated formatting, repeated decoding, and repeated view recomputation.
- Use structured concurrency and actor isolation deliberately; do not introduce gratuitous task creation or actor hopping.
- Align performance fixes with quality gates: correctness, testability, readability, lifecycle safety, and observability.

## Focus Areas

Always inspect these areas when relevant:

- Object creation discipline: repeated formatter creation, per-cell view model creation, transient wrapper objects, unnecessary boxing, repeated `Task` or closure allocation, avoidable bridging to Foundation.
- Resource lifecycle safety: caches without eviction, observers/timers not invalidated, tasks that outlive owners, images/data loaded too early, expensive singletons initialized on launch.
- Loop and hot-path efficiency: nested loops, repeated sorting/filtering/mapping in render or scroll paths, repeated date/number formatting, repeated regex/JSON decoding, redundant copy-on-write triggers.
- Data-structure fit: `Array.contains` where `Set` or dictionary lookup matches usage, ordered collections used where hashing is appropriate, large value types copied repeatedly, `String`/`Data` slicing and bridging mistakes.
- Algorithmic efficiency: accidental quadratic work, repeated whole-collection diffs, N+1 fetches, redundant layout passes, avoidable database or disk churn.
- Memory management: retain cycles, large temporary buffers, autorelease-heavy bridging, image inflation, cache growth, actor/task retention chains.
- Concurrency and threading: main-actor overuse, priority inversions, lock contention, serial queue bottlenecks, unbounded task fan-out, cancellation ignored, data races hidden behind `nonisolated` or unsafe shared state.
- UI rendering and responsiveness: expensive `body` recomputation, unstable identity in SwiftUI lists, synchronous image decoding, layout thrash, work in lifecycle callbacks that blocks first interaction, repeated diffing or invalidation.
- Startup and first-frame time: eager dependency construction, synchronous disk/network work, migration or logging work in launch path, oversized initial view models, work that can move behind first frame.

## Output Format

When reviewing code, report findings in this shape:

1. `Issue`: concise statement of the bottleneck or risk.
2. `Why it matters`: user-visible impact or systems impact.
3. `Evidence`: measured, likely, or possible.
4. `Recommendation`: the smallest credible change.
5. `Verification`: Instruments view, benchmark, metric, or regression test to run.

If nothing is clearly wrong, say so explicitly and list residual risks or missing measurements.

When generating or modifying code, also explain:

1. `Performance-sensitive choices`: data structures, ownership, caching, batching, or concurrency decisions baked into the implementation.
2. `Risk avoided`: the bottleneck or anti-pattern prevented by the design.
3. `Verification`: what should be profiled or benchmarked after the change lands.

## Evidence Expectations

- Prefer official Apple Developer and Swift documentation when justifying platform-specific advice.
- If a recommendation depends on a moving platform detail, verify against current official docs at the time of the review.
- When profiling is missing, say what should be measured before approving a risky refactor.
- Do not promise wins you cannot explain mechanically.

## Agent Compatibility

Keep the workflow tool-agnostic so it works in Codex, Claude Code, Cursor, and similar agents:

- Do not rely on vendor-specific commands or UI affordances.
- Use repo-local tooling when available, otherwise reason directly from source.
- Cite official docs with plain links or titles so any agent can reuse them.
- Keep recommendations actionable even when Instruments screenshots or traces are unavailable.

## References

- Review checklist: [references/review-checklist.md](references/review-checklist.md)
- Official grounding: [references/official-performance-sources.md](references/official-performance-sources.md)
