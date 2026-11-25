---
name: "dependency-risk-review"
description: "Review dependencies for vulnerability exposure, abandonment risk, unsafe permissions, version pinning issues, and upgrade hazards. Use when a user asks for a dependency audit, package risk review, upgrade planning, or as part of $full-test-suite pre-release work."
---

# Dependency Risk Review

Inspect third-party dependencies for real operational, security, or maintenance risk.

## Focus Areas

- known vulnerable or stale packages
- abandoned or unmaintained dependencies
- unsafe transitive reach into sensitive surfaces
- overbroad SDK permissions or telemetry collection
- version drift between manifests and lockfiles

## Rules

- Promote only evidence-backed risk, not generic “keep dependencies updated” advice.

## References

- Finding format: `../_shared-project-ops/references/finding-format.md`
- Severity rubric: `../_shared-project-ops/references/severity-rubric.md`
