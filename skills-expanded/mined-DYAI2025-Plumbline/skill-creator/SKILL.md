---
name: skill-creator
description: Use when creating or updating a Claude Code skill directory with a focused SKILL.md, safe trigger conditions, workflow, guardrails, and validation notes.
---

# Skill Creator

Use this local fallback together with `writing-skills` when the Agent Learning Loop has
explicit user approval to persist a new or improved reusable capability.

## Workflow
1. Confirm the approved change and target skill name.
2. Check existing skills for overlap before creating a new one.
3. Create or edit exactly one skill directory with `SKILL.md` unless the user approved more.
4. Write frontmatter with `name` and an action-oriented `description`.
5. Include trigger conditions, steps, guardrails, expected output, and validation.
6. Show the diff and run repository setup tests before committing.

## Guardrails
- Never create or modify skills without explicit per-item user approval.
- Prefer updating an existing skill over adding a near-duplicate.
- Keep skills small enough that agents can apply them reliably.
