---
name: "deployment-risk-checker"
pack: "deployment-release-pack"
purpose: "Identify and rank the key risks attached to a proposed deployment, cutover, migration, or release approach."
inputs: ["deployment plan", "system dependencies", "migration steps", "business criticality", "operational constraints"]
outputs: ["deployment risk register", "high-risk steps", "mitigations", "contingency needs", "risk-based recommendation"]
handoffs: ["rollback-readiness-checker", "go-live-readiness-reviewer", "post-release-monitoring-plan"]
---
# deployment-risk-checker

## Purpose
Identify and rank the key risks attached to a proposed deployment, cutover, migration, or release approach.

## Trigger this skill when
- A release, deployment, rollout, cutover, or environment promotion needs explicit operational review.
- You need deployment outputs that can feed engineering, operations, governance, or assessment work.
- The delivery plan risks confusion between readiness signals and actual release safety.

## Expected inputs
- deployment plan
- system dependencies
- migration steps
- business criticality
- operational constraints

## Deliverables
- deployment risk register
- high-risk steps
- mitigations
- contingency needs
- risk-based recommendation

## Operating procedure
1. Clarify the release context, deployment path, change window, and operational constraints.
2. Separate what is proven, tested, approved, or rehearsed from what is merely assumed.
3. Produce the skill-specific artifact or review output.
4. Surface risks, dependencies, timing gaps, ownership gaps, and rollback concerns explicitly.
5. Recommend the next best handoff instead of trying to solve the entire release lifecycle at once.

## Quality gates
- The output is specific to the current release context.
- Uncertainty, dependencies, and decision blockers are visible.
- The result is usable by an engineering lead, release manager, SRE/ops owner, or assessment team.
- Operational safety, not only delivery speed, is reflected in the recommendation.

## Handoff targets
- rollback-readiness-checker
- go-live-readiness-reviewer
- post-release-monitoring-plan

## Output style
- Be explicit about operational risk, timing, ownership, and reversibility.
- Prefer executable artifacts over broad process prose.
- Surface evidence gaps instead of inventing readiness.
- Keep the result usable in real runbooks, tickets, release docs, and repo workflows.

## Failure modes to avoid
- Do not confuse “mostly tested” with release safety.
- Do not assume rollback works because it was written down once.
- Do not hide configuration drift or approval gaps.
- Do not optimize for release speed at the expense of operational recovery.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks / blockers
## Open questions
## Recommended next skill
```
