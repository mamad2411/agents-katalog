---
name: "lightweight-review-facilitator"
pack: "code-review-inspection-pack"
purpose: "Run a compact lightweight review for code, design, tests, or docs when full formal inspection overhead is not justified."
inputs: ["artifact under review", "review focus areas", "available reviewers or stakeholders", "time constraints"]
outputs: ["lightweight review summary", "issue list", "assumptions and follow-ups", "recommended next skill"]
handoffs: ["code-review-checklist-runner", "review-issue-categorizer", "rework-plan-writer"]
---
# lightweight-review-facilitator

## Purpose
Run a compact lightweight review for code, design, tests, or docs when full formal inspection overhead is not justified.

## Trigger this skill when
- You need a focused code-review or inspection analysis or artifact rather than generic commentary.
- Review discipline, issue handling, or closure quality matters to the outcome.
- You need a reusable output another reviewer, developer, or agent can extend safely.

## Expected inputs
- artifact under review
- review focus areas
- available reviewers or stakeholders
- time constraints

## Deliverables
- lightweight review summary
- issue list
- assumptions and follow-ups
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
- code-review-checklist-runner
- review-issue-categorizer
- rework-plan-writer

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
