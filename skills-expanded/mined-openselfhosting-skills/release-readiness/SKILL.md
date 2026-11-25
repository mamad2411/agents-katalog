---
name: release-readiness
description: "Assesses whether a software release is ready by checking versioning, tests, artifacts, migration and rollback plans, security, documentation, and operational observability. Use before publishing a package, mobile/desktop app, service, or tagged release."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Release Readiness

## Goal
Produce a risk-based go/no-go assessment. Do not equate a successful build with a safe release.

## Workflow
1. Establish the intended release version, platforms, environments, release scope, audience, date constraints, and project-specific release policy.
2. Inspect the changes since the previous release/tag and compare them with release notes and issue/PR context. Identify changes that affect public APIs, persisted data, permissions, configuration, dependencies, or user workflows.
3. Verify version identifiers, package metadata, changelog, tags, signing/notarization requirements, artifact names, checksums, and supported platform/runtime matrix as applicable.
4. Review test/build evidence: unit and integration checks, supported platform builds, smoke tests, upgrade/rollback tests, and reproducible build steps where required. Record exact evidence and gaps.
5. Check security and supply-chain status: dependency review, secrets, signing credentials, CI permissions, provenance, and release artifact contents. Do not expose credentials.
6. Check data and deployment readiness: migration order, backward compatibility, backup/restore confidence, feature flags, health checks, monitoring/alerting, rate limits, and capacity assumptions as relevant.
7. Review user communication: release notes, known issues, upgrade instructions, deprecations, support guidance, and documentation links.
8. Define a staged rollout and rollback or forward-fix path proportionate to impact. State any irreversible changes and how to detect failure early.
9. Classify each item as Pass, Fail, Not run, or Not applicable with evidence. Missing information is not a pass.
10. Give a recommendation: **Go**, **Conditional go** (with explicit blockers/owners), or **No-go**. Do not publish, tag, deploy, or submit a release unless explicitly asked and authorized.

## Report template
- Release/version and target.
- Decision and rationale.
- Critical blockers.
- Validation evidence and checks not run.
- Migration/deployment steps.
- Monitoring and rollback/forward-fix plan.
- Known issues and customer-facing notes.

## Guardrails
Do not invent test results, approvals, signing status, marketplace acceptance, or monitoring coverage. Treat a missing rollback path for irreversible data changes as a meaningful risk, not a paperwork omission.
