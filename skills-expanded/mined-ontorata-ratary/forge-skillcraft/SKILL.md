---
name: forge-skillcraft
description: >-
  Author new Forge or project skills following Cursor SKILL.md conventions.
  Use when creating or updating .cursor/skills.
---
# Forge Skillcraft

**Activates:** adding or revising agent skills.

## Location

- Project skills: `.cursor/skills/{name}/SKILL.md`
- Register stage in `docs-ai/cross-cutting/agent-forge/manifest.json` if pipeline stage
- Never write to `~/.cursor/skills-cursor/` (Cursor internal)

## SKILL.md frontmatter

```yaml
---
name: forge-{verb}
description: >-
  One line: what + when to use (third person, trigger phrases).
---
```

## Quality bar

- Under 150 lines; link to docs-ai for depth
- Unique to Ratary â€” no copy-paste from external skill packs
- Reference existing prompts by path, don't duplicate
- Include verify/stop conditions

## Test a skill

1. Start fresh agent chat
2. Trigger phrase from description
3. Confirm agent reads skill before acting

Read Cursor guide: user skill `create-skill` if installed globally.
