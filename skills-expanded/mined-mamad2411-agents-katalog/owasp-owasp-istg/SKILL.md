---
name: owasp-owasp-istg
description: <a href="https://owasp.org/owasp-istg/"><img width="180px" align="right" style="float: right;" src="src/img/istg_cover.png"></a> The OWASP IoT Security Testing Guide provides a comprehensive methodology for penetration tests in the IoT fiel
category: general-owasp
repo: repos/owasp-istg
stack: github-actions
triggers:
  - "owasp-istg"
---

# Skill: owasp-istg

## Purpose
<a href="https://owasp.org/owasp-istg/"><img width="180px" align="right" style="float: right;" src="src/img/istg_cover.png"></a> The OWASP IoT Security Testing Guide provides a comprehensive methodology for penetration tests in the IoT fiel

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
