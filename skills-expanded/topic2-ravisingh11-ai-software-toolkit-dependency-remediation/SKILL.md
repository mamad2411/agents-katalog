---
name: dependency-remediation
description: "Resolve dependency vulnerabilities, package drift, audit alerts, and lockfile inconsistency while preserving package metadata. Use for Dependabot, Snyk, npm audit, package upgrade, and package manager maintenance work."
---

# Dependency Remediation

Use this skill for Dependabot, Snyk, npm audit, package upgrade, and lockfile
maintenance work.

## Inspect

- Identify alert severity, package path, and whether the dependency is direct or
  transitive.
- Check package manager, lockfile, runtime version, and workspace layout.
- Review CI and test commands before changing packages.

## Fix

- Prefer direct parent upgrades over broad overrides.
- Use overrides only when the vulnerable package is transitive and no safe
  parent upgrade is available.
- Keep first-party package metadata consistent with repository visibility,
  publishability, and the selected license.
- Treat vendored third-party package metadata separately from first-party package metadata.
- Avoid unrelated dependency churn unless the task is explicitly a broad
  upgrade.

## Safety

- Do not remove lockfiles unless the package manager migration is explicit.
- Do not change package license metadata for vendored third-party code unless the task is specifically license normalization.
- Preserve workspace-specific package manager choices instead of forcing a new tool.

## Verify

- Install with lockfile consistency.
- Run focused tests for affected paths.
- Run build/typecheck where practical.
- Re-run the audit or alert check.
- Document residual alerts and why they remain.
