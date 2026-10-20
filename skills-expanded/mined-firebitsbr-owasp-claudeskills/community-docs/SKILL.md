---
name: owasp-community-docs
description: This repo is composed of ready-for-print documents related to community outreach promoting OWASP content. Technical content in this repository is kind of meta, non-original, as we reference and use content from other sources within OWASP. I
category: documentation-and-guides
repo: repos/community-docs
stack: documentation
triggers:
  - "community-docs"
  - "write docs"
  - "update guide"
---

# Skill: community-docs

## Purpose
This repo is composed of ready-for-print documents related to community outreach promoting OWASP content. Technical content in this repository is kind of meta, non-original, as we reference and use content from other sources within OWASP. I

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
