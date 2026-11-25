---
name: container-review
description: "Review container images and runtime configuration for reproducibility, size, permissions, signals, health and secret handling. Use when Dockerfile, container image, container runtime."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "reliability"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Container Review

Review container images and runtime configuration for reproducibility, size, permissions, signals, health and secret handling.

## Activate when

- Dockerfile
- container image
- container runtime

## Focus

- Primary mission: Review container images and runtime configuration for reproducibility, size, permissions, signals, health and secret handling.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Identify the critical workflow, authoritative state, dependencies, and recovery objective.
2. Enumerate realistic failure modes: timeout, partial success, duplicate delivery, process loss, stale state, overload, dependency outage, and operator error.
3. Define bounded failure behavior, timeouts, retries, idempotency, backpressure, and recovery semantics where relevant.
4. Verify telemetry can distinguish local failure from dependency or infrastructure failure.
5. Exercise at least one representative failure or recovery path when tools/environment make that safe.
6. Check whether restart, retry, failover, or rollback can leave duplicate work, corrupted state, or stuck lifecycle state.
7. Return operationally prioritized gaps with evidence and a concrete recovery or hardening path.

## Deliverables

- Failure/recovery findings
- Operational gaps ranked by impact
- Verification or drill evidence where available
- A result that directly satisfies: Review container images and runtime configuration for reproducibility, size, permissions, signals, health and secret handling.

## Common failure modes

- Infinite retries or unbounded queues
- Failover claims with no recovery exercise
- Liveness checks that kill healthy-but-dependent processes
- Hiding uncertainty instead of stating what was not inspected, reproduced, measured, or verified.

## Composition

Use `skill-router` when this task needs multiple specialties. Prefer composition over copying another skill's workflow into this one.

## Exit criteria

- The requested decision, change, test, or review is supported by concrete evidence.
- Important residual risks, limitations, and unknowns are explicit.
- The output is specific enough for another engineer or agent to act on without reconstructing hidden reasoning.
