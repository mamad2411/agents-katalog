---
name: les-release-readiness
description: Prove a release candidate meets package, compatibility, security, and rollback gates before publication.
invocation: user
maturity: stable
route: release
profile: core
bootstrap: skills/les-bootstrap/SKILL.md
loads: ["../les-bootstrap/SKILL.md","../../policies/workflows/verification.md","../../policies/verification.md","../../policies/rules/security.md","../../policies/rules/dependencies.md","../../policies/rules/git-safety.md","../../policies/rules/definition-of-done.md"]
---

# Release Readiness

## Invoke

Inherit `../les-bootstrap/SKILL.md` and release verification policy.

## Inputs

Release candidate, acceptance gates, package boundary, and rollback plan.

## Procedure

1. Resolve candidate identity, version, changed paths, and release objective. Done when: the candidate cannot be confused with a stale package.
2. Map package, inventory, compatibility, dependency, security, rollback, and documentation conditions to local checks. Done when: every gate has evidence.
3. Verify clean payload, generated manifests, scripts, and recovery path. Done when: results are classified by environment and exit status.
4. Separate local readiness from provider activation and host smoke. Done when: pending or waived evidence is explicit and no release authority is implied.

## Output

Release evidence with readiness state and terminal status.

## Guardrails

Do not publish, tag, push, or use credentials without immediate R3 approval.

## Verification

`PENDING_HOST_SMOKE` never supports a full runtime ready claim. A credit waiver is
reported as pending, not pass.

Bootstrap LES. Map release conditions to clean-build, package-boundary,
compatibility, security, and rollback checks. Output pass, fail, skipped, and
pending evidence separately. Verification remains local; stop before publishing,
tagging, pushing, or credential use without explicit R3 approval.
