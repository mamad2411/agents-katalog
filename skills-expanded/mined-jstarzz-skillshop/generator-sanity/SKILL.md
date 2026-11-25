---
name: generator-sanity
description: "Prove the load generator and network are not the bottleneck before attributing a throughput ceiling to the system under test. Use when load generator bottleneck, RPS plateau, network ceiling."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "performance"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Generator Sanity

Prove the load generator and network are not the bottleneck before attributing a throughput ceiling to the system under test.

## Activate when

- load generator bottleneck
- RPS plateau
- network ceiling

## Focus

- Primary mission: Prove the load generator and network are not the bottleneck before attributing a throughput ceiling to the system under test.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Measure generator CPU, scheduler delay, memory, socket errors, connection reuse and backpressure before blaming the target.
2. Check NIC/link bandwidth, packet rate, ephemeral ports, file descriptor limits and kernel/socket constraints.
3. Compare scheduled, started and completed requests; divergence is generator evidence.
4. Run a known-simple local/lab target to establish per-worker generator ceiling.
5. Scale worker count and verify aggregate generation rises approximately as expected before claiming distributed headroom.
6. Check synchronized start and clock assumptions for multi-worker experiments.
7. Only attribute the observed load knee to the system under test after generator and network headroom are demonstrated.

## Deliverables

- Reproducible measurement protocol
- Results with achieved rates/distributions/resources
- Bottleneck or capacity conclusion with limitations
- A result that directly satisfies: Prove the load generator and network are not the bottleneck before attributing a throughput ceiling to the system under test.

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
