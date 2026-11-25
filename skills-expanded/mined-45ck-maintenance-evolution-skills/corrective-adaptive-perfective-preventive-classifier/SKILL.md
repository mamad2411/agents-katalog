---
name: "corrective-adaptive-perfective-preventive-classifier"
pack: "maintenance-evolution-pack"
purpose: "Classify maintenance work as corrective, adaptive, perfective, or preventive so the team can choose the right response and priority."
inputs: ["issue report or change request", "system context", "known symptoms or requested change", "constraints / urgency", "available evidence if any"]
outputs: ["summary", "findings", "structured outputs", "risks / blockers", "open questions", "recommended next skill"]
handoffs: ["maintenance-triage-helper", "change-impact-mapper", "maintenance-knowledge-capture-writer"]
---
# corrective-adaptive-perfective-preventive-classifier

## Purpose
Classify maintenance work as corrective, adaptive, perfective, or preventive so the team can choose the right response and priority.

## Trigger this skill when
- A maintenance, support, defect, release, or evolution decision needs clearer structure.
- Symptoms, causes, impacts, and release choices are being conflated.
- You need artifacts that reduce operational surprise and rework.

## Expected inputs
- issue report or change request
- system context
- known symptoms or requested change
- constraints / urgency
- available evidence if any

## Deliverables
- summary
- findings
- structured outputs
- risks / blockers
- open questions
- recommended next skill

## Operating procedure
1. Clarify whether the work is driven by a defect, environmental change, requested improvement, or preventive maintenance need.
2. Separate observations, assumptions, hypotheses, and verified facts.
3. Produce the skill-specific artifact or decision aid.
4. Surface blast radius, rollback needs, regression exposure, and consumer impact explicitly.
5. Recommend the next best handoff instead of trying to solve the entire maintenance lifecycle at once.

## Quality gates
- The output is specific to the current maintenance context.
- Uncertainty, evidence gaps, and operational constraints are visible.
- The result is usable by an engineer, maintainer, on-call responder, or team lead.
- The output improves safety, speed, or clarity of the next maintenance decision.

## Handoff targets
- maintenance-triage-helper
- change-impact-mapper
- maintenance-knowledge-capture-writer

## Output style
- Prefer operationally useful artifacts over generic “maintenance best practices.”
- Be explicit about urgency, blast radius, rollback risk, and residual uncertainty.
- Surface what still needs verification instead of implying the cause is proven.
- Keep outputs concise enough to drop into tickets, incident notes, PRs, or runbooks.

## Failure modes to avoid
- Do not confuse a symptom with a verified root cause.
- Do not recommend shipping changes without considering rollback and regression exposure.
- Do not hide environment or data dependencies that could invalidate the result.
- Do not treat all maintenance work as “just bug fixing.”

## Minimum output skeleton
```md
## Summary
## Findings
## Structured outputs
## Risks / blockers
## Open questions
## Recommended next skill
```
