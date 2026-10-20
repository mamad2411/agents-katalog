---
name: typescript-6-diagnostics
description: Diagnoses TypeScript 6 compiler errors, tsconfig problems, declaration emit changes, module-resolution failures, missing global types, and noisy migration failures. Use when tsc fails, editor types differ from CLI output, or TypeScript 6 upgrades produce confusing errors.
license: MIT
compatibility: Requires Node.js and a TypeScript project for the included helper scripts.
---

# TypeScript 6 Diagnostics

Use this skill when TypeScript 6 errors are confusing, noisy, or migration-related.

## Diagnostic Order

1. Confirm the compiler version used by the editor, CLI, package scripts, and CI.
2. Find the effective config with the repository's normal typecheck command or `tsc --showConfig`.
3. Reduce the failure to one project, config, or source file.
4. Separate config failures from source-level type errors.
5. Fix root causes before adding suppressions.
6. Verify with the same command that failed.

## Common TypeScript 6 Failure Areas

- Missing globals because `types` is now explicit.
- Emit path changes because `rootDir` is now config-directory based.
- Module resolution drift from old `baseUrl` or `classic` assumptions.
- Import assertions that need import attributes.
- CommonJS/ESM interop changes.
- Stricter default type checking.
- `tsc` command invocations that pass file names while a `tsconfig.json` exists.

## Scripts

Run with `--help` before use:

```bash
bash .agents/plugins/typescript-6/skills/typescript-6-diagnostics/scripts/verify-typescript-project.sh --help
node .agents/plugins/typescript-6/skills/typescript-6-diagnostics/scripts/guard-run-command.mjs --help
```

## Workflows

Use `workflows/typecheck-debug-workflow.md` when debugging TypeScript 6 compiler output.
