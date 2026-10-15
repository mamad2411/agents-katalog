---
name: jww-repository-validation
description: Select, run, and report proportionate validation for repository changes. Use after editing code, configuration, templates, documentation, or automation when the repository's relevant checks are not already explicit.
---

# Repository Validation

Use the narrowest check that exercises the changed behavior. Repository instructions and documented validation commands take precedence over these defaults.

## Discover the Checks

1. Read applicable `AGENTS.md`, `README`, contributor guidance, and nearby automation before choosing commands.
2. Inspect changed file types and available configuration such as `.editorconfig`, package manifests, CI workflows, task runners, and formatter or linter settings.
3. Prefer an existing documented check over inventing a new one.

## Choose Proportionate Validation

- Documentation: review readability and run `git diff --check`; run an available Markdown check when the repository uses one.
- Source code: format changed files and run focused tests, static analysis, or builds that exercise the change.
- Configuration, templates, and scripts: render, parse, or dry-run the affected artifact, and run a syntax check when applicable.
- Broad or risky changes: add the relevant integration or end-to-end check when available.

Start with read-only checks. Do not install dependencies, apply configuration, migrate data, publish artifacts, or otherwise change external state merely to validate unless the task authorizes those effects.

## Report Results

1. Review failures against the changed behavior before declaring them regressions.
2. State every relevant check run and its result.
3. State checks not run, why they were unavailable or disproportionate, and the remaining risk.
