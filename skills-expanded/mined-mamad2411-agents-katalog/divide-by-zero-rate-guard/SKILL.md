---
tags: [backend, divide, zero, rate, guard]
name: divide-by-zero-rate-guard
description: Guard rate/percentage calculations against zero denominators to prevent NaN from poisoning downstream metrics and serialization.
trigger: Computing errorRate / successRate / cacheHitRatio / any num/den metric; seeing NaN in dashboards or JSON serialization errors.
source_project: lucida-domain-apm
version: 1.0.0
category: backend
---

# Divide-by-Zero Rate Guard

Rate and percentage metrics (`errorRate`, `successRate`, `cacheHitRatio`, …) must check for a zero denominator before dividing.

## Why

In Java, integer `x/0` throws; double `x/0.0` yields `NaN` or `±Infinity`. `NaN` then propagates silently through `sum`, `avg`, and other aggregates, corrupting downstream metrics, and serializes as `"NaN"` in JSON — which many clients reject outright. The bug usually surfaces only when a new or idle tenant has zero traffic in a bucket, so early tests miss it.

## Pattern

```java
double errorRate = (servicedCount != 0)
        ? ((double) errorCount / servicedCount) * 100.0
        : 0.0;
```

Helper form:

```java
static double safeRate(long num, long den) {
    return den == 0 ? 0.0 : (double) num / den;
}
```

## Steps

1. Identify every rate/percentage field in the aggregation.
2. Wrap each division with an explicit zero-denominator check.
3. Unit-test the zero-traffic bucket — most "NaN in dashboard" bugs ship because no test covers the empty case.
4. If upstream values can themselves be `NaN`, guard at the source, not just at the last division.

## Counter / Caveats

- Returning `0.0` is a choice. For some metrics `null` is more honest: "no data" ≠ "0%". Pick per metric, and document in the DTO comment.
- In reactive pipelines, one `NaN` element can poison a `reduce`/`collect` — guard at the producer, not only at the consumer.
- Beware doubles summed from other doubles that are already `NaN` — one guard doesn't protect the chain.
