---
name: example-task
description: Baseline task skill example for .claude/skills/. Use as a reference template when authoring task skills. Do NOT use for builtin skills -- those go in src/skills/.
---

# Example Task Skill

A task skill is a session-scoped work instruction used by Claude Code.
Task skills differ from builtin skills: they require minimal frontmatter,
avoid scripts/ directories, and prefer inline examples.

## Key Differences from Builtin Skills

| Aspect | Builtin (src/skills/) | Task (.claude/skills/) |
|--------|----------------------|------------------------|
| Frontmatter | Full metadata block | Optional or minimal |
| scripts/ | Allowed | Not recommended |
| assets/ | Allowed | Not used |
| Body length | Up to 500 lines | Under 200 lines |
| Triggers | Required for routing | Not needed |

## Minimal Body-Only Template

When the skill is a simple protocol, omit frontmatter:

```
# My Task

## Rules

1. Always verify before writing
2. Never skip the lint step

## Steps

1. Read relevant files
2. Apply transformation
3. Verify result
```

## When to Add Frontmatter

Add name + description when:
- The skill should appear in skill listings
- You want the validator to check it by name
- The description serves as discovery hint

## Authoring Checklist

- [ ] Body under 200 lines
- [ ] No empty directories
- [ ] No "When to Use" section in body
- [ ] If frontmatter: name is kebab-case, description is one line
- [ ] run: node scripts/validate-skills.mjs .claude/skills/
