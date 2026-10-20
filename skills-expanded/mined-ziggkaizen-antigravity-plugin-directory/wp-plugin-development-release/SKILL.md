---
name: wp-plugin-development-release
description: Prepares a reproducible WordPress plugin release by aligning versions, compatibility, readmes, licensing, dependencies, build artifacts, quality evidence, and WordPress.org review requirements. Use when packaging a release or preparing a submission.
---

# WordPress Plugin Release Preparation

Use this skill only after implementation and review findings are addressed.

## Inputs to collect

- Release version and change classification.
- Distribution channel and release destination.
- Supported WordPress/PHP/dependency matrix and executed evidence.
- Plugin headers, readme, changelog, upgrade notices, schema/data version, and public deprecations.
- Build/package command, runtime dependencies, licensing inventory, artifact exclusions, signing/checksum policy, and rollback plan.
- WordPress.org account/repository state when applicable.

## Method

1. Apply the [version compatibility matrix](resources/version-compatibility-matrix.md) and reconcile claims with executed tests.
2. Apply the [release readiness checklist](resources/release-readiness-checklist.md).
3. Align plugin header `Version`, package metadata, readme stable tag, changelog, upgrade notices, schema version, and built asset versions.
4. Re-run syntax, tests, PHPCS/WPCS, static analysis, dependency audits, Plugin Check, and artifact install/runtime checks according to project policy.
5. Build from a clean checkout with the documented release command.
6. Inspect the archive contents, dependency licenses, generated assets, file permissions, secrets, development debris, and top-level folder name.
7. Install and exercise the artifact in clean lowest/current supported environments, including upgrade and uninstall paths affected by the release.
8. Use the optional WordPress.org MCP server only for current guidelines, readme validation, status, or review assistance.
9. Require explicit user approval immediately before submission, resubmission, release publication, or another external state-changing action.
10. Run the [prepare plugin release workflow](workflows/prepare-plugin-release-workflow.md).

## Release rules

- Do not publish from an uncommitted or dirty source tree.
- Do not claim a tested version that lacks evidence.
- Do not ship secrets, local environment files, caches, test output, or unnecessary development dependencies.
- Do not change data-deletion policy silently.
- Do not submit automatically merely because validation passed.
- Do not assume WordPress.org acceptance from Plugin Check or MCP validation.
- For WordPress.org distribution, verify GPL-compatible licensing for the plugin and all distributed dependencies/assets.

## Required output

Return a release-readiness report containing:

- intended version and distribution channel
- source commit and clean-build command
- compatibility evidence and gaps
- version/header/readme/schema alignment
- artifact name, file inventory summary, size, and checksum
- test/tool results
- licensing and privacy status
- migration, rollback, and uninstall notes
- WordPress.org status/reviewer feedback when applicable
- explicit blockers and the approval required for the next external action
