---
name: owasp-vulnerable-container-hub
description: There are many repositories out there to provide vulnerable environments such as web applications, containers or virtual machines to those who want to learn security, since it helps not only students or someone who recently joined the field
category: training-and-labs
repo: repos/vulnerable-container-hub
stack: javascript,documentation
triggers:
  - "vulnerable-container-hub"
  - "cloud security"
  - "container security"
  - "training lab"
  - "vulnerable app"
  - "node project"
  - "js tooling"
---

# Skill: vulnerable-container-hub

## Purpose
There are many repositories out there to provide vulnerable environments such as web applications, containers or virtual machines to those who want to learn security, since it helps not only students or someone who recently joined the field

## Use When
- Task references this repository or close related OWASP content.
- You need secure-by-default changes aligned with existing project patterns.
- You need to update code, docs, tests, CI, or release artifacts in this repo.

## Input Checklist
- Confirm target files and expected behavior change.
- Confirm whether changes are code, docs, infra, or mixed.
- Confirm test/lint commands available in repo.

## Execution Playbook
1. Read README, CONTRIBUTING, SECURITY, and workflow files if present.
2. Inspect manifests and lock files to identify runtime/tooling.
3. Implement minimal changes preserving current architecture/style.
4. Run local validation (tests/lint/build) when available.
5. Update docs/changelog when behavior or usage changes.

## Guardrails
- Avoid broad refactors unless explicitly requested.
- Keep dependency changes minimal and justified.
- Preserve repository conventions and branch protections.

## Expected Outputs
- Focused patch with clear rationale.
- Validation notes with commands executed.
- Follow-up suggestions if gaps remain.
