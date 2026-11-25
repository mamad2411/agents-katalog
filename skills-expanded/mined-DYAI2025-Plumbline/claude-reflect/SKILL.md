---
name: claude-reflect
description: Use during retrospectives to discover recurring process, prompt, skill, or workflow improvement candidates before authoring persistent changes.
---

# Claude Reflect

A local fallback for `/reflect` and `/reflect-skills` when an external reflect plugin is unavailable.

## Reflection workflow
1. Review the completed plan, diffs, tests, reviewer findings, and user corrections.
2. Cluster recurring friction into process, prompt, test, and skill categories.
3. For each candidate, state evidence, expected benefit, risk, and rollback.
4. Send persistent changes through the human approval gate and `writing-skills` if a skill is involved.

Do not modify prompts or skills automatically.

