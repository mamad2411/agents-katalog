---
name: android-performance-profiling
description: |
  Android performance and profiling patterns - startup analysis, baseline profiles, recomposition tracking, jank reduction, memory checks, and measurement-first optimization. Use this skill whenever diagnosing slow startup, dropped frames, excessive recomposition, memory pressure, or deciding how to profile before optimizing. Trigger on phrases like "performance", "profiling", "startup", "baseline profile", "jank", "recomposition", "memory leak", or "slow screen".
---

# Android Performance and Profiling

## Core Principles

- Measure first, optimize second.
- Fix the highest-impact bottleneck before micro-optimizing.
- Prefer repeatable profiling workflows over intuition.
- Performance work must preserve correctness and maintainability.
- Regressions should be caught with tooling where practical.

---

## What to Measure

Focus on the metrics that matter most:

| Concern | Typical signal |
|---|---|
| App startup | cold / warm / hot startup time |
| UI smoothness | jank, frame time, skipped frames |
| Compose work | unnecessary recomposition, unstable state |
| Memory | growth, leaks, churn, GC pressure |
| Disk / network | blocking work on main, oversized payloads |
| Build/runtime optimization | baseline profile and release performance |

---

## Startup Performance

Startup work should be minimal and intentional.

Guidelines:
- avoid heavy synchronous work in `Application`
- defer non-critical initialization
- initialize analytics, logging, and background work lazily when possible
- do not open database/network just because the app launched unless needed immediately

A good startup review asks:
- what must happen before first frame?
- what can wait until after first draw?
- what can wait until the related feature is opened?

---

## Baseline Profiles

Use baseline profiles to improve release startup and navigation performance.

Guidelines:
- generate profiles from critical user journeys
- keep them focused on startup and key flows
- validate benefits on release-like builds
- regenerate when major flows or dependencies change

Baseline profiles are most useful when the app has meaningful startup or navigation cost in production builds.

---

## Compose Performance

Common rules:
- keep state minimal and stable
- avoid passing unstable containers carelessly
- move business/data transformation out of composables
- avoid expensive work during recomposition
- prefer lazy layouts for long lists

Typical checks:
- is a composable recomposing more often than expected?
- is a large state object causing broad invalidation?
- are animations causing recomposition unnecessarily?

See the **android-compose-ui** skill for concrete Compose guidance.

---

## Main-Thread Discipline

Never do blocking disk, network, or CPU-heavy work on the main thread.

Examples of common violations:
- JSON parsing on main
- bitmap processing on main
- synchronous database access on main
- expensive collection transforms in UI callbacks

Move blocking work to the owning dispatcher. See the **android-coroutines-flow** skill.

---

## Scrolling and List Performance

For list-heavy screens:
- provide stable item keys when appropriate
- avoid nested expensive layouts per row
- avoid loading or formatting too much per item on every bind/recompose
- precompute UI-ready models when helpful
- keep image loading efficient and size-aware

---

## Memory and Leak Checks

Look for:
- retained screens or ViewModels that should be gone
- long-lived references to `Context`, `Activity`, or views
- growing caches without eviction rules
- repeated allocations in hot UI paths

Guidelines:
- avoid storing `Activity` references in long-lived classes
- keep caches bounded
- release listeners/observers when lifecycles end

---

## Data and Network Efficiency

Performance issues are often data-shape problems:
- oversized responses
- repeated identical requests
- loading more than the UI needs
- poor offline strategy causing unnecessary refreshes

Prefer:
- paged or incremental loading when datasets grow large
- Room-backed observation for offline-first screens
- cached or deduplicated fetches where appropriate

---

## Profiling Workflow

A practical workflow:
1. reproduce the issue on a realistic build/device
2. measure with profiler/tracing tools
3. identify the dominant bottleneck
4. fix one thing at a time
5. re-measure
6. document the regression guard if needed

Do not merge performance changes that only "feel faster" without evidence when the issue is non-trivial.

---

## Release vs Debug

Do not judge final performance from debug builds alone.

Important rules:
- verify on release or release-like builds
- benchmark startup-sensitive changes realistically
- validate baseline profile effects in non-debug variants

---

## What to Optimize First

Usually best first targets:
- startup blockers
- janky critical screens
- repeated unnecessary recomposition
- large image or list inefficiencies
- obvious leaks and unbounded caches

Usually poor first targets:
- tiny helper functions with no measured impact
- abstract "cleanups" without a metric
- premature threading complexity

---

## Checklist: Performance Work

- [ ] Reproduce the issue with a measurable signal
- [ ] Confirm whether startup, UI, memory, or data flow is the bottleneck
- [ ] Measure on a realistic build/device
- [ ] Fix the highest-impact bottleneck first
- [ ] Re-measure after the change
- [ ] Add a guardrail such as a profile, benchmark, or review note if needed