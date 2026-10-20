---
name: owasp-mastg-hacking-playground
description: Welcome to the MASTG Hacking Playground which is part of the [OWASP Mobile Application Security (MAS) project](https://mas.owasp.org/). The MASTG Hacking Playground is a collection of educational iOS and Android mobile apps, that are intent
category: training-and-labs
repo: repos/MASTG-Hacking-Playground
stack: github-actions
triggers:
  - "MASTG-Hacking-Playground"
  - "mobile security"
  - "masvs"
  - "training lab"
  - "vulnerable app"
---

# Skill: MASTG-Hacking-Playground

## Purpose
Welcome to the MASTG Hacking Playground which is part of the [OWASP Mobile Application Security (MAS) project](https://mas.owasp.org/). The MASTG Hacking Playground is a collection of educational iOS and Android mobile apps, that are intent

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
