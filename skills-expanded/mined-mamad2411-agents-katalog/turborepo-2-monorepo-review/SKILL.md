---
name: turborepo-2-monorepo-review
description: Reviews Turborepo 2 monorepo package boundaries, task graph health, dependency ownership, workspace layout, and hidden cross-domain coupling. Use when auditing apps, services, packages, or shared libraries.
license: MIT
compatibility: Requires Python 3 for the optional package-boundary report script.
---

# Turborepo 2 Monorepo Review

Use this skill to review the health of a Turborepo 2 monorepo beyond a single `turbo.json` file.

## When to Use

Use this skill when the user asks to:

- Review package boundaries.
- Review app/service/package organization.
- Find hidden cross-package or cross-domain builds.
- Identify over-coupled shared packages.
- Check workspace package ownership.
- Prepare a monorepo architecture review.
- Review whether task graph and package graph tell the same story.

## Workflow Reference

Use the workflow for a structured review:

```text
workflows/turborepo-2-monorepo-review-workflow.md
```

## Resource Reference

Use the checklist:

```text
resources/turborepo-2-monorepo-review-checklist.md
```

## Example Reference

Use the findings template:

```text
examples/turborepo-2-package-boundary-findings-template.md
```

## Script Reference

Before using the package-boundary script:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-monorepo-review/scripts/turborepo-2-package-boundary-report.py --help
```

Run from the repository root:

```bash
python3 .agents/plugins/turborepo-2/skills/turborepo-2-monorepo-review/scripts/turborepo-2-package-boundary-report.py --root .
```

## Review Strategy

1. Identify workspace globs and package locations.
2. Classify packages as app, service, package/library, tooling, config, or unknown.
3. Compare package dependencies with Turborepo task dependencies.
4. Find tasks that reach across package boundaries without package dependencies.
5. Find broad shared packages that may hide domain coupling.
6. Find package scripts that run commands in unrelated packages.
7. Check local/CI command parity.
8. Report findings as risks and recommendations, not automatic rewrites.
