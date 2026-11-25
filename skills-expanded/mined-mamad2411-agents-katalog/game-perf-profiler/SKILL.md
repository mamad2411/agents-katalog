---
name: game-perf-profiler
description: Frame-budget and performance specialist. Auto-invoked when frame time, draw calls, GC, memory bandwidth, CPU/GPU bottlenecks, or platform-specific performance regressions need investigation.
---

# Game Performance Profiling

Frame-time work is measurement work: find the regression, prove the bottleneck,
fix it, and prove the fix with numbers. Optimizations without a before/after pair
are guesses wearing a lab coat.

## When to reach for this

- Frame time over budget, or a hitch/spike players can feel
- A perf regression appeared and the offending change needs bisecting
- Setting or enforcing per-subsystem frame budgets
- Memory pressure: texture budgets, resident set, GC churn

## Principles

1. **Measure first, change second.** No optimization lands without a baseline
   capture and an after-capture from the same scene on the same hardware.
2. **Find the bottleneck class before tuning.** CPU-bound, GPU-bound,
   bandwidth-bound, or thermal-throttled each demand a different fix — a GPU
   optimization on a CPU-bound frame changes nothing. Check whether the render
   thread is waiting on the GPU (or vice versa) before touching code.
3. **The slow frame, not the average.** Players notice the 99th-percentile frame
   and hitches; report p50/p95/p99 frame time, never just the mean.
4. **Budgets per subsystem, in milliseconds.** At 60 fps the whole frame is
   16.6 ms (33.3 ms at 30, 8.3 ms at 120). Give rendering, simulation, audio, and
   scripting explicit slices and enforce them in CI or nightly captures.
5. **Test on target hardware.** Editor-on-desktop is not the platform. Profile the
   weakest device in the support matrix, and on mobile profile *warm* — thermal
   throttling after 10–15 minutes is the real performance envelope.
6. **Allocation is a frame cost.** Per-frame allocations feed GC spikes; hot paths
   should be zero-alloc, with pools for anything spawned at gameplay rate.

## Investigation workflow

| Step | Tool / action | Output |
|---|---|---|
| 1. Reproduce | fixed scene/replay on target hardware | deterministic capture scenario |
| 2. Baseline | engine profiler (Unity Profiler, Unreal Insights) | p50/p95/p99 frame time, thread timeline |
| 3. Classify | GPU capture (RenderDoc, PIX, Xcode/Instruments, AGI) vs. CPU timeline | bound-by verdict with evidence |
| 4. Bisect (if regression) | binary search commits with the step-2 scenario | offending change |
| 5. Fix | smallest change addressing the proven bottleneck | diff |
| 6. Prove | re-run step 2 identically | before/after table |
| 7. Guard | perf test or tracked metric on the capture scenario | regression alarm |

Skipping step 3 is the most common failure: weeks of micro-optimizing C# while the
frame was waiting on GPU fill rate.

## Pitfalls

- Profiling a development/debug build — instrumentation overhead distorts the
  ranking; verify findings in a release-like build
- Reporting averages that hide a 100 ms hitch every few seconds
- Draw-call counting on hardware where the actual limit is overdraw/fill rate (most mobile)
- Cold-device mobile numbers — the thermally throttled steady state is what players get
- "Optimizing" by toggling settings until it feels faster, with no capture either side
- No regression guard, so the win silently evaporates within three sprints

---
*Related: `game-engine` (engine-idiomatic fixes the profile demands), `game-audio`
(audio CPU/memory budgets), `game-netcode` (bandwidth is profiled separately) ·
domain agent: `game-architect` (platform-target matrix) · output/ADR format:
`playbook-conventions`*
