---
name: owasp-mas-gh-action-corellium
description: 1. Set the `CORELLIUM_API_TOKEN` secret (see [Corellium documentation](https://support.corellium.com/administration/api-token) and [GitHub documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/us
category: projects-and-frameworks
subcategory: mobile
repo: repos/mas-gh-action-corellium
stack: github-actions
triggers:
  - "mas-gh-action-corellium"
  - "mobile security"
  - "masvs"
---

# Skill: mas-gh-action-corellium

## Purpose
1. Set the `CORELLIUM_API_TOKEN` secret (see [Corellium documentation](https://support.corellium.com/administration/api-token) and [GitHub documentation](https://docs.github.com/en/actions/how-tos/write-workflows/choose-what-workflows-do/us

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
