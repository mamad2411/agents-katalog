---
name: "rework-plan-writer"
pack: "code-review-inspection-pack"
purpose: "Turn review findings into a concrete rework plan with owners, sequence, validation steps, and closure criteria."
inputs: ["review findings or defect list", "severity or priority data", "delivery constraints", "available owners or teams"]
outputs: ["rework plan", "validation and closure steps", "dependencies and risks", "recommended next skill"]
handoffs: ["release-readiness-reviewer", "inspection-metrics-summarizer", "lightweight-review-facilitator"]
---
# rework-plan-writer

## Purpose
Turn review findings into a concrete rework plan with owners, sequence, validation steps, and closure criteria.

## Trigger this skill when
- You need a focused code-review or inspection analysis or artifact rather than generic commentary.
- Review discipline, issue handling, or closure quality matters to the outcome.
- You need a reusable output another reviewer, developer, or agent can extend safely.

## Expected inputs
- review findings or defect list
- severity or priority data
- delivery constraints
- available owners or teams

## Deliverables
- rework plan
- validation and closure steps
- dependencies and risks
- recommended next skill

## Operating procedure
1. Clarify the artifact, review objective, and what counts as a meaningful issue.
2. Separate explicit evidence from assumptions, missing context, or inference.
3. Apply the relevant review structure, checklist, or inspection framing consistently.
4. Produce compact findings that support triage, rework, and decision-making.
5. Recommend the next most useful review, remediation, readiness, or process step.

## Quality gates
- Do not treat preference as defect unless the criterion is explicit.
- Make severity, uncertainty, and evidence quality explicit.
- Prefer actionable findings tied to consequence over vague style commentary.
- Keep the artifact compact, structured, and reusable.

## Handoff targets
- release-readiness-reviewer
- inspection-metrics-summarizer
- lightweight-review-facilitator

## Output style
- Be explicit about evidence quality and uncertainty.
- Prefer structured findings over narrative filler.
- Tie recommendations to risk, delivery consequence, or rework cost.
- Use severity, priority, or confidence labels when useful.

## Failure modes to avoid
- Do not collapse all issues into one undifferentiated list.
- Do not hide missing evidence, unclear criteria, or reviewer uncertainty.
- Do not recommend vague actions with no owner or closure path.
- Do not ignore process defects when the artifact issues are symptoms of review failure.

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Evidence / confidence
## Assumptions
## Open questions
## Recommended next skill
```
