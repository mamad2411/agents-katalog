---
name: "resilience-test-planner"
pack: "non-functional-testing-pack"
purpose: "Plan resilience testing around dependency failures, retries, timeouts, degraded modes, and recovery behavior."
inputs: ["system architecture", "external dependencies", "failure assumptions", "recovery expectations"]
outputs: ["resilience test plan", "failure injection matrix", "expected degraded modes", "recovery criteria"]
handoffs: ["stress-test-scenario-writer", "observability-driven-test-planner", "nfr-evidence-matrix-builder"]
---
# resilience-test-planner

## Purpose
Plan resilience testing around dependency failures, retries, timeouts, degraded modes, and recovery behavior.

## Trigger this skill when
- You need this specific non-functional planning or review task rather than a broad testing request.
- You want explicit artifacts, thresholds, and evidence expectations.
- You need an output another agent or developer can execute or extend safely.

## Expected inputs
- system architecture
- external dependencies
- failure assumptions
- recovery expectations

## Deliverables
- resilience test plan
- failure injection matrix
- expected degraded modes
- recovery criteria

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
- stress-test-scenario-writer
- observability-driven-test-planner
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
