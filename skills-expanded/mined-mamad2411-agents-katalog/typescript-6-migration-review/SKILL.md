---
name: typescript-6-migration-review
description: Reviews and migrates TypeScript projects to TypeScript 6.x by auditing tsconfig options, dependencies, module resolution, stricter defaults, deprecated syntax, and TypeScript 7 readiness. Use when upgrading from TypeScript 5.x, fixing deprecation warnings, or preparing migration plans.
license: MIT
compatibility: Requires a TypeScript project and access to its tsconfig/package files.
---

# TypeScript 6 Migration Review

Use this skill when upgrading a project to TypeScript 6.x or reviewing TypeScript 6 compatibility.

## Migration Priorities

1. Confirm the current and target TypeScript versions.
2. Make compiler configuration explicit before changing source code.
3. Remove deprecated or removed TypeScript 6 options.
4. Fix missing global types by adding explicit `types` entries.
5. Fix `rootDir`, module resolution, declaration emit, and import syntax issues.
6. Keep `ignoreDeprecations: "6.0"` temporary and tracked.
7. Run typecheck after each logical batch of changes.

## What to Inspect

- `package.json`
- lockfiles
- `tsconfig.json` and extended configs
- project references
- package `exports` and `types`
- generated declaration output
- imports using JSON/module attributes
- namespace declarations
- scripts that call `tsc` with file names

## Migration Script

Run the audit script with `--help` before use:

```bash
node .agents/plugins/typescript-6/skills/typescript-6-migration-review/scripts/audit-tsconfig.mjs --help
```

The script reads config text and reports likely TypeScript 6 migration risks. It does not modify files.

## Workflows

Use `workflows/ts5-to-ts6-migration-workflow.md` for a repeatable TypeScript 5.x to 6.x migration review.

## Resources

Use `resources/typescript-6-migration-notes.md` for common TypeScript 6 default changes, removed options, and safe fixes.
