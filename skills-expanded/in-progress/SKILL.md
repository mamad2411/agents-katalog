---
name: in-progress
description: Manage draft skills that are not ready to ship yet. Use when the user asks to prototype, sketch, test, evaluate, or promote an experimental skill from in-progress into a stable skill bucket.
---

# In Progress Skill Incubator

Use this skill for draft skills that need iteration before becoming public or team-ready.

## Purpose

`skills/in-progress/` is a staging area. A draft belongs here when the idea is useful but the trigger, workflow, scope, or validation is still uncertain.

## Rules

- Draft skills should not be listed as stable skills in the root README.
- Keep experiments small enough to promote or retire quickly.
- Do not add large references until the core workflow works.
- Do not promote a skill without realistic trigger examples.

## Workflow

1. Define the experiment
   - State the repeated task the draft skill should improve.
   - Name the expected trigger phrases.
   - Identify what the agent should do differently after loading it.

2. Draft narrowly
   - Give the skill one main job.
   - Prefer workflow steps over broad advice.
   - Add stop conditions when misuse is likely.

3. Test with realistic prompts
   - Try at least three prompts that should trigger the skill.
   - Try one prompt that should not trigger it.
   - Note where the instructions are too vague or too broad.

4. Decide status
   - Promote to a domain bucket when the workflow is stable and useful.
   - Keep in progress when examples still fail or scope is unclear.
   - Move to `deprecated/` when the idea is no longer worth pursuing.

5. Promote cleanly
   - Move the skill folder into the right bucket.
   - Update README references if the skill is public.
   - Update workflows or registries only when the skill is part of a repeatable job.

## Promotion Checklist

- `name` is lowercase and hyphenated.
- `description` clearly says when to use the skill.
- The body has a workflow, rules, and verification or output guidance.
- The skill has one main job.
- It does not duplicate another stable skill.
- Any long examples or references are moved into `references/`.

## Output Format

End with:

- Draft status
- What changed
- What still needs testing
- Promote, keep, or retire recommendation
