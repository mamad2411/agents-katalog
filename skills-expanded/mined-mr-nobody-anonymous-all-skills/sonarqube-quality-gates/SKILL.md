---
name: sonarqube-quality-gates
description: "Operate SonarQube/SonarCloud quality gates: gate conditions, coverage import, new-code focus, issue triage and false-positive policy."
type: procedural
category: security
domain: security
version: 1.0.0
author: Mr-Nobody-Anonymous
license: MIT
risk: low
level: intermediate
triggers:
  - sonarqube quality gate failing
  - sonar coverage import
  - sonar new code period
  - sonar issue triage
  - sonar scanner ci
keywords:
  - sonarqube
  - quality-gate
  - coverage
  - static-analysis
  - new-code
source: custom
enabled: true
---

# SonarQube Quality Gates

## Purpose

Operate SonarQube/SonarCloud quality gates: gate conditions, coverage import, new-code focus, issue triage and false-positive policy.

## When to Use

- A quality gate blocks merges and needs a real fix rather than a bypass.
- Coverage is not being imported from the test run.
- Technical debt must be paid down incrementally on new code.

## When NOT to Use

- The team has no Sonar instance and only needs local linting.
- The finding is a confirmed false positive that belongs in the exclusion list, not in code.
- You need runtime security testing rather than static analysis.

## Capabilities

- Configure gates around new-code metrics instead of absolute totals.
- Import coverage and test execution reports from CI correctly.
- Triage issues by severity, type and effort with documented decisions.
- Exclude generated and vendored code explicitly.

## Inputs

- Sonar project key, server URL and token (via CI secret store).
- The scanner version and the build tool in use.
- The coverage report path produced by the test runner.

## Workflow

1. Confirm the gate definition and which conditions fail the current run.
2. Verify the scanner sees the right sources, tests and exclusions.
3. Ensure coverage is imported (`sonar.coverageReportPaths` or the format-specific property).
4. Fix new-code issues first; record accepted false positives with a reason.
5. Re-run the scan and confirm the gate status before merging.

## Tools

- sonar-scanner / the Sonar plugin for your build tool
- CI coverage reports
- the Sonar API

## Examples

- `sonar-scanner -Dsonar.projectKey=app -Dsonar.sources=src -Dsonar.tests=tests`
- `sonar-scanner -Dsonar.coverage.lcov.reportPaths=coverage/lcov.info`
- `curl -su "$SONAR_TOKEN:" "$SONAR_HOST/api/qualitygates/project_status?projectKey=app"`

## Safety

- Never disable a gate to merge; fix the finding or record an explicit, reviewed exclusion.
- Excluding source directories can hide real issues; exclude only generated code.
- Sonar tokens are credentials: keep them in the CI secret store, never in the repo.

## Source

All-Skills canonical library (`skills/security/sonarqube-quality-gates`). First-party skill, maintained in this repository.

## Notes

- New-code focus keeps legacy debt from growing without a freeze.
- A gate that nobody can pass gets bypassed; calibrate thresholds to reality.
- Pairs with: `security/sast`, `development/code-review`.
