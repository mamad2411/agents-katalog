---
name: dependency-health
description: "Assesses dependency health, update risk, licensing signals, maintenance, known vulnerabilities, and lockfile reproducibility. Use when updating packages, investigating supply-chain risk, preparing a release, or reviewing dependency changes."
license: MIT
metadata:
  author: OpenSelfHosting
  version: "1.0.0"
---

# Dependency Health

## Goal
Evaluate dependency changes and propose safe, reproducible maintenance. Do not equate the newest version with the best choice or a reported advisory with confirmed exploitability in this application.

## Workflow
1. Detect the package ecosystem and its authoritative manifest and lockfile. Read repository guidance for package manager and supported runtime versions.
2. Inspect the dependency diff, direct versus transitive status, version range, release notes/changelog, compatibility requirements, and project usage where available.
3. Assess relevant signals: known security advisories, active maintenance, release cadence, issue/patch activity, compatibility, transitive dependency growth, installation scripts/native code, package provenance, and license obligations. Use current authoritative sources when external research is available; record lookup dates for time-sensitive claims.
4. Determine exposure and reachability. A vulnerable package matters differently depending on whether affected code is reachable, which feature is enabled, and how input reaches it. Do not dismiss a vulnerability solely because reachability is unclear.
5. Recommend one of: keep, patch, upgrade minor/major, replace, pin, constrain, remove, or investigate. Explain benefits, breaking-change risk, and migration work.
6. Preserve reproducibility. Update the manifest and lockfile using the project's package manager; do not hand-edit lockfile internals. Avoid unrelated bulk upgrades.
7. Run package-manager validation, targeted tests, audit/scanner commands when available, and build/type checks relevant to the change.
8. Review the final diff for unexpected package sources, post-install scripts, repository changes, and accidental secret files.

## Report
Include ecosystem, dependencies examined, evidence/source date, risk and confidence, compatibility impacts, recommended version/action, commands actually run, and unresolved licensing/security questions.

## Guardrails
- Do not invent a CVE, severity, license, maintainer status, or version availability.
- Do not upgrade to an unverified package name or typosquatted alternative.
- Do not delete lockfiles or suppress audit findings merely to clear a check.
- Do not install untrusted packages or execute package lifecycle scripts without assessing source and environment risk.
- A clean automated audit is not proof that the application is secure.
