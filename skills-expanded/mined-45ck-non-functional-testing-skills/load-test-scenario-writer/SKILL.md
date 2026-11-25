---
name: "load-test-scenario-writer"
pack: "non-functional-testing-pack"
purpose: "Design load scenarios that represent expected and peak traffic, concurrency, and transaction mix for the system."
inputs: ["system context", "expected load profile", "critical transactions", "acceptance thresholds"]
outputs: ["load scenarios", "ramp profile", "pass/fail thresholds", "monitoring checklist"]
handoffs: ["performance-test-planner", "soak-test-planner", "nfr-evidence-matrix-builder"]
---
# load-test-scenario-writer

## Purpose
Design load scenarios that represent expected and peak traffic, concurrency, and transaction mix for the system.

## Trigger this skill when
- You need this specific non-functional planning or review task rather than a broad testing request.
- You want explicit artifacts, thresholds, and evidence expectations.
- You need an output another agent or developer can execute or extend safely.

## Expected inputs
- system context
- expected load profile
- critical transactions
- acceptance thresholds

## Deliverables
- load scenarios
- ramp profile
- pass/fail thresholds
- monitoring checklist

## Operating procedure
1. Clarify the target non-functional concern, the system boundary, and what would count as evidence.
2. Translate vague goals into measurable metrics, thresholds, and observation points.
3. Make assumptions, environmental constraints, and known blind spots explicit.
4. Produce a compact artifact that can drive test execution or quality review.

## Quality gates
- Prefer realistic workloads and failure modes over synthetic but meaningless coverage.
- Tie every scenario to an observable outcome and measurement method.
- State thresholds, assumptions, and residual risks explicitly.
- Do not hide missing telemetry or environment limitations.

## Handoff targets
- performance-test-planner
- soak-test-planner
- nfr-evidence-matrix-builder

## Output style
- Be explicit about uncertainty, infeasibility, and residual risk.
- Prefer compact, explainable artifacts over bloated plans.
- Make pass/fail logic and evidence expectations obvious.
- Keep scenarios tied to user impact, system behavior, or operational risk.

## Failure modes to avoid
- Do not produce non-functional plans with no measurable thresholds.
- Do not assume production-like behavior without naming environment gaps.
- Do not bury required telemetry, instrumentation, or recovery assumptions.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Metrics / thresholds
## Assumptions
## Open questions
## Recommended next skill
```
