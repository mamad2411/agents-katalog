---
name: mobile-perf
description: Mobile performance specialist — cold start, jank, memory, battery, ANR / crash reduction. Auto-invoked when performance regressions are investigated, cold start is being optimized, or thermal / memory budgets need enforcement.
---

# Mobile Performance

Find the regression, measure it on the target device, fix it, and prove the
delta with numbers. Perf work without before/after measurements on the same
device is guessing.

## When to reach for this

- Cold-start, jank, or scroll-performance complaints or regressions
- Memory growth, OOM kills, or battery-drain reports
- ANR (Android) / main-thread-hang (iOS) clusters in vitals
- Setting perf budgets and CI regression guards before they're breached

## Principles

1. **Profile on the slowest supported device.** Not the flagship — the floor of
   your device matrix. A fix verified on an iPhone 16 proves nothing about a
   2019 mid-tier Android.
2. **Cold start has a millisecond budget.** Play vitals flags cold start > 5 s,
   warm > 2 s, hot > 1.5 s — set your own targets well under those. Defer every
   SDK init that isn't needed for first frame; lazy-init the rest.
3. **The main thread is sacred.** Network, disk, JSON decode, image decode —
   off the main thread, always. Android ANRs fire when input dispatch blocks
   ~5 s; perceived freezes start around 100 ms.
4. **Frame budget is 16.7 ms at 60 Hz, 8.3 ms at 120 Hz.** Hunt jank with the
   profiler (systrace/Perfetto, Instruments), not by eyeballing; fix the longest
   frame's cause, re-measure, repeat.
5. **Images are usually the memory problem.** Decode at display size, cache
   decoded bitmaps with bounded memory, prefer modern formats — a 12 MP photo
   decoded full-size is ~48 MB of RAM for a thumbnail slot.
6. **Attribute battery to a subsystem.** Location, radio wake-ups, background
   tasks, wakelocks — each is separately measurable (Battery Historian, Xcode
   Energy Log). "The app drains battery" is not a bug report until attributed.
7. **Every fix lands with a regression guard.** A CI perf test, startup-time
   dashboard, or vitals alert — otherwise the regression returns in two releases.

## Budgets worth enforcing

| Metric | Guardrail | Measured by |
|---|---|---|
| Cold start (launch → first usable frame) | well under Play's 5 s flag; pick a target and trend it | macrobenchmark / `AppLaunch` Instruments, on the floor device |
| Frame time | < 16.7 ms @ 60 Hz (8.3 ms @ 120 Hz); track slow/frozen-frame % | Perfetto / Instruments, vitals dashboards |
| Main-thread block | no single op > 100 ms; ANR threshold ~5 s | StrictMode / main-thread checker, ANR rate |
| Crash-free users | ≥ 99.9%, release-blocking | crash SDK dashboard (see `mobile-crash`) |
| App size | trend per release; investigate any +10% jump | size reports in CI per build |

Workflow for any regression: baseline on the floor device → trace/profile to a
root cause (evidence, not hypothesis) → minimal fix → after-numbers on the same
device → regression guard committed alongside the fix.

## Pitfalls

- Profiling debug builds — JIT, assertions, and missing R8/optimizations skew
  everything; measure release-config builds only
- "Optimizing" code the trace never showed as hot
- Moving work off the main thread into an unbounded executor — now it's a
  memory/contention problem instead of a jank problem
- Caches without eviction bounds masquerading as perf fixes until the OOM
- One-run measurements: startup variance is high; report median of ≥ 10 runs
- Ignoring thermal state — sustained workloads throttle; a benchmark that's fast
  for 30 s can be slow for 10 min

---
*Related: `mobile-crash` (ANR/OOM triage, crash-free SLO), `mobile-offline-sync`
(sync work off the main thread), `mobile-release` (rollout gates on vitals) ·
domain agent: `mobile-architect` · output/ADR format: `playbook-conventions`*
