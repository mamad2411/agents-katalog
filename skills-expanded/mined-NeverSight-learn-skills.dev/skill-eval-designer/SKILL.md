---
name: skill-eval-designer
description: Design behavior evals, positive and negative prompts, expected behaviors, rubrics, fixtures, golden outputs, forward-tests, regression cases, and quality gates for AI agent skills and reusable agent workflows. Use when creating or improving SKILL.md packages, validating trigger descriptions, proving agent behavior changes, avoiding prompt dumps, or building eval-backed skill marketplaces.
---

# Skill Eval Designer

Use this skill to prove a skill changes agent behavior on realistic tasks.

## Workflow

1. Identify skill purpose, trigger boundary, expected artifact, failure modes, and target agent behavior.
2. Read `references/skill-eval-systems.md`.
3. Create positive prompts, negative prompts, expected behavior assertions, and artifact checks.
4. Add edge cases for over-triggering, under-triggering, unsafe advice, missing references, and generic output.
5. Produce eval fixture, behavior example, and forward-test plan.

## Guardrails

- Do not evaluate only whether the skill name appears.
- Do not leak the expected answer into the prompt.
- Include negative prompts so the skill does not trigger everywhere.

## Output format

```text
Skill under eval:
Behavior boundary:

Positive prompts:
- <prompt> -> expected behavior

Negative prompts:
- <prompt> -> why skill should not trigger

Assertions:
- <observable behavior>

Forward-test plan:
- task, artifact, pass/fail evidence
```
