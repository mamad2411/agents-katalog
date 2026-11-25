---
name: les-knowledge-promotion
description: Promote durable verified task findings into the correct project-owned knowledge location.
invocation: model
maturity: stable
route: knowledge
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/knowledge-promotion.md","../../policies/memory-model.md","../../policies/rules/documentation.md","../../policies/rules/technical-decisions.md"]
---

# Knowledge Promotion

## Invoke

Inherit `../les-bootstrap/SKILL.md` and knowledge-promotion workflow.

## Inputs

Verified finding, durable scope, and project-owned destination.

## Procedure

1. Check repetition, ownership, and evidence. Done when: promotion is justified.
2. Choose the smallest durable location. Done when: temporary state is excluded.
3. Record verification or expiry condition. Done when: future users can trust the note.

## Output

Project-owned knowledge record or explicit `SKIPPED` status.

## Guardrails

Never promote secrets, preferences, or unverified inference.

## Verification

Link the record to its originating evidence.

Bootstrap LES, then load `../../policies/workflows/knowledge-promotion.md`,
`../../policies/memory-model.md`, and the documentation and
technical-decisions rules. Output only durable, scoped, evidence-backed project
knowledge. Exclude temporary state, secrets, preferences, and inference.
