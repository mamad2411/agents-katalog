---
name: "patch-management-checker"
pack: "cloud-platform-operations-pack"
purpose: "Check whether platform and cloud-hosted components can be patched safely with clear ownership, cadence, testing, and rollback coverage."
inputs: ["asset list", "patch cadence", "maintenance policy", "testing evidence", "rollback approach"]
outputs: ["patch readiness review", "ownership gaps", "cadence risks", "test and rollback concerns", "recommended fixes"]
handoffs: ["maintenance-window-planner", "update-rollback-planner", "blue-green-readiness-reviewer"]
---
# patch-management-checker

## Purpose
Check whether platform and cloud-hosted components can be patched safely with clear ownership, cadence, testing, and rollback coverage.

## Trigger this skill when
- A cloud or platform decision needs operationally realistic review rather than generic best-practice talk.
- You need outputs that can feed architecture, operations, release, migration, or governance work.
- The team risks hand-waving ownership, drift, rollback, timing, or lifecycle constraints.

## Expected inputs
- asset list
- patch cadence
- maintenance policy
- testing evidence
- rollback approach

## Deliverables
- patch readiness review
- ownership gaps
- cadence risks
- test and rollback concerns
- recommended fixes

## Operating procedure
1. Clarify the actual workload, platform boundary, environment scope, and operational ownership.
2. Separate what is observed, measured, or approved from what is merely assumed.
3. Produce the skill-specific artifact or review output.
4. Surface lifecycle risks, drift, dependency timing, rollback gaps, and hidden ops burden explicitly.
5. Recommend the next best handoff instead of trying to solve the whole platform strategy at once.

## Quality gates
- The result is specific to the real workload and operating context.
- Ownership, timing, and rollback assumptions are visible.
- The output is usable by engineers, platform owners, ops staff, architects, or assessors.
- The recommendation reflects operational safety and maintainability, not only implementation speed.

## Handoff targets
- maintenance-window-planner
- update-rollback-planner
- blue-green-readiness-reviewer

## Output style
- Be explicit about control, ownership, reversibility, and operational cost.
- Prefer concrete decision artifacts over general cloud prose.
- Surface evidence gaps instead of inventing certainty.
- Keep outputs reusable inside runbooks, ADRs, tickets, migration plans, and platform docs.

## Failure modes to avoid
- Do not assume “cloud-native” means operationally simple.
- Do not ignore drift, tagging gaps, or unowned resources.
- Do not treat rollback as optional for risky updates or migrations.
- Do not bury customer impact or support timing behind architecture language.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks / blockers
## Open questions
## Recommended next skill
```
