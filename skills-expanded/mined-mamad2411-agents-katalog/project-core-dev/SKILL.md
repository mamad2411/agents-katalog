---
name: project-core-dev
description: Overlay for day-to-day feature work and bug fixes in repo-owned code. Provides a validation checklist for build, test, format, and analysis. Use alongside the repo's principle skill.
---

# Project Core Dev

This is a composable overlay, not a standalone workflow.
Use alongside the repo's principle skill (e.g. **coding-guidance-cpp**) for
normal feature work and bug fixes in repo-owned code.

## When to use

The task is a feature, bug fix, or refactor in repo-owned code that needs a
standard build-test-format-analyze validation pass.

## Not for

Vendored dependency changes (use **project-vendor-boundary**), release/packaging
work (use **project-release-maintainer**), config/test-focused work (use
**project-config-and-tests**), or environment diagnosis (use
**project-platform-diagnose**).

## Validation Checklist

Run the repo's equivalents of these steps before committing:

- build with the development preset or debug configuration
- run the test suite with output on failure for covered changes
- run the formatter or format-check target
- run a lightweight smoke test (e.g. `--help` or `--version` on the main binary)
- add analyzer, sanitizer, or memory-checking validation when the change surface
  justifies it
- run static analysis targets when available
