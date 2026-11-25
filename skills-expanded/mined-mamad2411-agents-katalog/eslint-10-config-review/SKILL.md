---
name: eslint-10-config-review
description: Reviews, creates, and migrates ESLint 10 flat config files. Use when working with eslint.config files, rule configuration, legacy eslintrc migration, parser/plugin boundaries, or lint setup quality.
---

# ESLint 10 Config Review

Use this skill for ESLint 10 configuration work.

## Process

1. Identify the package manager, module system, workspace layout, and existing lint scripts.
2. Locate `eslint.config.*`, legacy `.eslintrc*`, `package.json`, and CI lint jobs.
3. Run helper scripts with `--help` before using them.
4. Prefer read-only inspection before making config changes.
5. Keep ESLint scope separate from framework-specific plugins unless the project already uses them.
6. Explain any new parser, plugin, or shareable config dependency before adding it.

## Helper Script

```powershell
node .\.agents\plugins\eslint-10\skills\eslint-10-config-review\scripts\eslint-config-scan.mjs --help
```

## Workflows

- `workflows/flat-config-review-workflow.md`
- `workflows/migrate-to-eslint-10-workflow.md`

## Resource

- `resources/flat-config-review-checklist.md`

## Example

- `examples/eslint-config-example.mjs`
