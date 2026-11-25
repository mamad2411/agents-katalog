---
name: take-my-load-operator
description: "Operate Take My Load safely for distributed capacity-aware tests with authorization, synchronized workers and generator sanity checks. Use when take-my-load, distributed load generation, multi-worker load."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "performance"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Take My Load Operator

Operate Take My Load safely for distributed capacity-aware tests with authorization, synchronized workers and generator sanity checks.

## Activate when

- take-my-load
- distributed load generation
- multi-worker load

## Focus

- Primary mission: Operate Take My Load safely for distributed capacity-aware tests with authorization, synchronized workers and generator sanity checks.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Confirm the target is explicitly authorized and matches the controller's default-deny host/CIDR policy.
2. Inspect registered workers, heartbeat freshness and aggregate usable capacity; stale workers must not count.
3. Discover actual engine capabilities from the deployed binary/version instead of assuming roadmap features exist.
4. Create an immutable plan containing target, engine, requested rate/concurrency, duration, scenario, data and stop conditions.
5. Use coordination simulation before first real execution on a new topology or after meaningful control-plane changes.
6. Execute through the controller so capacity-aware sharding, ready barriers, synchronized `start_at`, cancellation and failure propagation remain intact.
7. Observe scheduled/started/completed/failed counts, achieved rate, backpressure, latency/status summaries and worker/network headroom.
8. Never interpret the platform planning ceiling or the 1M-RPS architecture target as a benchmark result; validate capacity on appropriate hardware and network.
9. Store controller/worker/engine versions plus the exact plan with every result.

## Deliverables

- Reproducible measurement protocol
- Results with achieved rates/distributions/resources
- Bottleneck or capacity conclusion with limitations
- A result that directly satisfies: Operate Take My Load safely for distributed capacity-aware tests with authorization, synchronized workers and generator sanity checks.

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
