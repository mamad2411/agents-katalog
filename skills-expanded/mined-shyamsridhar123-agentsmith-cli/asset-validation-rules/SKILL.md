---
name: asset-validation-rules
description: Validate generated skills, agents, hooks, and registry entries with actionable errors/warnings.
---

# Asset Validation Rules

Validate generated skills, agents, hooks, and registry entries with actionable errors/warnings.

## When to Use

Use this skill when:

- Working with code in `src/commands/validate.ts/`
- User mentions "validate"
- User mentions "frontmatter"
- User mentions "yaml"
- User mentions "hooks"
- User mentions "registry"

## Patterns

- SKILL.md frontmatter checks for name/description
- agent.yaml required fields and skill existence
- hook event validation against whitelist
- registry JSON line parsing with required fields
- summary with errors/warnings and exit code

## Examples

```
await validateCommand('.', { verbose: true });
```

## Category

**quality** - Testing, validation, and code quality
