---
name: asset-generation-templates
description: Generate SKILL.md, agent.yaml, and hook YAML with structured content and conventions.
---

# Asset Generation Templates

Generate SKILL.md, agent.yaml, and hook YAML with structured content and conventions.

## When to Use

Use this skill when:

- Working with code in `src/generator/index.ts/`
- User mentions "generate"
- User mentions "SKILL.md"
- User mentions "agent.yaml"
- User mentions "hooks"
- User mentions "yaml"

## Patterns

- directory scaffolding under .github/
- markdown frontmatter for skills
- YAML agent config with skills/tools/triggers/hierarchy
- hook YAML with event, commands, optional condition
- dry-run support without writing files

## Examples

```
const files = await generator.generate(analysis); // writes .github/skills/* and .github/agents/*
```

## Category

**patterns** - Common code patterns and conventions
