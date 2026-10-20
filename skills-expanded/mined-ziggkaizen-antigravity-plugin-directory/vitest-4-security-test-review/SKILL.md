---
name: vitest-4-security-test-review
description: Reviews Vitest 4 security regression coverage for authentication, authorization, access control, tokens, secrets, validation, injection, SSRF, CSRF, XSS, path traversal, and cryptography boundaries. Use when fixing security bugs or changing security-sensitive code.
license: MIT
compatibility: Vitest 4.x, Node.js 20+, and Vite 6+ when Vite integration is used.
---

# Vitest 4 Security Test Review

Use this skill when reviewing or designing tests for security-sensitive behavior.

## Workflow

- `workflows/security-regression-review-workflow.md`: Use when a security-sensitive change needs regression coverage.

## Resource

- `resources/security-regression-checklist.md`: Use to choose attack cases, denied paths, and fixture safety requirements.

## Example

- `examples/security-regression-test-example.md`: Reference example for testing denied access behavior.

## Script

Run with `--help` before using:

- `scripts/vitest-4-security-test-required.mjs`: Optional hook script that checks generic security-sensitive changed files and reminds agents when no related test files changed.

## Security Testing Principles

- Test the security property, not just the happy path.
- Ensure denied paths are explicit.
- Use safe fake tokens, fake secrets, and local fixtures.
- Never commit real credentials or sensitive production data.
- Avoid snapshots for security-critical logic unless the snapshot is tiny and intentionally reviewed.
- Do not downgrade security expectations to make a regression test pass.
