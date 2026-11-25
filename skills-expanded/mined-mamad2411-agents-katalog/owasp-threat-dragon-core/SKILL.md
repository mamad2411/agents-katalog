---
name: owasp-threat-dragon-core
description: A historical version is kept here on the [1.4.0 branch](https://github.com/OWASP/threat-dragon-core/tree/1.4.0). All new development, bugfixes, etc will take place in the [threat-dragon](https://github.com/OWASP/threat-dragon), and all issu
category: projects-and-frameworks
subcategory: other
repo: repos/threat-dragon-core
stack: documentation
triggers:
  - "threat-dragon-core"
---

# Skill: threat-dragon-core

## Purpose
A historical version is kept here on the [1.4.0 branch](https://github.com/OWASP/threat-dragon-core/tree/1.4.0). All new development, bugfixes, etc will take place in the [threat-dragon](https://github.com/OWASP/threat-dragon), and all issu

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
