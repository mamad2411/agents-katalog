---
name: "product-vs-process-quality-splitter"
pack: "software-quality-pack"
purpose: "Separate product quality concerns from process quality concerns so remediation targets the right layer."
inputs: ["system or component context", "quality goals or stakeholder expectations", "available evidence", "constraints and known risks"]
outputs: ["structured findings", "quality-focused artifact", "assumptions and evidence gaps", "recommended next skill"]
handoffs: ["process-quality-checker", "quality-risk-register-builder", "quality-goal-scorer"]
---
# product-vs-process-quality-splitter

## Purpose
Separate product quality concerns from process quality concerns so remediation targets the right layer.

## Trigger this skill when
- You need a focused software-quality analysis or artifact rather than a broad generic review.
- Quality claims, tradeoffs, or risks are currently vague or implicit.
- You need a reusable output another reviewer, developer, or agent can extend safely.

## Expected inputs
- system or component context
- quality goals or stakeholder expectations
- available evidence
- constraints and known risks

## Deliverables
- structured findings
- quality-focused artifact
- assumptions and evidence gaps
- recommended next skill

## Operating procedure
1. Clarify which quality concern is in scope and why it matters to the system or stakeholder.
2. Separate explicit evidence from assumptions, missing data, or inference.
3. Convert vague quality language into concrete attributes, criteria, or review findings.
4. Produce a compact artifact that supports decision-making, follow-up analysis, or governance.
5. Recommend the next most useful quality, verification, or remediation step.

## Quality gates
- Do not make strong quality claims without evidence or confidence notes.
- Make tradeoffs, assumptions, and blind spots explicit.
- Prefer actionable findings tied to consequence over generic “improve quality” advice.
- Keep the artifact compact, structured, and reusable.

## Handoff targets
- process-quality-checker
- quality-risk-register-builder
- quality-goal-scorer

## Output style
- Be explicit about evidence quality and uncertainty.
- Prefer structured findings over narrative filler.
- Tie recommendations to quality impact, operational consequence, or change cost.
- Use severity, priority, or confidence labels when useful.

## Failure modes to avoid
- Do not confuse stakeholder optimism with evidence.
- Do not collapse all quality concerns into one generic score.
- Do not hide missing telemetry, weak tests, or process gaps.
- Do not recommend vague actions with no owner or consequence path.

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
