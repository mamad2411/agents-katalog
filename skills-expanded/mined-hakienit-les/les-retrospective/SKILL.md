---
name: les-retrospective
description: Turn completed engineering work into a small evidence-backed improvement to process, architecture, tests, or project knowledge.
invocation: model
maturity: stable
route: retrospective
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/knowledge-promotion.md","../../policies/memory-model.md","../../policies/rules/documentation.md","../../policies/rules/technical-decisions.md"]
---

# Retrospective

## Invoke

Bootstrap LES after a meaningful delivery, incident, review, migration, or handoff
when repeated friction or a durable lesson may justify a change.

## Inputs

Objective, outcome, evidence, surprises, decisions, failures, recovery, and current
project knowledge ownership.

## Procedure

1. Separate observed events from interpretation. Done when: claims point to checks, traces, or user evidence.
2. Identify one or more leverage points. Done when: the lesson is framed as a behavior or decision change, not blame.
3. Choose promote, amend, defer, or discard. Done when: ownership, location, and expiry are explicit.
4. Record the smallest follow-up. Done when: the next action has acceptance and does not become automatic scope expansion.

## Output

Retrospective record with facts, lesson, affected owner, decision, follow-up,
verification, and terminal status.

## Guardrails

Do not promote anecdotes or private state into universal policy. Do not create
follow-up work without a named trigger and acceptance condition.

## Verification

Check evidence, duplication, ownership, and expiry. Mark a non-durable result
`SKIPPED` with the reason.
