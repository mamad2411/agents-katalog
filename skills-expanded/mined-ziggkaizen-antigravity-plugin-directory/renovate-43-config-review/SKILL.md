---
name: renovate-43-config-review
description: Reviews, creates, validates, and refactors Renovate 43 repository configuration. Use when working with renovate.json, renovate.jsonc, packageRules, dependencyDashboard, automerge, schedules, hostRules, config presets, Renovate config changes, or Renovate reconfiguration PRs.
license: MIT
compatibility: Requires Renovate 43 knowledge. Optional validation requires Node.js with npx or a cached Renovate 43 package.
---

# Renovate 43 Config Review

Use this skill for repository-level Renovate 43 config creation, review, refactoring, and validation.

## Workflows

- `workflows/renovate-43-config-review-workflow.md`: structured repository config review.
- `workflows/renovate-43-reconfigure-workflow.md`: safe `renovate/reconfigure` branch workflow.

## Resources

- `resources/renovate-43-config-checklist.md`
- `resources/renovate-43-config-location-matrix.md`

## Examples

- `examples/renovate-43-conservative-jsonc.md`
- `examples/renovate-43-best-practices-jsonc.md`

## Scripts

Run scripts with `--help` before using them.

```bash
python3 scripts/detect-renovate-configs.py --help
python3 scripts/review-renovate-config-change.py --help
bash scripts/validate-renovate-config.sh --help
```

## Required Review Approach

1. Identify config file location and config type.
2. Keep repository config separate from self-hosted global config.
3. Review schema, presets, package rules, host rules, automerge, grouping, pinning, lockfile maintenance, and security update behavior.
4. Validate with `renovate-config-validator`.
5. Report blockers, security risks, behavior changes, and maintainability improvements.
