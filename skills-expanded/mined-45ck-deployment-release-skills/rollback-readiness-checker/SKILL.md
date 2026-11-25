---
name: "rollback-readiness-checker"
pack: "deployment-release-pack"
purpose: "Check whether rollback can actually be executed quickly and safely if the deployment causes unacceptable impact."
inputs: ["deployment method", "rollback procedure", "data migration characteristics", "recovery constraints", "owners/on-call info"]
outputs: ["rollback readiness assessment", "reversal steps", "irreversible change warnings", "timing/ownership gaps", "mitigations"]
handoffs: ["runbook-writer", "deployment-risk-checker", "go-live-readiness-reviewer"]
---
# rollback-readiness-checker

## Purpose
Check whether rollback can actually be executed quickly and safely if the deployment causes unacceptable impact.

## Trigger this skill when
- A release, deployment, rollout, cutover, or environment promotion needs explicit operational review.
- You need deployment outputs that can feed engineering, operations, governance, or assessment work.
- The delivery plan risks confusion between readiness signals and actual release safety.

## Expected inputs
- deployment method
- rollback procedure
- data migration characteristics
- recovery constraints
- owners/on-call info

## Deliverables
- rollback readiness assessment
- reversal steps
- irreversible change warnings
- timing/ownership gaps
- mitigations

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
- runbook-writer
- deployment-risk-checker
- go-live-readiness-reviewer

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
