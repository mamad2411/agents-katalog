---
name: "risk-register-builder"
pack: "project-management-pack"
purpose: "Create a project risk register with causes, impacts, likelihood, responses, and owners."
inputs: ["project context", "constraints", "assumptions", "known concerns/incidents"]
outputs: ["risk register", "top risks", "response ideas", "ownership suggestions"]
handoffs: ["stakeholder-comms-planner", "cost-estimation-helper", "etc-reestimation-helper"]
---
# risk-register-builder

## Purpose
Create a project risk register with causes, impacts, likelihood, responses, and owners.

## Trigger this skill when
- A project, delivery effort, or formal planning activity needs clearer control artifacts.
- Scope, risk, cost, schedule, communication, or closure signals need structured review.
- You need planning outputs that can feed engineering, governance, or assessment work.

## Expected inputs
- project context
- constraints
- assumptions
- known concerns/incidents

## Deliverables
- risk register
- top risks
- response ideas
- ownership suggestions

## Operating procedure
1. Clarify the project context, objective, and control horizon.
2. Separate what is known from what is assumed, estimated, or missing.
3. Produce the skill-specific artifact or review output.
4. Surface risks, tradeoffs, ownership gaps, and ethics concerns explicitly.
5. Recommend the next best handoff instead of trying to solve the whole lifecycle at once.

## Quality gates
- The output is specific to the current project context.
- Uncertainty, assumptions, and decision dependencies are visible.
- The result is usable by a PM, engineering lead, or project team.
- Risks should be causal and actionable, not generic statements with no response path.

## Handoff targets
- stakeholder-comms-planner
- cost-estimation-helper
- etc-reestimation-helper

## Output style
- Be explicit about scope, timing, cost, risk, and governance tradeoffs.
- Prefer operational artifacts over broad managerial prose.
- Surface evidence gaps instead of inventing certainty.
- Keep the result usable in real project documents and repo workflows.

## Failure modes to avoid
- Do not confuse aspiration with approved commitment.
- Do not hide uncertainty inside a neat-looking plan.
- Do not treat every stakeholder or deliverable as equally critical.
- Do not sever planning artifacts from execution reality.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks / blockers
## Open questions
## Recommended next skill
```
