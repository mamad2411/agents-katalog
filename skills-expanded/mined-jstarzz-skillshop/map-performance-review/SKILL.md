---
name: map-performance-review
description: "Review interactive map rendering, layers, markers, data updates and geospatial payloads for smooth constrained-device performance. Use when map performance, MapLibre, many markers."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "performance"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Map Performance Review

Review interactive map rendering, layers, markers, data updates and geospatial payloads for smooth constrained-device performance.

## Activate when

- map performance
- MapLibre
- many markers

## Focus

- Primary mission: Review interactive map rendering, layers, markers, data updates and geospatial payloads for smooth constrained-device performance.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Define the performance question, workload, target metrics, SLOs, environment, data shape, and stop conditions before measuring.
2. Establish a reproducible low-load or pre-change baseline.
3. Measure both the system under test and the measurement/generator side so attribution is possible.
4. Change load or implementation one controlled dimension at a time.
5. Record achieved throughput/concurrency, latency distribution, errors, saturation, and relevant resource telemetry together.
6. Locate the first bottleneck or dominant cost using profiles/plans/traces rather than optimizing by intuition.
7. Repeat comparable measurements after changes and report variance, limitations, and sustainable—not fantasy—capacity.

## Deliverables

- Reproducible measurement protocol
- Results with achieved rates/distributions/resources
- Bottleneck or capacity conclusion with limitations
- A result that directly satisfies: Review interactive map rendering, layers, markers, data updates and geospatial payloads for smooth constrained-device performance.

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
