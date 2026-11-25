---
name: test-enforcement
description: Enforces test discipline. Can be used to review test coverage, suggest missing tests, or act as the "arbiter" role in TDD flows. Follows the same Production Contract as other quality skills.
when-to-use: When test quality or coverage is critical, or as the test specialist in effort-scaled reviews.
---

# Test Enforcement Skill — Grok Edition

Specialized skill for the "Tests" reviewer slot in implement/execute-plan, and for standalone test quality work.

## Responsibilities (aligned with transferred disciplines)

- Review test coverage on changed code
- Flag missing edge cases, error paths, and integration tests
- Act as arbiter in TDD flows (verify Red before Green)
- Record testing-related friction patterns
- Use structured handoffs (QA form)

## Production Contract Alignment

- Pre-Flight: Understand what the implementation was supposed to do
- Ledger: When used inside a bounded loop, respect attempt count and previous feedback
- Friction: Testing gaps are high-value friction to record
- Verifier: This skill's findings should be visible to the final verifier

## Current Stub Status

This is a focused stub. Full implementation would include:
- AST / coverage tool integration for automatic analysis
- Stronger connection to the Task Lifecycle Ledger for multi-round test improvement
- Auto-generation of missing test skeletons (future)

For now it provides the contract, persona guidance, and handoff expectations so it can be used immediately as the "Tests" specialist in effort >= 2 runs.

When called, it should produce output compatible with the general review format + the handoff QA templates.