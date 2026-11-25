---
name: les-dependency-change
description: Evaluate and implement an explicit dependency addition, removal, or upgrade.
invocation: model
maturity: stable
route: dependency
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/task-lifecycle.md","../../policies/rules/dependencies.md","../../policies/rules/security.md","../../policies/verification.md"]
---

# Dependency Change

## Invoke

Inherit `../les-bootstrap/SKILL.md` and dependency policy.

## Inputs

Requested dependency change, consumers, compatibility, and risk.

## Procedure

1. Identify necessity and existing alternatives. Done when: the dependency decision is justified.
2. Inspect affected APIs and security boundary. Done when: compatibility is bounded.
3. Verify lockfile and consumers. Done when: change evidence passes.

## Output

Dependency decision, compatibility evidence, and terminal status.

## Guardrails

Do not add dependencies for convenience or perform external installation without authority.

## Verification

Record version, affected consumers, and focused checks.

Bootstrap LES. Prove the need, inspect existing alternatives, assess compatibility,
license, security, package size, and rollback, then use the project's native pinning
mechanism. Output the minimal manifest change and verification evidence. Stop
before installation or external fetch without authority.
