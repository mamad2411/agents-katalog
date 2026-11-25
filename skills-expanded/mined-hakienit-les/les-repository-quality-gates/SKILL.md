---
name: les-repository-quality-gates
description: Audit repository structure, scripts, dependencies, documentation, and quality gates for maintainability without changing the repository.
invocation: model
maturity: stable
route: repository-quality
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/review.md","../../policies/verification.md","../../policies/rules/coding-quality.md","../../policies/rules/testing.md","../../policies/rules/documentation.md"]
---

# Repository Quality Gates

## Invoke

Bootstrap LES for a read-only assessment of repository health or before a broad
refactor/release decision.

## Inputs

Repository state, declared checks, package boundary, architecture conventions,
recent changes, and target quality concern.

## Procedure

1. Resolve scope and runnable gates. Done when: commands, paths, and exclusions are explicit.
2. Inspect structure, ownership, tests, dependencies, scripts, and documentation. Done when: findings trace to evidence rather than taste.
3. Run the smallest relevant checks. Done when: pass, fail, skipped, and unavailable results are separated.
4. Rank findings and safe next actions. Done when: no finding silently becomes an implementation.

## Output

Quality audit with scope, checks, findings, severity, confidence, evidence,
impact, owner, and next safe action.

## Guardrails

Read-only. Do not turn cleanup opportunities into unrequested refactoring or claim
quality from file presence alone.

## Verification

Every finding has a path or command evidence. A clean result lists the checks that
actually ran and their limits.
