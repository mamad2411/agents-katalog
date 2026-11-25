---
name: owasp-cheatsheetseries
description: Welcome to the official repository for the Open Worldwide Application Security Project® (OWASP) Cheat Sheet Series project. The project focuses on providing good security practices for builders in order to secure their applications. In ord
category: documentation-and-guides
repo: repos/CheatSheetSeries
stack: nodejs,python,docker,github-actions,documentation
triggers:
  - "CheatSheetSeries"
  - "write docs"
  - "update guide"
  - "python script"
  - "node project"
  - "js tooling"
---

# Skill: CheatSheetSeries

## Purpose
Welcome to the official repository for the Open Worldwide Application Security Project® (OWASP) Cheat Sheet Series project. The project focuses on providing good security practices for builders in order to secure their applications. In ord

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
