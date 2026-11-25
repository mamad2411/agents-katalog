---
name: personal-camelcase-preference
description: Enforce camelCase naming preference for variables, settings keys, and identifiers in user-facing docs and project scripts.
---

# Personal CamelCase Preference

The user strongly prefers `camelCase` naming. Apply this preference everywhere possible across scripts and documentation.

- Use `camelCase` names for configuration keys and variables.
- Prefer `camelCase` in command examples and environment variables when technically supported.
- Keep naming consistent across bash, PowerShell, and docs unless a platform requires another format.

## Required exceptions by codebase

Use the naming style required by the target language, framework, or existing codebase conventions when needed. Common cases include:

- `snake_case`
- `PascalCase`
- `UPPER_CASE`
- `kebab-case`
- `Train-Case`
- `dot.case`
- `path/case`
- `camelCase`

Rule: default to `camelCase`, but do not fight established project conventions.

## Example preference

- Preferred: `learningReviewThrasholder`

## When updating existing files

1. Replace non-camelCase keys with camelCase alternatives.
2. Update all references in scripts and docs in the same change.
3. Keep behavior backward-compatible only if explicitly requested.
