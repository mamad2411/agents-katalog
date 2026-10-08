---
name: write-a-skill
description: Create new agent skills with proper structure, progressive disclosure, and bundled resources. Use when the user wants to create, write, build, or improve a skill or workflow command.
---

# Write A Skill

Create or improve a skill as its own task, not as part of the orchestrate workflow.

## Process

1. Gather requirements:
   - what task or domain the skill covers
   - what use cases it must handle
   - whether it needs scripts or only instructions
   - what references should shape it
2. Draft the skill with:
   - `SKILL.md`
   - `references/` when richer guidance is needed
   - `examples/` when examples are useful
   - `scripts/` for deterministic helpers
3. Review the draft against the skill checklist before finishing.

## Rules

1. Keep `SKILL.md` concise and easy for Codex to select.
2. Put richer guidance in `references/` instead of bloating `SKILL.md`.
3. Make the description specific enough that Codex can distinguish the skill from others.
4. Include escape hatches for ambiguous input.

## Resources

- Skill authoring guide: `references/skill-authoring.md`
