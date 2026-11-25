---
name: "performance-test-planner"
pack: "non-functional-testing-pack"
purpose: "Plan performance testing around response time, throughput, resource usage, bottlenecks, and realistic workloads."
inputs: ["system context", "performance goals", "critical user journeys", "environment constraints"]
outputs: ["performance test plan", "workload model", "metrics list", "risk notes"]
handoffs: ["load-test-scenario-writer", "stress-test-scenario-writer", "observability-driven-test-planner"]
---
# performance-test-planner

## Purpose
Plan performance testing around response time, throughput, resource usage, bottlenecks, and realistic workloads.

## Trigger this skill when
- You need this specific non-functional planning or review task rather than a broad testing request.
- You want explicit artifacts, thresholds, and evidence expectations.
- You need an output another agent or developer can execute or extend safely.

## Expected inputs
- system context
- performance goals
- critical user journeys
- environment constraints

## Deliverables
- performance test plan
- workload model
- metrics list
- risk notes

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
- load-test-scenario-writer
- stress-test-scenario-writer
- observability-driven-test-planner

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
