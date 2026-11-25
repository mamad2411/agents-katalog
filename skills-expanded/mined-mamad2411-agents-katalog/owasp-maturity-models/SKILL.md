---
name: owasp-maturity-models
description: Node application to help managing Maturity Models like the ones created by BSIMM and OpenSAMM Build status: [![Build Status](https://travis-ci.org/OWASP/Maturity-Models.svg?branch=master)](https://travis-ci.org/OWASP/Maturity-Models) Curren
category: documentation-and-guides
repo: repos/Maturity-Models
stack: nodejs,docker
triggers:
  - "Maturity-Models"
  - "write docs"
  - "update guide"
  - "node project"
  - "js tooling"
---

# Skill: Maturity-Models

## Purpose
Node application to help managing Maturity Models like the ones created by BSIMM and OpenSAMM Build status: [![Build Status](https://travis-ci.org/OWASP/Maturity-Models.svg?branch=master)](https://travis-ci.org/OWASP/Maturity-Models) Curren

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
