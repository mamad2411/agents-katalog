---
name: les-handoff
description: Create or recover a precise work handoff when ownership or execution continuity changes.
invocation: model
maturity: stable
route: handoff
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/handoff-recovery.md","../../policies/memory-model.md"]
---

# Handoff

## Invoke

Inherit `../les-bootstrap/SKILL.md` and handoff workflow.

## Inputs

Objective, current state, decisions, changes, checks, and blockers.

## Procedure

1. Record repository identity, branch/base, commit, dirty paths, and ownership. Done when: another owner can locate the exact state.
2. Record verified facts, evidence commands, exit status, decisions, inferences, and pending approvals. Done when: stale claims are visible.
3. Record rollback, blockers, unavailable checks, and evidence freshness. Done when: recovery risk is explicit.
4. Name the next safe action and its completion condition. Done when: recovery is reproducible without inferring authority.

## Output

Handoff record with repository identity, state, evidence, decisions, blockers,
rollback/recovery, next safe action, and terminal status.

## Guardrails

Do not put secrets, private state, or unverified conclusions in durable records.

## Verification

On recovery, revalidate state and the narrowest stale proof.

Bootstrap LES, then load `../../policies/workflows/handoff-recovery.md` and
`../../policies/memory-model.md`. Record objective, state, decisions, changed
paths, checks, blockers, and next action in the project-owned work area. Validate
the repository state before resuming from any handoff.
