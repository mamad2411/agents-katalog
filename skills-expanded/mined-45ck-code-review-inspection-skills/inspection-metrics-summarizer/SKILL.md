---
name: "inspection-metrics-summarizer"
pack: "code-review-inspection-pack"
purpose: "Summarize inspection and review metrics so teams can see defect density, issue mix, effort, outcomes, and improvement opportunities."
inputs: ["review logs or issue data", "artifact size or scope data", "timing or effort data if available", "desired reporting audience"]
outputs: ["inspection metrics summary", "patterns and insights", "data quality caveats", "recommended next skill"]
handoffs: ["defect-leakage-predictor", "process-review-gap-detector", "release-readiness-reviewer"]
---
# inspection-metrics-summarizer

## Purpose
Summarize inspection and review metrics so teams can see defect density, issue mix, effort, outcomes, and improvement opportunities.

## Trigger this skill when
- You need a focused code-review or inspection analysis or artifact rather than generic commentary.
- Review discipline, issue handling, or closure quality matters to the outcome.
- You need a reusable output another reviewer, developer, or agent can extend safely.

## Expected inputs
- review logs or issue data
- artifact size or scope data
- timing or effort data if available
- desired reporting audience

## Deliverables
- inspection metrics summary
- patterns and insights
- data quality caveats
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
- defect-leakage-predictor
- process-review-gap-detector
- release-readiness-reviewer

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
