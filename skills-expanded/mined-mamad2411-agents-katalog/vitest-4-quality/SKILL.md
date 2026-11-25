---
name: vitest-4-quality
description: Reviews Vitest 4 coverage, CI commands, migrations, dependency compatibility, critical-flow coverage, and final verification. Use when checking test quality, coverage behavior, package scripts, migration risk, or release-readiness.
license: MIT
compatibility: Vitest 4.x, Node.js 20+, and Vite 6+ when Vite integration is used.
---

# Vitest 4 Quality

Use this skill for coverage, migration, CI, dependency, and final verification work around Vitest 4.

## Version Boundary

- Target Vitest 4.x only.
- Keep dependencies on the Vitest 4 release line.
- Confirm Node.js 20+ and Vite 6+ where applicable.
- Do not mix Vitest 5 beta behavior into Vitest 4 guidance.

## Workflows

- `workflows/coverage-review-workflow.md`: Use when adding, changing, or reviewing coverage config, coverage commands, critical-flow coverage, or thresholds.
- `workflows/migration-review-workflow.md`: Use when migrating from Jest, Mocha, Chai, Sinon, Vitest 3, or older config patterns to Vitest 4.

## Resources

- `resources/ci-command-matrix.md`: Use when choosing or reviewing local and CI Vitest commands.

## Examples

- `examples/package-scripts-example.md`: Reference package scripts for Vitest 4 projects.

## Scripts

Run scripts with `--help` before using:

- `scripts/vitest-4-command-guard.mjs`: Hook script that prompts before risky Vitest or destructive shell commands.

## Quality Review Checklist

- Verify the installed `vitest` version and package manager.
- Verify Node.js and Vite compatibility.
- Check that package scripts use the intended mode: watch, one-shot, changed, coverage, shard, UI, or browser.
- Prefer targeted test commands before full-suite commands during agent work.
- Ensure CI uses `vitest run`, not watch mode.
- Ensure coverage config has deliberate `include` patterns.
- Ensure critical flows and security-sensitive changes have tests.
- Ensure integration tests do not depend on live external services by default.
- Ensure no `.only` remains in committed tests.
- Report commands actually run and commands intentionally not run.
