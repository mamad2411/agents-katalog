---
name: owasp-samm
description: OWASP SAMM has moved to a new organization: https://github.com/owaspsamm. There you will now find both the [core model](https://github.com/owaspsamm/core) as well as all derived projects. If you're looking for documents related to OWASP SAM
category: general-owasp
repo: repos/samm
stack: javascript,documentation
triggers:
  - "samm"
  - "node project"
  - "js tooling"
---

# Skill: samm

## Purpose
OWASP SAMM has moved to a new organization: https://github.com/owaspsamm. There you will now find both the [core model](https://github.com/owaspsamm/core) as well as all derived projects. If you're looking for documents related to OWASP SAM

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
