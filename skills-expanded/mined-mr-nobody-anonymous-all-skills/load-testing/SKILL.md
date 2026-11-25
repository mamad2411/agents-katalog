---
name: load-testing
description: "Plan and run load tests: SLO-derived targets, k6 scenarios, ramp profiles, percentile analysis and bottleneck attribution."
type: procedural
category: testing
domain: testing
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: medium
level: advanced
triggers:
  - k6 load test script
  - load test ramp profile
  - p95 latency regression
  - soak test plan
  - capacity planning test
keywords:
  - load-testing
  - k6
  - performance
  - percentiles
  - capacity
  - soak
source: custom
enabled: true
---

# Load Testing

## Purpose

Plan and run load tests: SLO-derived targets, k6 scenarios, ramp profiles, percentile analysis and bottleneck attribution.

## When to Use

- A release must be validated against a latency or throughput target.
- Capacity planning needs measured breaking points.
- A performance regression must be reproduced and attributed.

## When NOT to Use

- The environment cannot be isolated from real users.
- The target is unknown; define the SLO first.
- The bottleneck is clearly a single slow query that a microbenchmark can settle.

## Capabilities

- Derive test targets from SLOs rather than arbitrary request counts.
- Write k6 scenarios for smoke, load, stress and soak profiles.
- Read percentiles and error rates instead of averages.
- Attribute saturation to CPU, memory, I/O, locks or downstream calls.

## Inputs

- The SLO: target p95/p99 latency, throughput and acceptable error rate.
- The test environment's capacity and isolation guarantees.
- Realistic traffic mix and payload sizes from production telemetry.

## Workflow

1. Write the target down before running anything.
2. Start with a smoke test to validate the script and assertions.
3. Ramp gradually to the target load; watch saturation and error rates as you go.
4. Run a soak test at expected steady load to catch leaks.
5. Correlate results with server metrics to name the bottleneck.

## Tools

- k6 (or Locust/Gatling)
- Grafana / Prometheus for server metrics
- CI runner

## Examples

- `k6 run --vus 50 --duration 5m loadtest.js`
- `k6 run -e BASE_URL=https://staging.example smoke.js`
- `k6 run --out experimental-prometheus-rw loadtest.js`

## Safety

- Load-test only environments you are authorised to test; production tests need approval.
- Averages hide tail latency; always report p95/p99 and error rate together.
- Ramp-down matters: aborting a test can leave fixtures and connections behind.

## Source

All-Skills canonical library (`skills/testing/load-testing`). First-party skill, maintained in this repository.

## Notes

- `k6` thresholds fail the run automatically, which makes the test a gate.
- Test scenarios should reuse production traffic ratios, not uniform endpoints.
- Pairs with: `observability/slo-sli`, `testing/website-testing`.
