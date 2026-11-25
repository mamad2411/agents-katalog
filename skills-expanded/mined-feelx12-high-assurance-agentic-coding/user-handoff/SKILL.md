---
name: user-handoff
description: Produce a user-actionable next-steps handoff at the end of any mode session.
---

# Skill: User Handoff

Use in **all modes** — always end with a handoff.

## Goal

Ensure every mode session ends with a structured, human-readable handoff that tells the user what was done, what remains, and what to do next.

## Steps

1. Identify the **current mode** from context (grounding, debugging, implementation, verification). **Important:** If the session changed modes (e.g., escalated from Debugging to Grounding), use the FINAL mode, not the starting mode.
2. Load the corresponding handoff template from `.kilo/templates/<mode>-next-steps-handoff.md`.
3. Read the `user-actionable-output.md` rule from `.kilo/rules/user-actionable-output.md` if you need the field descriptions.
4. Fill in each field based on what happened in the session.
5. If any **handoff escalation triggers** are present (auth, payments, permissions, PII, public API, safety-critical, scoring, scheduling, data integrity, low-confidence Alloy, architecture drift), set the gate status to "Requires Human Approval".
6. Output the completed handoff.

## Template Selection

| Mode | Template |
|---|---|
| Grounding | `.kilo/templates/grounding-next-steps-handoff.md` |
| Debugging | `.kilo/templates/debugging-next-steps-handoff.md` |
| Implementation | `.kilo/templates/implementation-next-steps-handoff.md` |
| Verification | `.kilo/templates/verification-next-steps-handoff.md` |

## Handoff Format

Every handoff must contain these fields (in this order):

```
## 1. What was completed
## 2. What was NOT completed
## 3. What needs user review
## 4. Assumptions needing sign-off
## 5. Current gate status
## 6. Next recommended mode
## 7. Copy/paste prompt for next agent
```
