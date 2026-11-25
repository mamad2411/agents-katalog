---
name: load-test
description: "Design, execute and interpret realistic authorized load tests using traffic models, explicit SLOs, progressive ramps and system telemetry. Use when load test, capacity validation, performance before release."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "performance"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Load Test

Design, execute and interpret realistic authorized load tests using traffic models, explicit SLOs, progressive ramps and system telemetry.

## Activate when

- load test
- capacity validation
- performance before release

## Focus

- Primary mission: Design, execute and interpret realistic authorized load tests using traffic models, explicit SLOs, progressive ramps and system telemetry.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Confirm the target is owned or explicitly authorized for testing.
2. Identify critical user journeys, traffic mix, data cardinality and whether arrival-rate or closed-user modeling matches reality.
3. Define SLOs and stop conditions before generating significant traffic: latency percentiles, error rate, saturation, and safety thresholds.
4. Establish a low-load baseline and validate test data/authentication behavior.
5. Ramp progressively through baseline, expected peak and stress/breakpoint profiles; use separate soak or spike experiments for those questions.
6. Monitor the system under test and the load generator: CPU, memory, network, DB/pools, queues, GC/runtime, scheduled vs started vs completed requests and backpressure.
7. Report achieved—not requested—throughput/concurrency with p50/p95/p99, errors and resource saturation.
8. Identify the first bottleneck, change one thing, rerun a comparable profile, and preserve the full plan/result for regression analysis.

## Deliverables

- Reproducible measurement protocol
- Results with achieved rates/distributions/resources
- Bottleneck or capacity conclusion with limitations
- A result that directly satisfies: Design, execute and interpret realistic authorized load tests using traffic models, explicit SLOs, progressive ramps and system telemetry.

## Common failure modes

- Reporting requested RPS as achieved RPS
- Optimizing before establishing a benchmark/profile
- Blaming the target before proving generator/network headroom
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
