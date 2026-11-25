---
name: teacher-adoption-modeling
description: Build and audit a teacher adoption conditions model for an AI agent supporting active learning, distinguishing perceptions, concerns, barriers, enablers, institutional conditions, and design implications.
---

# Teacher Adoption Modeling

Use when the user asks to analyze teacher perceptions, concerns, adoption conditions, barriers, enablers, readiness, or implementation conditions.

## Core Distinctions

Keep these categories separate:

- perceptions: how teachers understand or value the AI agent
- concerns: worries, risks, doubts, or objections
- barriers: practical or structural obstacles
- enablers: factors that make adoption easier
- conditions for adoption: requirements that must be met for acceptable use
- design implications: how the agent should change in response
- institutional implications: policy, training, workload, support, governance

## Workflow

1. Read relevant findings, codebooks, or theme tables.
2. Extract adoption-related evidence.
3. Group evidence by category.
4. Identify relationships:
   - concern -> condition
   - barrier -> support mechanism
   - perceived benefit -> design priority
   - institutional constraint -> governance implication
5. Draft a model that can be represented as:
   - table
   - matrix
   - conceptual diagram
   - chapter subsection
6. Flag unsupported or overgeneralized adoption claims.

## Output

Create or update:

- `models/TEACHER_ADOPTION_MODEL.md`
- `models/ADOPTION_CONDITIONS_MATRIX.md`
- `figures/adoption-conditions-model.mmd`

## Guardrails

Do not flatten teacher concerns into generic "resistance".
Do not imply causal relationships unless the study design supports them.
