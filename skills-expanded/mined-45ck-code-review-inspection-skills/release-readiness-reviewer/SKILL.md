---
name: "release-readiness-reviewer"
pack: "code-review-inspection-pack"
purpose: "Assess whether a change, feature, or release is ready to proceed based on review evidence, testing, risk, and unresolved defects."
inputs: ["release scope or candidate artifact", "review and test evidence", "known issues or risks", "operational constraints"]
outputs: ["release readiness assessment", "blocking vs non-blocking issues", "residual risk summary", "recommended next skill"]
handoffs: ["review-severity-scorer", "rework-plan-writer", "inspection-metrics-summarizer"]
---
# release-readiness-reviewer

## Purpose
Assess whether a change, feature, or release is ready to proceed based on review evidence, testing, risk, and unresolved defects.

## Trigger this skill when
- You need a focused code-review or inspection analysis or artifact rather than generic commentary.
- Review discipline, issue handling, or closure quality matters to the outcome.
- You need a reusable output another reviewer, developer, or agent can extend safely.

## Expected inputs
- release scope or candidate artifact
- review and test evidence
- known issues or risks
- operational constraints

## Deliverables
- release readiness assessment
- blocking vs non-blocking issues
- residual risk summary
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
- review-severity-scorer
- rework-plan-writer
- inspection-metrics-summarizer

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
