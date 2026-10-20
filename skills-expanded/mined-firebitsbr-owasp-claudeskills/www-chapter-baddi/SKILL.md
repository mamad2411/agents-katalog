---
name: owasp-www-chapter-baddi
description: <h1 align="center">OWASP Baddi Chapter</h1> This is the source repository of OWASP Baddi. The Chapter wiki is located at https://owasp.org/www-chapter-baddi **Contributions**
category: community-and-events
repo: repos/www-chapter-baddi
stack: ruby,documentation
triggers:
  - "www-chapter-baddi"
---

# Skill: www-chapter-baddi

## Purpose
<h1 align="center">OWASP Baddi Chapter</h1> This is the source repository of OWASP Baddi. The Chapter wiki is located at https://owasp.org/www-chapter-baddi **Contributions**

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
