---
name: brainstorming
description: Use when a requirement, design gap, blocker, or open question must be closed with the user instead of being guessed by the agent.
---

# Brainstorming

Use this as a structured user-collaboration gate.

## Workflow
1. Name exactly one gap or decision.
2. Provide 2-4 concrete options with consequences and a recommended default if safe.
3. Ask for an explicit choice or missing fact.
4. Record the chosen answer as evidence in the spec/decision log.

## Guardrail
Do not turn an unconfirmed option into an assumption. If the user does not answer, keep the item `OPEN QUESTION` or `BLOCKER`.

