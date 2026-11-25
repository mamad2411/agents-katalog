---
name: responsible-ai-agent-audit
description: Audit responsible AI risks for an educational AI agent, including teacher autonomy, student privacy, transparency, accountability, bias, overreliance, hallucinated advice, and governance conditions.
---

# Responsible AI Agent Audit

Use when assessing ethical, responsible AI, governance, or risk issues in the dissertation's AI agent design.

## Risk Areas

Check:

- teacher autonomy and professional judgment
- student data privacy and consent
- institutional policy and governance
- transparency of AI-generated advice
- accountability for wrong or harmful teaching suggestions
- hallucinated or weakly grounded pedagogy
- bias across disciplines, language, ability, and teaching contexts
- accessibility and inclusion
- overreliance and deskilling
- workload shifting
- data retention and third-party services

## Workflow

1. Identify the agent feature or scenario under review.
2. List stakeholders:
   - teachers
   - students
   - institution
   - learning designers
   - technical maintainers
3. For each risk, record:
   - risk description
   - affected stakeholder
   - likelihood
   - severity
   - evidence source
   - mitigation
   - residual concern
4. Translate risks into design requirements and adoption conditions.

## Output

Create or update:

- `audit-reports/RESPONSIBLE_AI_AUDIT.md`
- `design-specs/RESPONSIBLE_AI_REQUIREMENTS.md`
- `models/RISK_TO_ADOPTION_CONDITIONS.md`

## Guardrails

Read `../dissertation-shared/references/privacy-and-ethics.md`.
Do not treat ethics as a generic checklist; connect risks to this dissertation's teacher-facing active learning context.
