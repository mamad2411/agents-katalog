---
name: production-readiness
description: "Gate production launch on configuration, migrations, reliability, observability, backup, rollback, security and verified critical journeys. Use when production readiness, launch review, go live."
license: MIT
compatibility: "Agent Skills compatible hosts; optimized for coding agents with repository and test/tool access."
metadata:
  category: "reliability"
  version: "0.1.0"
  maintainer: "SkillShop maintainers"
  maturity: "draft"
---

# Production Readiness

Gate production launch on configuration, migrations, reliability, observability, backup, rollback, security and verified critical journeys.

## Activate when

- production readiness
- launch review
- go live

## Focus

- Primary mission: Gate production launch on configuration, migrations, reliability, observability, backup, rollback, security and verified critical journeys.
- Use project/runtime evidence; this skill is a workflow, not a role-play persona.
- If another skill owns a deeper specialist concern, hand off instead of duplicating its entire workflow.

## Workflow

1. Identify critical data paths, dependencies, actors and launch SLOs.
2. Verify environment configuration, secrets, least privilege, migrations and mixed-version compatibility.
3. Check health/readiness, graceful shutdown, timeouts, retries, idempotency, rate/resource limits and failure behavior.
4. Verify structured logs, useful metrics/traces, alert ownership and a workable 2AM diagnosis path.
5. Confirm backup/restore assumptions and rollback or forward-fix strategy.
6. Run release-candidate QA on the exact artifact and select security/performance checks proportional to risk.
7. Distinguish launch blockers from follow-up hardening; do not pass a ceremonial checklist with missing evidence.
8. Return go, conditional-go or no-go with evidence and explicit residual risk.

## Deliverables

- Failure/recovery findings
- Operational gaps ranked by impact
- Verification or drill evidence where available
- A result that directly satisfies: Gate production launch on configuration, migrations, reliability, observability, backup, rollback, security and verified critical journeys.

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
