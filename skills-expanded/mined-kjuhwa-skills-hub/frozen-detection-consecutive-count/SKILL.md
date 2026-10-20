---
tags: [backend, frozen, detection, consecutive, count]
name: frozen-detection-consecutive-count
description: Detect a stuck/frozen metric (identical value for N consecutive samples) by CONSECUTIVE-dampening equality check; catches sensor/collector failures that threshold alarms miss.
trigger: Collector reports a valid-looking but unchanging value (flatline) that static thresholds never alert on.
source_project: lucida-alarm
version: 1.0.0
category: backend
---

# Frozen-Value Detection (Consecutive Equality)

## Shape

`FrozenCondition(evaluationCount=N)` with the `dampeningType = CONSECUTIVE` invariant enforced in the constructor. On evaluation, read the N most recent samples in order; alarm if all N equal.

## Steps

1. Define entity with `evaluationCount` (default 5).
2. Constructor asserts `dampeningType = CONSECUTIVE`; any other value is misconfiguration.
3. On each evaluation, fetch the N most recent samples (ordered newest-first or oldest-first, consistent).
4. If `samples.size() < evaluationCount` → return empty (warm-up).
5. Iterate `samples[1..N-1]` vs `samples[0]`; mismatch → not frozen.
6. All equal → emit alarm: `frozen[metric=X, value=V, count=N]` with severity.
7. Persist frozen state in Redis keyed by `(confId, measurementId)` with TTL; clear on any value change.

## Counter / Caveats

- For float metrics, use an epsilon comparison (`abs(a-b) < eps`), not `==`, or the first floating noise sample clears the alarm falsely.
- The `CONSECUTIVE` invariant must be enforced by code, not just docs — it drifts otherwise.
- Integer collectors that report a cached value until a refresh can look frozen on short windows; size `N` against your collector cadence.
- Consider also firing on "exactly-repeating short sequences" if the collector has a known stale-cache bug.
